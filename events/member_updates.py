from utils.imports import *
from nextcord.utils import get as nextcord_get

class MemberUpdates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        server_language = get_server_language(before.guild.id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        if before.communication_disabled_until != after.communication_disabled_until:
            channel_log_id = load_member_logs_channel_id(after.guild.id)
            if channel_log_id is not None:
                log_channel = nextcord.utils.get(after.guild.text_channels, id=int(channel_log_id))
                if log_channel is not None:
                    async for entry in after.guild.audit_logs(action=nextcord.AuditLogAction.member_update, limit=1):
                        if entry.target.id == after.id:
                            moderator = entry.user
                            reason = entry.reason if entry.reason else language_strings.get("NO_REASON_PROVIDED")

                            if after.communication_disabled_until is not None:
                                timeout_until = after.communication_disabled_until.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone("Europe/Warsaw"))
                                timeout_until_str = timeout_until.strftime("%m/%d/%Y, %H:%M %Z")

                                embed = nextcord.Embed(
                                    title=language_strings.get("MEMBER_TIMED_OUT_TITLE"),
                                    color=nextcord.Color.dark_red()
                                )
                                embed.add_field(name=language_strings.get("USER"), value=after.mention, inline=False)
                                embed.add_field(name=language_strings.get("USER_ID"), value=after.id, inline=False)
                                embed.add_field(name=language_strings.get("REASON"), value=f"**{reason}**", inline=False)
                                embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                                embed.add_field(name=language_strings.get("MODERATOR_ID"), value=moderator.id, inline=False)
                                embed.add_field(name=language_strings.get("TIMEOUT_UNTIL"), value=timeout_until_str, inline=True)
                                embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                            else:
                                embed = nextcord.Embed(
                                    title=language_strings.get("MEMBER_UNMUTED_TITLE"),
                                    color=nextcord.Color.green()
                                )
                                embed.add_field(name=language_strings.get("USER"), value=after.mention, inline=False)
                                embed.add_field(name=language_strings.get("USER_ID"), value=after.id, inline=False)
                                embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                                embed.add_field(name=language_strings.get("MODERATOR_ID"), value=moderator.id, inline=False)
                                embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                            await log_channel.send(embed=embed)
                            return

        if before.display_name != after.display_name:
            embed_a = nextcord.Embed(
                title=language_strings.get("EDITED_DISPLAY_NAME_TITLE"),
                color=nextcord.Color.dark_purple()
            )

            moderator_avatar = after.avatar.url if after.avatar else nextcord.Embed.Empty
            moderator_nick = after.display_name
            embed_a.set_author(name=moderator_nick, icon_url=moderator_avatar)
            embed_a.add_field(name=language_strings.get("USER"), value=before.mention)
            embed_a.add_field(name=language_strings.get("OLD"), value=before.display_name, inline=False)
            embed_a.add_field(name=language_strings.get("NEW"), value=after.display_name, inline=False)
            async for entry in before.guild.audit_logs(action=nextcord.AuditLogAction.member_update, limit=1):
                if entry.target.id == after.id and entry.changes.before.nick != entry.changes.after.nick:
                    moderator = entry.user
                    embed_a.add_field(name=language_strings.get("CHANGED_BY"), value=f"{moderator.mention}", inline=False)
                    break
            embed_a.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

            channel_log_id = load_member_logs_channel_id(before.guild.id)
            if channel_log_id is not None:
                logs_channel = nextcord.utils.get(before.guild.text_channels, id=int(channel_log_id))
                if logs_channel is not None:
                    await logs_channel.send(embed=embed_a)

        current_boost_count = after.guild.premium_subscription_count
        current_boost_level = after.guild.premium_tier
        previous_boost_count = before.guild.premium_subscription_count
        previous_boost_level = before.guild.premium_tier

        if not before.premium_since and after.premium_since:
            await self.log_boost_event(
                member=after,
                language_strings=language_strings,
                is_boost=True,
                boost_count=current_boost_count,
                boost_level=current_boost_level,
                previous_boost_count=previous_boost_count,
                previous_boost_level=previous_boost_level
            )

        if before.premium_since and not after.premium_since:
            await self.log_boost_event(
                member=after,
                language_strings=language_strings,
                is_boost=False,
                boost_count=current_boost_count,
                boost_level=current_boost_level,
                previous_boost_count=previous_boost_count,
                previous_boost_level=previous_boost_level
            )
    
    async def log_boost_event(self, member, language_strings, is_boost, boost_count, boost_level, previous_boost_count, previous_boost_level):
        if not hasattr(member.guild, "_boost_event_logged"):
            setattr(member.guild, "_boost_event_logged", {})

        if not member.guild._boost_event_logged.get(member.id, False):
            member.guild._boost_event_logged[member.id] = True
            channel_log_id = load_server_logs_channel_id(member.guild.id)
            if channel_log_id is not None:
                channel = nextcord_get(member.guild.text_channels, id=int(channel_log_id))
                if channel is not None:
                    embed_title = language_strings.get("BOOST_TITLE") if is_boost else language_strings.get("UNBOOST_TITLE")
                    embed_color = nextcord.Color.purple() if is_boost else nextcord.Color.red()

                    embed = nextcord.Embed(title=embed_title, color=embed_color)
                    embed.add_field(name=language_strings.get("USER"), value=member.mention)
                    embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
                    
                    if is_boost:
                        if boost_count != previous_boost_count and boost_level == previous_boost_level:
                            message = language_strings.get("SERVER_BOOST_INCREASE").format(boost_count=boost_count)
                        elif boost_level != previous_boost_level and boost_count == previous_boost_count:
                            message = language_strings.get("BOOST_LEVEL_INCREASE").format(boost_level=boost_level)
                        elif boost_count != previous_boost_count and boost_level != previous_boost_level:
                            message = language_strings.get("BOOST_AND_LEVEL_INCREASE").format(boost_count=boost_count, boost_level=boost_level)
                    else:
                        if boost_count != previous_boost_count and boost_level == previous_boost_level:
                            message = language_strings.get("SERVER_BOOST_DECREASE").format(boost_count=boost_count)
                        elif boost_level != previous_boost_level and boost_count == previous_boost_count:
                            message = language_strings.get("BOOST_LEVEL_DECREASE").format(boost_level=boost_level)
                        elif boost_count != previous_boost_count and boost_level != previous_boost_level:
                            message = language_strings.get("BOOST_AND_LEVEL_DECREASE").format(boost_count=boost_count, boost_level=boost_level)
                    
                    embed.add_field(name=language_strings.get("BOOST_UPDATE"), value=message, inline=False)
                    await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(MemberUpdates(bot))