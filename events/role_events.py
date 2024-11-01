from utils.imports import *

class RoleEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_language_strings(self, guild_id):
        server_language = get_server_language(guild_id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            return json.load(file)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        try:
            language_strings = await self.get_language_strings(role.guild.id)
            channel_log_id = load_role_logs_channel_id(role.guild.id)

            if channel_log_id is not None:
                log_channel = nextcord.utils.get(role.guild.text_channels, id=int(channel_log_id))
                if log_channel is not None:
                    async for entry in role.guild.audit_logs(action=nextcord.AuditLogAction.role_create, limit=1):
                        if entry.target == role:
                            moderator = entry.user

                            embed = nextcord.Embed(title=language_strings.get("ROLE_CREATED_TITLE"), color=nextcord.Color.dark_green())
                            embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                            embed.add_field(name=language_strings.get("MODERATOR_ID"), value=moderator.id, inline=False)
                            embed.add_field(name=language_strings.get("ROLE_NAME"), value=f"<@&{role.id}>", inline=False)
                            embed.add_field(name=language_strings.get("ROLE_ID"), value=role.id, inline=False)
                            embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                            await log_channel.send(embed=embed)
                            return
        except Exception as e:
            print(f"Error in on_guild_role_create: {e}")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        try:
            language_strings = await self.get_language_strings(role.guild.id)
            channel_log_id = load_role_logs_channel_id(role.guild.id)

            print(f"Role {role.name} deleted. Attempting to log...")  # Debug log

            if channel_log_id is not None:
                log_channel = nextcord.utils.get(role.guild.text_channels, id=int(channel_log_id))
                if log_channel is not None:
                    print(f"Found log channel: {log_channel.name} (ID: {log_channel.id})")  # Debug log
                    for _ in range(3):  # Retry mechanism, attempts 3 times
                        async for entry in role.guild.audit_logs(action=nextcord.AuditLogAction.role_delete, limit=1):
                            print(f"Checking audit log entry: {entry.action}, target: {entry.target}, user: {entry.user}")  # Debug log
                            if entry.target.id == role.id:  # Compare IDs to ensure the correct role
                                moderator = entry.user
                                print(f"Audit log entry found for role delete by {moderator}")  # Debug log

                                embed = nextcord.Embed(title=language_strings.get("ROLE_DELETED_TITLE"), color=nextcord.Color.dark_red())
                                embed.add_field(name=language_strings.get("ROLE_NAME"), value=role.name, inline=False)
                                embed.add_field(name=language_strings.get("ROLE_ID"), value=role.id, inline=False)
                                embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                                embed.add_field(name=language_strings.get("MODERATOR_ID"), value=moderator.id, inline=False)
                                embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                                await log_channel.send(embed=embed)
                                return
        except Exception as e:
            print(f"Error in on_guild_role_delete: {e}")

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        try:
            language_strings = await self.get_language_strings(before.guild.id)
            channel_log_id = load_role_logs_channel_id(before.guild.id)

            if channel_log_id is not None:
                log_channel = nextcord.utils.get(before.guild.text_channels, id=int(channel_log_id))
                if log_channel is not None:
                    async for entry in before.guild.audit_logs(action=nextcord.AuditLogAction.role_update, limit=1):
                        if entry.target == after:
                            moderator = entry.user

                            embed = nextcord.Embed(title=language_strings.get("ROLE_UPDATED_TITLE"), color=nextcord.Color.dark_blue())
                            embed.add_field(name=language_strings.get("ROLE"), value=f"<@&{after.id}>", inline=False)
                            embed.add_field(name=language_strings.get("ROLE_ID"), value=after.id, inline=False)
                            embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                            embed.add_field(name=language_strings.get("MODERATOR_ID"), value=moderator.id, inline=False)

                            role_changes_detected = False

                            if before.name != after.name:
                                embed.add_field(name=language_strings.get("ROLE_NAME_CHANGE"), value=f"{before.name} <:arrow:1233496150095564851> {after.name}", inline=False)
                                role_changes_detected = True

                            if before.color != after.color:
                                embed.add_field(name=language_strings.get("ROLE_COLOR_CHANGE"), value=f"{before.color} <:arrow:1233496150095564851> {after.color}", inline=False)
                                role_changes_detected = True

                            if before.hoist != after.hoist:
                                embed.add_field(name=language_strings.get("ROLE_HOIST_CHANGE"), value=f"{'<:on0:1234134687572688896>' if before.hoist else '<:off0:1234134671332479107>'} <:arrow:1233496150095564851> {'<:on0:1234134687572688896>' if after.hoist else '<:off0:1234134671332479107>'}", inline=False)
                                role_changes_detected = True

                            if before.mentionable != after.mentionable:
                                embed.add_field(name=language_strings.get("ROLE_MENTIONABLE_CHANGE"), value=f"{'<:on0:1234134687572688896>' if before.mentionable else '<:off0:1234134671332479107>'} <:arrow:1233496150095564851> {'<:on0:1234134687572688896>' if after.mentionable else '<:off0:1234134671332479107>'}", inline=False)
                                role_changes_detected = True

                            if before.permissions != after.permissions:
                                permission_changes = []
                                for perm, value in after.permissions:
                                    if value != getattr(before.permissions, perm):
                                        state = "<:on0:1234134687572688896>" if value else "<:off0:1234134671332479107>"
                                        permission_changes.append(f"{state}: {perm.replace('_', ' ').title()}")
                                        role_changes_detected = True

                                if permission_changes:
                                    embed.add_field(name=language_strings.get("PERMISSIONS_CHANGED_TITLE"), value='\n'.join(permission_changes), inline=False)

                            if role_changes_detected:
                                embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                                await log_channel.send(embed=embed)
                                return
        except Exception as e:
            print(f"Error in on_guild_role_update: {e}")

def setup(bot):
    bot.add_cog(RoleEvents(bot))