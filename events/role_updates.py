from utils.imports import *

class RoleUpdates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            removed_roles = [role for role in before.roles if role not in after.roles]
            added_roles = [role for role in after.roles if role not in before.roles]

            channel_log_id = load_member_logs_channel_id(before.guild.id)
            server_language = get_server_language(before.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)

            if channel_log_id is not None:
                channel = nextcord.utils.get(before.guild.text_channels, id=int(channel_log_id))

                if channel is not None:
                    async for entry in after.guild.audit_logs(action=nextcord.AuditLogAction.member_role_update, limit=1):
                        moderator = entry.user

                        if removed_roles:
                            embed = nextcord.Embed(title=language_strings.get("ROLES_TAKEN_TITLE"), color=nextcord.Color.dark_red())
                            embed.add_field(name=language_strings.get("USER"), value=after.mention)
                            embed.add_field(name=language_strings.get("USER_ID"), value=after.id, inline=False)
                            if moderator.id == after.id:
                                embed.add_field(name=language_strings.get("TYPE"), value=language_strings.get("ROLES_SELF_TAKEN_TYPE"), inline=False)
                            else:
                                embed.add_field(name=language_strings.get("TYPE"), value=language_strings.get("ROLES_TAKEN_TYPE"), inline=False)
                            embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                            embed.add_field(name=language_strings.get("TAKEN_ROLE"), value=', '.join([f"<@&{role.id}>" for role in removed_roles]), inline=False)
                            embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
                            await channel.send(embed=embed)

                        if added_roles:
                            embed = nextcord.Embed(title=language_strings.get("ROLES_GIVEN_TITLE"), color=nextcord.Color.dark_green())
                            embed.add_field(name=language_strings.get("USER"), value=after.mention)
                            embed.add_field(name=language_strings.get("USER_ID"), value=after.id, inline=False)
                            if moderator.id == after.id:
                                embed.add_field(name=language_strings.get("TYPE"), value=language_strings.get("ROLES_SELF_GIVEN_TYPE"), inline=False)
                            else:
                                embed.add_field(name=language_strings.get("TYPE"), value=language_strings.get("ROLES_GIVEN_TYPE"), inline=False)
                            embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                            embed.add_field(name=language_strings.get("ADDED_ROLE"), value=', '.join([f"<@&{role.id}>" for role in added_roles]), inline=False)
                            embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
                            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(RoleUpdates(bot))