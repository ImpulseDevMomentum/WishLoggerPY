from utils.imports import *
import nextcord
from nextcord.ext import commands

class ChannelEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        try:
            server_language = get_server_language(channel.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)

            channel_log_id = load_server_logs_channel_id(channel.guild.id)

            if channel_log_id is not None:
                log_channel = nextcord.utils.get(channel.guild.text_channels, id=int(channel_log_id))
                if log_channel is not None:
                    async for entry in channel.guild.audit_logs(action=nextcord.AuditLogAction.channel_delete, limit=1):
                        moderator = entry.user
                        moderator_id = moderator.id

                        if isinstance(channel, nextcord.TextChannel):
                            title = language_strings.get("DELETED_TEXT_CHANNEL_TITLE")
                        elif isinstance(channel, nextcord.VoiceChannel):
                            title = language_strings.get("DELETED_VOICE_CHANNEL_TITLE")
                        elif isinstance(channel, nextcord.StageChannel):
                            title = language_strings.get("DELETED_STAGE_CHANNEL_TITLE")
                        elif channel.type == nextcord.ChannelType.news:
                            title = language_strings.get("DELETED_ANNOUNCEMENT_CHANNEL_TITLE")
                        elif isinstance(channel, nextcord.ForumChannel):
                            title = language_strings.get("DELETED_FORUM_CHANNEL_TITLE")
                        elif isinstance(channel, nextcord.CategoryChannel):
                            title = language_strings.get("DELETED_CATEGORY_TITLE")
                        else:
                            title = language_strings.get("DELETED_CHANNEL_TITLE")

                        embed = nextcord.Embed(
                            title=title,
                            color=nextcord.Color.dark_red()
                        )

                        embed.add_field(name=language_strings.get("CHANNEL_NAME"), value=channel.name, inline=False)
                        if isinstance(channel, nextcord.TextChannel) or isinstance(channel, nextcord.VoiceChannel) or isinstance(channel, nextcord.StageChannel):
                            if channel.category:
                                embed.add_field(name=language_strings.get("CATEGORY"), value=channel.category.name, inline=False)
                        embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                        embed.add_field(name=language_strings.get("MODERATOR_ID"), value=moderator_id, inline=False)
                        embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                        await log_channel.send(embed=embed)
                        return
        except Exception as e:
            print(f"Error in on_guild_channel_delete: {e}")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        try:
            server_language = get_server_language(channel.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)

            channel_log_id = load_server_logs_channel_id(channel.guild.id)

            if channel_log_id is not None:
                log_channel = nextcord.utils.get(channel.guild.text_channels, id=int(channel_log_id))
                if log_channel is not None:
                    async for entry in channel.guild.audit_logs(action=nextcord.AuditLogAction.channel_create, limit=1):
                        moderator = entry.user
                        moderator_id = moderator.id

                        if isinstance(channel, nextcord.TextChannel):
                            title = language_strings.get("CREATED_TEXT_CHANNEL_TITLE")
                        elif isinstance(channel, nextcord.VoiceChannel):
                            title = language_strings.get("CREATED_VOICE_CHANNEL_TITLE")
                        elif isinstance(channel, nextcord.StageChannel):
                            title = language_strings.get("CREATED_STAGE_CHANNEL_TITLE")
                        elif channel.type == nextcord.ChannelType.news:
                            title = language_strings.get("CREATED_ANNOUNCEMENT_CHANNEL_TITLE")
                        elif isinstance(channel, nextcord.ForumChannel):
                            title = language_strings.get("CREATED_FORUM_CHANNEL_TITLE")
                        elif isinstance(channel, nextcord.CategoryChannel):
                            title = language_strings.get("CREATED_CATEGORY_TITLE")
                        else:
                            title = language_strings.get("CREATED_CHANNEL_TITLE")

                        embed = nextcord.Embed(
                            title=title,
                            color=nextcord.Color.dark_green()
                        )

                        embed.add_field(name=language_strings.get("CHANNEL_NAME"), value=channel.name, inline=False)
                        if isinstance(channel, nextcord.TextChannel) or isinstance(channel, nextcord.VoiceChannel) or isinstance(channel, nextcord.StageChannel):
                            if channel.category:
                                embed.add_field(name=language_strings.get("CATEGORY"), value=channel.category.name, inline=False)
                        embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                        embed.add_field(name=language_strings.get("MODERATOR_ID"), value=moderator_id, inline=False)
                        embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                        await log_channel.send(embed=embed)
                        return
        except Exception as e:
            print(f"Error in on_guild_channel_create: {e}")

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        try:
            server_language = get_server_language(before.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)

            channel_log_id = load_server_logs_channel_id(before.guild.id)

            if channel_log_id is not None:
                logs_channel = nextcord.utils.get(before.guild.text_channels, id=int(channel_log_id))
                if logs_channel is not None:
                    async for entry in before.guild.audit_logs(action=nextcord.AuditLogAction.channel_update, limit=1):
                        moderator = entry.user

                        if isinstance(before, nextcord.TextChannel):
                            title = language_strings.get("UPDATED_TEXT_CHANNEL_TITLE")
                        elif isinstance(before, nextcord.VoiceChannel):
                            title = language_strings.get("UPDATED_VOICE_CHANNEL_TITLE")
                        elif isinstance(before, nextcord.StageChannel):
                            title = language_strings.get("UPDATED_STAGE_CHANNEL_TITLE")
                        elif before.type == nextcord.ChannelType.news:
                            title = language_strings.get("UPDATED_ANNOUNCEMENT_CHANNEL_TITLE")
                        elif isinstance(before, nextcord.ForumChannel):
                            title = language_strings.get("UPDATED_FORUM_CHANNEL_TITLE")
                        elif isinstance(before, nextcord.CategoryChannel):
                            title = language_strings.get("UPDATED_CATEGORY_TITLE")
                        else:
                            title = language_strings.get("UPDATED_CHANNEL_TITLE")

                        embed = nextcord.Embed(
                            title=title,
                            color=nextcord.Color.dark_orange()
                        )
                        embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                        embed.add_field(name=language_strings.get("CHANNEL_NAME"), value=f"<#{after.id}>", inline=False)

                        changes_detected = False

                        if before.name != after.name:
                            embed.add_field(name=language_strings.get("NAME"), value=f"{before.name} <:arrow:1233496150095564851> {after.name}", inline=False)
                            changes_detected = True

                        if before.type != after.type:
                            embed.add_field(name=language_strings.get("TYPE"), value=f"{before.type} <:arrow:1233496150095564851> {after.type}", inline=False)
                            changes_detected = True

                        if before.category != after.category:
                            embed.add_field(name=language_strings.get("CATEGORY"), value=f"{before.category.name if before.category else 'None'} <:arrow:1233496150095564851> {after.category.name if after.category else 'None'}", inline=False)
                            changes_detected = True

                        if before.is_nsfw() != after.is_nsfw():
                            embed.add_field(name=language_strings.get("NSFW"), value=f"{'<:on0:1234134687572688896>' if before.is_nsfw() else '<:off0:1234134671332479107>'} <:arrow:1233496150095564851> {'<:on0:1234134687572688896>' if after.is_nsfw() else '<:off0:1234134671332479107>'}", inline=False)
                            changes_detected = True

                        if isinstance(before, nextcord.TextChannel) and isinstance(after, nextcord.TextChannel):
                            if before.topic != after.topic:
                                embed.add_field(name=language_strings.get("DESCRIPTION"), value=f"{before.topic if before.topic else 'None'} <:arrow:1233496150095564851> {after.topic if after.topic else 'None'}", inline=False)
                                changes_detected = True

                            if before.slowmode_delay != after.slowmode_delay:
                                embed.add_field(name=language_strings.get("SLOWMODE"), value=f"{before.slowmode_delay} <:arrow:1233496150095564851> {after.slowmode_delay}", inline=False)
                                changes_detected = True

                        if isinstance(before, nextcord.VoiceChannel) and isinstance(after, nextcord.VoiceChannel):
                            if before.bitrate != after.bitrate:
                                embed.add_field(name=language_strings.get("BITRATE"), value=f"{before.bitrate} <:arrow:1233496150095564851> {after.bitrate}", inline=False)
                                changes_detected = True

                            if before.user_limit != after.user_limit:
                                embed.add_field(name=language_strings.get("USER_LIMIT"), value=f"{before.user_limit} <:arrow:1233496150095564851> {after.user_limit}", inline=False)
                                changes_detected = True

                            if before.video_quality_mode != after.video_quality_mode:
                                if after.video_quality_mode == nextcord.VideoQualityMode.full:
                                    after_video_quality = language_strings.get("FULL_QUALITY")
                                elif after.video_quality_mode == nextcord.VideoQualityMode.auto:
                                    after_video_quality = language_strings.get("AUTO_QUALITY")
                                else:
                                    after_video_quality = after.video_quality_mode

                                if before.video_quality_mode == nextcord.VideoQualityMode.full:
                                    before_video_quality = language_strings.get("FULL_QUALITY")
                                elif before.video_quality_mode == nextcord.VideoQualityMode.auto:
                                    before_video_quality = language_strings.get("AUTO_QUALITY")
                                else:
                                    before_video_quality = before.video_quality_mode

                                embed.add_field(name=language_strings.get("VIDEO_QUALITY_MODE"), value=f"{before_video_quality} <:arrow:1233496150095564851> {after_video_quality}", inline=False)
                                changes_detected = True

                            if before.rtc_region != after.rtc_region:
                                embed.add_field(name=language_strings.get("REGION"), value=f"{before.rtc_region if before.rtc_region else language_strings.get('AUTOMATIC') } <:arrow:1233496150095564851> {after.rtc_region if after.rtc_region else language_strings.get('AUTOMATIC')}", inline=False)
                                changes_detected = True

                        if isinstance(before, nextcord.StageChannel) and isinstance(after, nextcord.StageChannel):
                            if before.bitrate != after.bitrate:
                                embed.add_field(name=language_strings.get("BITRATE"), value=f"{before.bitrate} <:arrow:1233496150095564851> {after.bitrate}", inline=False)
                                changes_detected = True

                            if before.user_limit != after.user_limit:
                                embed.add_field(name=language_strings.get("USER_LIMIT"), value=f"{before.user_limit} <:arrow:1233496150095564851> {after.user_limit}", inline=False)
                                changes_detected = True

                            if before.video_quality_mode != after.video_quality_mode:
                                if after.video_quality_mode == nextcord.VideoQualityMode.full:
                                    after_video_quality = language_strings.get("FULL_QUALITY")
                                elif after.video_quality_mode == nextcord.VideoQualityMode.auto:
                                    after_video_quality = language_strings.get("AUTO_QUALITY")
                                else:
                                    after_video_quality = after.video_quality_mode

                                if before.video_quality_mode == nextcord.VideoQualityMode.full:
                                    before_video_quality = language_strings.get("FULL_QUALITY")
                                elif before.video_quality_mode == nextcord.VideoQualityMode.auto:
                                    before_video_quality = language_strings.get("AUTO_QUALITY")
                                else:
                                    before_video_quality = before.video_quality_mode

                                embed.add_field(name=language_strings.get("VIDEO_QUALITY_MODE"), value=f"{before_video_quality} <:arrow:1233496150095564851> {after_video_quality}", inline=False)
                                changes_detected = True

                        modified_permissions_embed = nextcord.Embed(
                            title=language_strings.get("PERMISSIONS_UPDATED_TITLE"),
                            color=nextcord.Color.blue()
                        )

                        for target, before_perm in before.overwrites.items():
                            after_perm = after.overwrites.get(target)
                            if before_perm != after_perm:
                                if target == before.guild.default_role:
                                    target_name = language_strings.get("EVERYONE")
                                else:
                                    target_name = target.display_name if isinstance(target, nextcord.Member) else target.mention

                                modified_permissions_embed.add_field(name=language_strings.get("ROLE_NAME") if isinstance(target, nextcord.Role) else language_strings.get("MEMBER_NAME"), value=target_name, inline=False)
                                modified_permissions_embed.add_field(name=language_strings.get("CHANNEL_NAME"), value=f"<#{after.id}>", inline=False)

                                async for entry in before.guild.audit_logs(action=nextcord.AuditLogAction.overwrite_update, limit=1):
                                    moderator = entry.user
                                    modified_permissions_embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)

                                modified_perms = []
                                if after_perm:
                                    for perm, value in after_perm:
                                        if value != getattr(before_perm, perm):
                                            truevale = "<:Added:1290710549188841483>" if value else "<:Removed:1290710550581481502>"
                                            modified_perms.append(f"{truevale}: {perm.replace('_', ' ').title()}")
                                else:
                                    modified_perms = [language_strings.get("NO_PERMISSION_CHANGES")]

                                modified_perm_desc = '\n'.join(modified_perms)
                                modified_permissions_embed.add_field(name="", value=modified_perm_desc, inline=False)

                        if len(modified_permissions_embed.fields) > 1:
                            modified_permissions_embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
                            await logs_channel.send(embed=modified_permissions_embed)

                        if changes_detected:
                            embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
                            await logs_channel.send(embed=embed)
        except Exception as e:
            print(f"Error in on_guild_channel_update: {e}")

def setup(bot):
    bot.add_cog(ChannelEvents(bot))