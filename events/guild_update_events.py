from utils.imports import *

class GuildUpdateEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_moderator(self, guild, action_type):
        entry = await guild.audit_logs(limit=1, action=action_type).find(lambda e: e.target.id == guild.id)
        return entry.user if entry else None

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        changes = []

        server_language = get_server_language(before.id)
        language_file = f'language/{server_language}.json'
        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        if before.name != after.name:
            changes.append(f"{language_strings.get('SERVER_NAME_CHANGED')}: `{before.name}` {language_strings.get('TO_SV_UPDATE')} `{after.name}`")

        if before.icon != after.icon:
            changes.append(language_strings.get('SERVER_ICON_CHANGED'))

        if before.banner != after.banner:
            changes.append(language_strings.get('SERVER_BANNER_CHANGED'))

        if before.region != after.region:
            changes.append(f"{language_strings.get('SERVER_REGION_CHANGED')}: `{before.region}` {language_strings.get('TO_SV_UPDATE')} `{after.region}`")

        if before.owner != after.owner:
            changes.append(f"{language_strings.get('SERVER_OWNER_CHANGED')}: `{before.owner}` {language_strings.get('TO_SV_UPDATE')} `{after.owner}`")

        if before.verification_level != after.verification_level:
            changes.append(f"{language_strings.get('SERVER_VERIFICATION_LEVEL_CHANGED')}: `{before.verification_level}` {language_strings.get('TO_SV_UPDATE')} `{after.verification_level}`")

        if before.explicit_content_filter != after.explicit_content_filter:
            changes.append(f"{language_strings.get('SERVER_EXPLICIT_CONTENT_FILTER_CHANGED')}: `{before.explicit_content_filter}` {language_strings.get('TO_SV_UPDATE')} `{after.explicit_content_filter}`")

        if before.verification_level != after.verification_level:
            changes.append(f"{language_strings.get('SERVER_VERIFICATION_LEVEL_CHANGED')}: `{before.verification_level}` {language_strings.get('TO_SV_UPDATE')} `{after.verification_level}`")

        if before.afk_channel != after.afk_channel:
            before_afk = before.afk_channel.name if before.afk_channel else language_strings.get('NONE')
            after_afk = after.afk_channel.name if after.afk_channel else language_strings.get('NONE')
            changes.append(f"{language_strings.get('SERVER_AFK_CHANNEL_CHANGED')}: `{before_afk}` {language_strings.get('TO_SV_UPDATE')} `{after_afk}`")

        if before.default_notifications != after.default_notifications:
            changes.append(f"{language_strings.get('SERVER_NOTIFICATION_SETTINGS_CHANGED')}: `{before.default_notifications}` {language_strings.get('TO_SV_UPDATE')} `{after.default_notifications}`")

        if before.afk_timeout != after.afk_timeout:
            changes.append(f"{language_strings.get('SERVER_AFK_TIMEOUT_CHANGED')}: `{before.afk_timeout} seconds` {language_strings.get('TO_SV_UPDATE')} `{after.afk_timeout} seconds`")

        if before.system_channel != after.system_channel:
            before_system = before.system_channel.name if before.system_channel else language_strings.get('NONE')
            after_system = after.system_channel.name if after.system_channel else language_strings.get('NONE')
            changes.append(f"{language_strings.get('SERVER_SYSTEM_CHANNEL_CHANGED')}: `{before_system}` {language_strings.get('TO_SV_UPDATE')} `{after_system}`")

        if before.description != after.description:
            changes.append(f"{language_strings.get('SERVER_DESCRIPTION_CHANGED')}: `{before.description or language_strings.get('NONE')}` {language_strings.get('TO_SV_UPDATE')} `{after.description or language_strings.get('NONE')}`")

        if before.premium_tier != after.premium_tier:
            changes.append(f"{language_strings.get('SERVER_PREMIUM_TIER_CHANGED')}: `{before.premium_tier}` {language_strings.get('TO_SV_UPDATE')} `{after.premium_tier}`")

        if before.premium_subscriber_role != after.premium_subscriber_role:
            changes.append(f"{language_strings.get('SERVER_PREMIUM_ROLE_CHANGED')}: `{before.premium_subscriber_role}` {language_strings.get('TO_SV_UPDATE')} `{after.premium_subscriber_role}`")


        if changes:
            channel_log_id = load_server_logs_channel_id(before.id)
            logs_channel = nextcord.utils.get(before.text_channels, id=int(channel_log_id))

            if logs_channel:
                embed = nextcord.Embed(title=language_strings.get('SERVER_UPDATE_TITLE'), color=nextcord.Color.dark_gold())
                changes_str = "\n".join(changes)
                embed.add_field(name=language_strings.get('CHANGES'), value=changes_str, inline=False)
                
                moderator = await self.fetch_moderator(after, nextcord.AuditLogAction.guild_update)

                if moderator:
                    embed.add_field(name=language_strings.get('MODERATOR'), value=moderator.mention, inline=False)
                    embed.add_field(name=language_strings.get('MODERATOR_ID'), value=moderator.id, inline=False)

                if after.icon:
                    embed.set_thumbnail(url=after.icon.url)
                if after.banner:
                    embed.set_image(url=after.banner.url)


                embed.add_field(name=language_strings.get('TODAY_AT'), value=current_datetime(), inline=True)
                await logs_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(GuildUpdateEvents(bot))