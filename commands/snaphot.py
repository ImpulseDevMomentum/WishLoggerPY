from utils.imports import *
import json
import os
from datetime import datetime
import asyncio

def serialize_permissions(overwrites):
    permissions = {}
    for role, overwrite in overwrites.items():
        perm_dict = {}
        for perm in nextcord.Permissions.VALID_FLAGS:
            if hasattr(overwrite, perm):
                perm_dict[perm] = getattr(overwrite, perm)
        permissions[str(role.id)] = perm_dict
    return permissions

class Snap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="snap", description="Manage server snapshots")
    async def snap(self, interaction: Interaction):
        pass

    @snap.subcommand(name="create", description="Create a backup of the server. Only the server owner can use this command.")
    async def snap_create(
        self, 
        interaction: Interaction, 
        name: str = SlashOption(description="Name of your snapshot", default=None)
    ):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)

        if member != guild.owner:
            await interaction.response.send_message("Only the server owner can use this command.", ephemeral=True)
            return

        server_language = get_server_language(interaction.guild.id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        snapshot_dir = "snapshots"
        if not os.path.exists(snapshot_dir):
            os.makedirs(snapshot_dir)

        existing_snapshots = [f for f in os.listdir(snapshot_dir) if f.startswith(f"{guild.id}_") and f.endswith(".json")]
        if existing_snapshots:
            await interaction.response.send_message(language_strings.get("SNAPSHOT_EXISTS"), ephemeral=True)
            return

        if name is None:
            name = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_name = f"{guild.id}_{name}.json"

        embed = nextcord.Embed(title="Snapshot Creation", description="Starting the snapshot process...", color=0xADD8E6)
        msg = await interaction.response.send_message(embed=embed, ephemeral=True)

        data = {
            "name": guild.name,
            "id": guild.id,
            "created_at": datetime.now().isoformat(),
            "snapshot_name": name,
            "channels": [],
            "roles": [],
            "categories": []
        }

        for role in guild.roles:
            data["roles"].append({
                "name": role.name,
                "id": role.id,
                "snap_role_id": role.id,  # Custom identifier to link roles
                "permissions": role.permissions.value,
                "color": role.color.value,
                "hoist": role.hoist,
                "mentionable": role.mentionable,
                "position": role.position
            })

        for category in guild.categories:
            cat_data = {
                "name": category.name,
                "id": category.id,
                "snap_category_id": category.id,  # Custom identifier to link categories
                "position": category.position,
                "nsfw": category.is_nsfw(),
                "channels": []
            }

            for channel in category.channels:
                ch_data = {
                    "name": channel.name,
                    "id": channel.id,
                    "snap_channel_id": channel.id,  # Custom identifier to link channels
                    "type": str(channel.type),
                    "position": channel.position,
                    "topic": channel.topic if isinstance(channel, nextcord.TextChannel) else None,
                    "nsfw": channel.is_nsfw() if isinstance(channel, nextcord.TextChannel) else None,
                    "slowmode_delay": channel.slowmode_delay if isinstance(channel, nextcord.TextChannel) else None,
                    "bitrate": channel.bitrate if isinstance(channel, nextcord.VoiceChannel) else None,
                    "user_limit": channel.user_limit if isinstance(channel, nextcord.VoiceChannel) else None,
                    "rtc_region": str(channel.rtc_region) if isinstance(channel, nextcord.VoiceChannel) else None,
                    "permissions": serialize_permissions(channel.overwrites)
                }
                cat_data["channels"].append(ch_data)

            data["categories"].append(cat_data)

        uncategorized_channels = [ch for ch in guild.channels if ch.category is None]
        for channel in uncategorized_channels:
            ch_data = {
                "name": channel.name,
                "id": channel.id,
                "snap_channel_id": channel.id,  # Custom identifier to link channels
                "type": str(channel.type),
                "position": channel.position,
                "topic": channel.topic if isinstance(channel, nextcord.TextChannel) else None,
                "nsfw": channel.is_nsfw() if isinstance(channel, nextcord.TextChannel) else None,
                "slowmode_delay": channel.slowmode_delay if isinstance(channel, nextcord.TextChannel) else None,
                "bitrate": channel.bitrate if isinstance(channel, nextcord.VoiceChannel) else None,
                "user_limit": channel.user_limit if isinstance(channel, nextcord.VoiceChannel) else None,
                "rtc_region": str(channel.rtc_region) if isinstance(channel, nextcord.VoiceChannel) else None,
                "permissions": serialize_permissions(channel.overwrites)
            }
            data["channels"].append(ch_data)

        snapshot_path = os.path.join(snapshot_dir, snapshot_name)
        with open(snapshot_path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        embed.description = f"Snapshot `{name}` was created successfully."
        await msg.edit(embed=embed)

    @snap.subcommand(name="delete", description="Delete a server snapshot. Only the server owner can use this command.")
    async def snap_delete(
        self, 
        interaction: Interaction, 
        name: str = SlashOption(description="Name of your snapshot", default=None, required=True)
    ):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)

        if member != guild.owner:
            await interaction.response.send_message("Only the server owner can use this command.", ephemeral=True)
            return

        server_language = get_server_language(interaction.guild.id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        snapshot_dir = "snapshots"
        snapshot_path = os.path.join(snapshot_dir, f"{guild.id}_{name}.json")

        if os.path.exists(snapshot_path):
            os.remove(snapshot_path)
            await interaction.response.send_message(f"Snapshot `{name}` deleted successfully.", ephemeral=True)
        else:
            await interaction.response.send_message(f"No snapshot found with the name `{name}`.", ephemeral=True)

    @snap.subcommand(name="build", description="Rebuild the server from a snapshot. Only the server owner can use this command.")
    async def snap_build(
        self, 
        interaction: Interaction, 
        name: str = SlashOption(description="Name of your snapshot", default=None, required=True)
    ):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)

        # Check if the user is the server owner
        if member != guild.owner:
            await interaction.response.send_message("Only the server owner can use this command.", ephemeral=True)
            return

        # Get server language (assuming you have a function for this)
        server_language = get_server_language(interaction.guild.id)
        language_file = f'language/{server_language}.json'

        # Load language strings
        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        # Set the snapshot path
        snapshot_dir = "snapshots"
        snapshot_path = os.path.join(snapshot_dir, f"{guild.id}_{name}.json")

        # Check if the snapshot exists
        if not os.path.exists(snapshot_path):
            await interaction.response.send_message(f"No snapshot found with the name `{name}`.", ephemeral=True)
            return

        # Load the snapshot data
        with open(snapshot_path, "r") as f:
            data = json.load(f)

        # Send an initial embed message
        embed = nextcord.Embed(title="Snapshot Build", description="Starting the rebuild process...", color=0xADD8E6)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Step 1: Create Categories
        created_categories = {}
        for category_data in data["categories"]:
            category = nextcord.utils.get(guild.categories, id=int(category_data["snap_category_id"]))
            if not category:
                category = await guild.create_category(
                    name=category_data["name"], 
                    position=category_data["position"]
                )
                created_categories[category_data["snap_category_id"]] = category
                await asyncio.sleep(1)  # Slowmode

        # Step 2: Create Channels
        for category_data in data["categories"]:
            category = created_categories.get(category_data["snap_category_id"])
            for channel_data in category_data["channels"]:
                if not nextcord.utils.get(guild.channels, id=int(channel_data["snap_channel_id"])):
                    if channel_data["type"] == "text":
                        await guild.create_text_channel(
                            name=channel_data["name"], 
                            category=category, 
                            position=channel_data["position"], 
                            topic=channel_data.get("topic"), 
                            slowmode_delay=channel_data.get("slowmode_delay", 0)
                        )
                    elif channel_data["type"] == "voice":
                        rtc_region_value = channel_data.get("rtc_region")
                        if rtc_region_value == "None":
                            rtc_region_value = None
                        await guild.create_voice_channel(
                            name=channel_data["name"], 
                            category=category, 
                            position=channel_data["position"], 
                            bitrate=channel_data.get("bitrate", 64000), 
                            user_limit=channel_data.get("user_limit", 0),
                            rtc_region=rtc_region_value
                        )
                    await asyncio.sleep(1)  # Slowmode

        # Step 3: Create Roles
        for role_data in data["roles"]:
            if not nextcord.utils.get(guild.roles, id=int(role_data["snap_role_id"])):
                await guild.create_role(
                    name=role_data["name"], 
                    permissions=nextcord.Permissions(int(role_data["permissions"])), 
                    color=nextcord.Color(role_data["color"]), 
                    hoist=role_data["hoist"], 
                    mentionable=role_data["mentionable"]
                )
                await asyncio.sleep(1)  # Slowmode

        # Final update of the embed message
        embed.description = "Server rebuilt from snapshot successfully."
        await interaction.followup.send(embed=embed, ephemeral=True)

    @snap.subcommand(name="check", description="Check the details of the current snapshot. Only the server owner can use this command.")
    async def snap_check(self, interaction: Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)

        if member != guild.owner:
            await interaction.response.send_message("Only the server owner can use this command.", ephemeral=True)
            return

        snapshot_dir = "snapshots"
        existing_snapshots = [f for f in os.listdir(snapshot_dir) if f.startswith(f"{guild.id}_") and f.endswith(".json")]

        if not existing_snapshots:
            await interaction.response.send_message("No snapshot found for this server.", ephemeral=True)
            return

        snapshot_path = os.path.join(snapshot_dir, existing_snapshots[0])

        with open(snapshot_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        embed = nextcord.Embed(title="Snapshot Details", color=0xADD8E6)
        embed.add_field(name="Snapshot Name", value=data.get("snapshot_name", "Unknown"))
        embed.add_field(name="Creation Date", value=data.get("created_at", "Unknown"))
        embed.add_field(name="Server Name", value=data.get("name", "Unknown"))
        embed.set_footer(text=f"Snapshot ID: {data.get('id', 'Unknown')}")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @snap.subcommand(name="download", description="Download a server snapshot. Only the server owner can use this command.")
    async def snap_download(
        self, 
        interaction: Interaction,
        name: str = SlashOption(description="Name of your snapshot", default=None, required=True)
    ):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)

        if member != guild.owner:
            await interaction.response.send_message("Only the server owner can use this command.", ephemeral=True)
            return

        snapshot_dir = "snapshots"
        snapshot_path = os.path.join(snapshot_dir, f"{guild.id}_{name}.json")

        if not os.path.exists(snapshot_path):
            await interaction.response.send_message(f"No snapshot found with the name `{name}`.", ephemeral=True)
            return

        file = nextcord.File(snapshot_path, filename=f"{name}.json")
        await interaction.response.send_message(file=file, ephemeral=True)

def setup(bot):
    bot.add_cog(Snap(bot))