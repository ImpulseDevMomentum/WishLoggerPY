from utils.imports import *

INVITE_CACHE_FILE = 'invite_cache.json'
USERS_INFO_FILE = 'users_info.json'

def load_json_file(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def save_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.invite_cache = load_json_file(INVITE_CACHE_FILE)
        self.users_info = load_json_file(USERS_INFO_FILE)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server_language = get_server_language(member.guild.id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        invites_before = self.invite_cache.get(str(member.guild.id), {})
        invites_after = await member.guild.invites()

        used_invite = None
        for invite in invites_after:
            if invite.code in invites_before and invites_before[invite.code] < invite.uses:
                used_invite = invite
                break

        self.invite_cache[str(member.guild.id)] = {invite.code: invite.uses for invite in invites_after}
        save_json_file(INVITE_CACHE_FILE, self.invite_cache)

        is_first_join = str(member.id) not in self.users_info
        if is_first_join:
            self.users_info[str(member.id)] = {'joined_at': str(member.joined_at)}

        channel_log_id = load_member_logs_channel_id(member.guild.id)
        if channel_log_id is not None:
            channel = nextcord.utils.get(member.guild.text_channels, id=int(channel_log_id))
            if channel is not None:
                if member.bot:
                    embed = nextcord.Embed(title=language_strings.get("BOT_ADDED_TITLE"), color=nextcord.Color.blue())
                    embed.add_field(name=language_strings.get("NAME"), value=member.name, inline=False)
                    embed.add_field(name=language_strings.get("AUTHORIZED_BY"), value=used_invite.inviter.mention if used_invite else "<:unknow:1252293325029904414>", inline=False)
                    embed.add_field(name=language_strings.get("VERIFIED"), value=f"Verified `>` {'<:Enabled:1248656166498730095>' if member.public_flags.verified_bot else '<:PermDenied:1248352895854973029>'}", inline=False)
                else:
                    embed = nextcord.Embed(title=language_strings.get("USER_JOINED_TITLE"), color=nextcord.Color.dark_green())
                    embed.add_field(name=language_strings.get("USER"), value=member.mention, inline=True)
                    embed.add_field(name=language_strings.get("USER_ID"), value=member.id, inline=True)

                    account_created_days_ago = (datetime.now(tz=pytz.utc) - member.created_at).days
                    if account_created_days_ago < 3:
                        embed.add_field(name=language_strings.get("ACCOUNT_AGE"), value=language_strings.get("ACCOUNT_AGE_WARNING"), inline=False)

                    was_ever_banned = any(entry.action == nextcord.AuditLogAction.ban and entry.target == member for entry in await member.guild.audit_logs(limit=None).flatten())
                    if was_ever_banned:
                        embed.add_field(name=language_strings.get("WAS_EVER_BANNED"), value=language_strings.get("USER_PREVIOUSLY_BANNED"), inline=False)

                    was_ever_kicked = any(entry.action == nextcord.AuditLogAction.kick and entry.target == member for entry in await member.guild.audit_logs(limit=None).flatten())
                    if was_ever_kicked:
                        embed.add_field(name=language_strings.get("WAS_EVER_KICKED"), value=language_strings.get("USER_PREVIOUSLY_KICKED"), inline=False)

                    join_status = language_strings.get("USER_FIRST_JOIN") if is_first_join else language_strings.get("USER_REJOINED")
                    embed.add_field(name=language_strings.get("JOINED_BEFORE"), value=join_status, inline=True)

                    if used_invite:
                        embed.add_field(name=language_strings.get("INVITED_BY"), value=used_invite.inviter.mention, inline=False)
                        embed.add_field(name=language_strings.get("INVITE_CODE"), value=f"https://discord.gg/{used_invite.code}", inline=False)
                        embed.add_field(name=language_strings.get("INVITE_USES"), value=used_invite.uses, inline=False)

                embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=False)
                await channel.send(embed=embed)

        save_json_file(USERS_INFO_FILE, self.users_info)

def setup(bot):
    bot.add_cog(MemberJoin(bot))
