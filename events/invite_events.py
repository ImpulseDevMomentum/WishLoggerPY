from utils.imports import *
import json
import nextcord
from nextcord.ext import commands

logged_invites = {}
invite_cache = {}

class InviteEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        try:
            server_language = get_server_language(invite.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)


            channel_log_id = load_server_logs_channel_id(invite.guild.id)
            logs_channel = nextcord.utils.get(invite.guild.text_channels, id=int(channel_log_id))

            if invite.code not in logged_invites and invite.code not in invite_cache.get(invite.guild.id, {}):
                logged_invites[invite.code] = True

                embed = nextcord.Embed(
                    title=language_strings.get("INVITE_CREATED_TITLE"),
                    color=nextcord.Color.dark_green()
                )
                
                embed.add_field(name=language_strings.get("INVITE_LINK"), value=f"https://discord.gg/{invite.code}", inline=False)
                embed.add_field(name=language_strings.get("MAX_USES"), value=invite.max_uses if invite.max_uses else language_strings.get("UNLIMITED"), inline=True)

                if invite.channel:
                    embed.add_field(name=language_strings.get("CHANNEL_INVITE").replace("{channel_name}", invite.channel.name), value="", inline=True)
                elif hasattr(invite, 'stage_instance'):
                    embed.add_field(name=language_strings.get("STAGE_INVITE").replace("{channel_name}", invite.stage_instance.channel.name), value="", inline=True)
                elif hasattr(invite, 'event'):
                    embed.add_field(name=language_strings.get("EVENT_INVITE").replace("{event_name}", invite.event.name), value="", inline=True)

                embed.add_field(name=language_strings.get("EXPIRES_AT"), value=invite.expires_at.strftime('%Y-%m-%d %H:%M:%S') if invite.expires_at else language_strings.get("NEVER"), inline=True)
                embed.add_field(name=language_strings.get("TEMPORARY"), value=language_strings.get("YES") if invite.temporary else language_strings.get("NO"), inline=True)
                embed.add_field(name=language_strings.get("CREATED_VIA"), value=invite.inviter.mention if invite.inviter else language_strings.get("UNKNOWN"), inline=False)
                embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                invites = await invite.guild.invites()
                invite_cache[invite.guild.id] = {inv.code: inv.uses for inv in invites}

                await logs_channel.send(embed=embed)

                await asyncio.sleep(15)
                del logged_invites[invite.code]
        except Exception as e:
            print(f"Error in on_invite_create: {e}")

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        try:
            server_language = get_server_language(invite.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)

            channel_log_id = load_server_logs_channel_id(invite.guild.id)
            logs_channel = nextcord.utils.get(invite.guild.text_channels, id=int(channel_log_id))

            embed = nextcord.Embed(
                title=language_strings.get("INVITE_DELETED_TITLE"),
                color=nextcord.Color.dark_red()
            )

            embed.add_field(name=language_strings.get("INVITE_LINK"), value=f"https://discord.gg/{invite.code}", inline=False)
            embed.add_field(name=language_strings.get("MAX_USES"), value=invite.max_uses if invite.max_uses else language_strings.get("UNLIMITED"), inline=True)

            if invite.channel:
                embed.add_field(name=language_strings.get("CHANNEL_INVITE").replace("{channel_name}", invite.channel.name), value="", inline=True)
            elif hasattr(invite, 'stage_instance'):
                embed.add_field(name=language_strings.get("STAGE_INVITE").replace("{channel_name}", invite.stage_instance.channel.name), value="", inline=True)
            elif hasattr(invite, 'event'):
                embed.add_field(name=language_strings.get("EVENT_INVITE").replace("{channel_name}", invite.invite.event.name), value="", inline=True)

            embed.add_field(name=language_strings.get("TEMPORARY"), value=language_strings.get("YES") if invite.temporary else language_strings.get("NO"), inline=True)
            embed.add_field(name=language_strings.get("EXPIRES_AT"), value=invite.expires_at.strftime('%Y-%m-%d %H:%M:%S') if invite.expires_at else language_strings.get("NEVER"), inline=True)

            guild = invite.guild
            async for entry in guild.audit_logs(limit=1, action=nextcord.AuditLogAction.invite_delete):
                deleted_by = entry.user
                embed.add_field(name=language_strings.get("DELETED_VIA"), value=deleted_by.mention, inline=False)
                embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
                await logs_channel.send(embed=embed)
                break
        except Exception as e:
            print(f"Error in on_invite_delete: {e}")

def setup(bot):
    bot.add_cog(InviteEvents(bot))