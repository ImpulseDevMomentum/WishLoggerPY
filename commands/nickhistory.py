from utils.imports import *

NICKNAME_HISTORY_FILE = "nicknames.json"
MAX_HISTORY_ENTRIES = 6

def load_nickname_history():
    if os.path.exists(NICKNAME_HISTORY_FILE):
        with open(NICKNAME_HISTORY_FILE, "r") as file:
            return json.load(file)
    return {}

def save_nickname_history(state):
    with open(NICKNAME_HISTORY_FILE, "w") as file:
        json.dump(state, file, indent=4)

class NicknameHistory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_nickname_history(self, before, after):
        if before.nick != after.nick:
            guild_id = str(after.guild.id)
            user_id = str(after.id)
            state = load_nickname_history()

            if guild_id not in state:
                state[guild_id] = {}

            if user_id not in state[guild_id]:
                state[guild_id][user_id] = []

            old_nick = before.nick if before.nick is not None else before.display_name
            new_nick = after.nick if after.nick is not None else after.display_name

            state[guild_id][user_id].append({
                "old_nick": old_nick,
                "new_nick": new_nick,
                "changed_at": current_datetime()
            })

            save_nickname_history(state)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        await self.update_nickname_history(before, after)

    @nextcord.slash_command(name="nickhistory", description="Manage nickname history")
    async def nickhistory(self, interaction: nextcord.Interaction):
        pass

    @nickhistory.subcommand(name="view", description="View a user's nickname history")
    async def view(
        self, 
        interaction: nextcord.Interaction, 
        member: nextcord.Member = SlashOption(description="The user you want to check", required=True)
    ):
        if not interaction.user.guild_permissions.administrator and not interaction.user.guild_permissions.manage_nicknames and interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message("<:Warning:1248654084500885526> You don't have permissions to use this command.", ephemeral=True)

        guild_id = str(interaction.guild.id)
        user_id = str(member.id)
        state = load_nickname_history()

        if guild_id in state and user_id in state[guild_id]:
            history = state[guild_id][user_id]
            if history:
                embed = nextcord.Embed(
                    title=f"<:customprofile0:1233820382277144666> Nickname History", 
                    description=f"Here is a log of the last {min(len(history), MAX_HISTORY_ENTRIES)} nickname changes for **{member.mention}**:",
                    color=nextcord.Color.blue()
                )
                embed.set_thumbnail(url=member.display_avatar.url)

                for entry in history[-MAX_HISTORY_ENTRIES:]:
                    embed.add_field(
                        name=f"<:time:1247976543678894182> {entry['changed_at']}",
                        value=f"**Old Nickname**: `{entry['old_nick']}`\n**New Nickname**: `{entry['new_nick']}`",
                        inline=False
                    )
                embed.set_footer(text="Nickname history is private and only visible to you or your discord mods")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(f"<:Warning:1248654084500885526> No nickname history found for **{member.mention}**.", ephemeral=True)
        else:
            await interaction.response.send_message(f"<:Warning:1248654084500885526> No nickname history found for **{member.mention}**.", ephemeral=True)

def setup(bot):
    bot.add_cog(NicknameHistory(bot))