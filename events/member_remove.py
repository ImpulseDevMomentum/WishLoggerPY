from utils.imports import *

class MemberRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            server_language = get_server_language(member.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)

            channel_log_id = load_member_logs_channel_id(member.guild.id)
            
            if channel_log_id is not None:
                channel = nextcord.utils.get(member.guild.text_channels, id=int(channel_log_id))
                if channel is not None:
                    if member.bot:
                        embed = nextcord.Embed(title=language_strings.get("BOT_REMOVED_TITLE"), color=nextcord.Color.dark_red())
                        embed.add_field(name=language_strings.get("NAME"), value=member.name, inline=False)
                        deauthorized_by = "Unknown"
                        async for entry in member.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.kick):
                            if entry.target.id == member.id:
                                deauthorized_by = entry.user.mention
                                break
                        embed.add_field(name=language_strings.get("DEAUTHORIZED_BY"), value=deauthorized_by, inline=False)
                    else:
                        async for entry in member.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.ban):
                            if entry.target.id == member.id:
                                return
                        embed = nextcord.Embed(title=language_strings.get("USER_LEFT_TITLE"), color=nextcord.Color.dark_red())
                        
                        embed.add_field(name=language_strings.get("USER"), value=member.mention, inline=True)
                        embed.add_field(name=language_strings.get("USER_ID"), value=member.id, inline=True)
                        embed.add_field(name="", value="", inline=False)
                        
                        roles = [role.mention for role in member.roles[1:]]
                        roles_str = ", ".join(roles) if roles else language_strings.get("NONE")
                        embed.add_field(name=language_strings.get("ROLES"), value=roles_str, inline=True)

                        highest_role = member.top_role.mention if member.top_role else language_strings.get("NONE")
                        embed.add_field(name=language_strings.get("HIGHEST_ROLE"), value=highest_role, inline=True)
                        embed.add_field(name="", value="", inline=False)
                        
                        join_date = member.joined_at.strftime("%m/%d/%Y, %H:%M") if member.joined_at else language_strings.get("UNKNOWN")
                        embed.add_field(name=language_strings.get("JOINED_AT"), value=join_date, inline=True)
                        embed.add_field(name="", value="", inline=False)

                        joined_at_utc = member.joined_at.replace(tzinfo=timezone.utc) if member.joined_at else datetime.utcnow().replace(tzinfo=timezone.utc)
                        time_spent = datetime.utcnow().replace(tzinfo=timezone.utc) - joined_at_utc
                        days = time_spent.days
                        hours, remainder = divmod(time_spent.seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        time_spent_str = f"{days}d {hours}h {minutes}m {seconds}s"

                        embed.add_field(name=language_strings.get("TIME_SPENT_IN_SERVER"), value=time_spent_str, inline=True)
                        embed.add_field(name="", value="", inline=False)

                        kicked = False
                        async for entry in member.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.kick):
                            entry_time = entry.created_at.replace(tzinfo=None)
                            if entry.target.id == member.id and (datetime.utcnow() - entry_time).total_seconds() < 10:
                                kicked = True
                                embed.add_field(name=language_strings.get("ACTION"), value=language_strings.get("KICKED_ACTION").format(user=entry.user.mention), inline=False)
                                embed.add_field(name=language_strings.get("MODERATOR"), value=entry.user.mention, inline=False)
                                break
                        
                        if not kicked:
                            embed.add_field(name=language_strings.get("ACTION"), value=language_strings.get("USER_LEFT_ACTION"), inline=False)
                    
                    embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=False)
                    await channel.send(embed=embed)
        except Exception as e:
            print(f"Error in on_member_remove: {e}")


def setup(bot):
    bot.add_cog(MemberRemove(bot))