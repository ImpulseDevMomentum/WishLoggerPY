from utils.imports import *
import json

class MemberUnban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        try:
            server_language = get_server_language(guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)

            channel_log_id = load_member_logs_channel_id(guild.id)
            
            if channel_log_id is not None:
                channel = nextcord.utils.get(guild.text_channels, id=int(channel_log_id))
                if channel is not None:
                    async for entry in guild.audit_logs(limit=1):
                        if entry.action == nextcord.AuditLogAction.unban and entry.target == user:
                            moderator = entry.user

                            embed = nextcord.Embed(
                                color=nextcord.Color.green(),
                                title=language_strings.get("UNBANNED_USER_TITLE")
                            )
                            embed.add_field(name=language_strings.get("USER"), value=user.mention, inline=False)
                            embed.add_field(name=language_strings.get("USER_ID"), value=user.id, inline=False)
                            embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                            embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=False)

                            await channel.send(embed=embed)

                            self.remove_ban_data(guild.id, user.id)
                            return
        except Exception as e:
            print(f"Error in on_member_unban: {e}")

    def remove_ban_data(self, guild_id, user_id):
        data = load_json('ban_reasons.json')
        
        if not data:
            print("No data found in ban_reasons.json")
            return

        if str(guild_id) in data:
            reasons_to_remove = [key for key, value in data[str(guild_id)].items() if value.get("user_id") == str(user_id)]
            if reasons_to_remove:
                for reason_id in reasons_to_remove:
                    del data[str(guild_id)][reason_id]
                save_json('ban_reasons.json', data)
                print(f"Removed ban data for user ID {user_id} in guild ID {guild_id}.")
            else:
                print(f"No ban data found for user ID {user_id} in guild ID {guild_id}.")
        else:
            print(f"No records found for guild ID {guild_id}.")

def setup(bot):
    bot.add_cog(MemberUnban(bot))