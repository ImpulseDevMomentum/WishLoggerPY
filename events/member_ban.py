from utils.imports import *
import json
import random

class MemberBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel_log_id = load_member_logs_channel_id(guild.id)
        
        if channel_log_id is not None:
            channel = nextcord.utils.get(guild.text_channels, id=int(channel_log_id))
            if channel is not None:
                async for entry in guild.audit_logs(limit=1):
                    if entry.action == nextcord.AuditLogAction.ban and entry.target == user:
                        server_language = get_server_language(guild.id)
                        language_file = f'language/{server_language}.json'

                        with open(language_file, 'r') as file:
                            language_strings = json.load(file)

                        moderator = entry.user
                        reason_id = str(random.randint(100000000, 999999999))
                        reason = entry.reason if entry.reason else language_strings.get("MODERATOR_USE").format(reason_id=reason_id)

                        embed = nextcord.Embed(title=language_strings.get("BANNED_USER_TITLE"),color=nextcord.Color.dark_red())
                        embed.add_field(name=language_strings.get("USER"), value=user.mention)
                        embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                        embed.add_field(name=language_strings.get("REASON"), value=reason, inline=False)
                        embed.add_field(name=language_strings.get("USER_ID"), value=user.id, inline=False)
                        embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=False)

                        log_message = await channel.send(embed=embed)

                        ban_data = {
                            "user_id": str(user.id),
                            "reason": reason,
                            "log_message_id": log_message.id,
                            "log_channel_id": channel.id
                        }
                        self.save_ban_reason(guild.id, reason_id, ban_data)

    def generate_reason_id(self):
        return str(random.randint(100000000, 999999999))

    def save_ban_reason(self, guild_id, reason_id, ban_data):
        data = load_json('ban_reasons.json')
        if not data:
            data = {}

        if str(guild_id) not in data:
            data[str(guild_id)] = {}

        data[str(guild_id)][reason_id] = ban_data

        save_json('ban_reasons.json', data)

def setup(bot):
    bot.add_cog(MemberBan(bot))