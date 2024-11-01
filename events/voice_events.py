from utils.imports import *

class VoiceEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_voice_times = {}

    async def get_language_strings(self, guild_id):
        server_language = get_server_language(guild_id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            return json.load(file)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            language_strings = await self.get_language_strings(member.guild.id)
            logs_channel_id = load_server_logs_channel_id(member.guild.id)

            if logs_channel_id is not None:
                logs_channel = nextcord.utils.get(member.guild.text_channels, id=int(logs_channel_id))

                if logs_channel is not None:
                    if before.channel is None and after.channel is not None:
                        self.user_voice_times[member.id] = datetime.utcnow()
                        
                        users_on_channel = [user for user in after.channel.members if user.id != member.id]

                        embed = nextcord.Embed(
                            title=language_strings.get("JOINED_VC_TITLE"),
                            color=nextcord.Color.dark_green()
                        )
                        embed.add_field(
                            name=language_strings.get("USER"),
                            value=member.mention,
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("VC_NAME"),
                            value=f"{after.channel.name} (<#{after.channel.id}>)",
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("VC_ID"),
                            value=after.channel.id,
                            inline=False
                        )
                        
                        if users_on_channel:
                            users_list = ", ".join([f"{user.display_name} ({user.mention})" for user in users_on_channel[:7]])
                            if len(users_on_channel) > 7:
                                users_list += f", and {len(users_on_channel) - 7} more"
                            embed.add_field(
                                name=language_strings.get("USERS_ON_CHANNEL"),
                                value=users_list,
                                inline=False
                            )
                        
                        embed.add_field(
                            name=language_strings.get("TODAY_AT"),
                            value=current_datetime(),
                            inline=True
                        )
                        
                        await logs_channel.send(embed=embed)

                    elif before.channel is not None and after.channel is None:
                        join_time = self.user_voice_times.pop(member.id, None)
                        time_spent_str = str(datetime.utcnow() - join_time).split('.')[0] if join_time else language_strings.get("UNKNOWN", "Unknown")
                        
                        embed = nextcord.Embed(
                            title=language_strings.get("LEFT_VC_TITLE"),
                            color=nextcord.Color.dark_red()
                        )
                        embed.add_field(
                            name=language_strings.get("USER"),
                            value=member.mention,
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("VC_NAME"),
                            value=f"{before.channel.name} (<#{before.channel.id}>)",
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("VC_ID"),
                            value=before.channel.id,
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("TIME_SPENT"),
                            value=time_spent_str,
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("TODAY_AT"),
                            value=current_datetime(),
                            inline=True
                        )
                        
                        await logs_channel.send(embed=embed)

                    elif before.channel != after.channel and before.channel is not None and after.channel is not None:
                        embed = nextcord.Embed(
                            title=language_strings.get("MOVED_VC_TITLE"),
                            color=nextcord.Color.blue()
                        )
                        embed.add_field(
                            name=language_strings.get("USER"),
                            value=f"{member.name} ({member.mention})",
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("USER_ID"),
                            value=member.id,
                            inline=True
                        )
                        embed.add_field(
                            name=language_strings.get("FROM_VC"),
                            value=f"{before.channel.name} ({before.channel.mention})" if before.channel else "**N/A**",
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("TO_VC"),
                            value=f"{after.channel.name} ({after.channel.mention})" if after.channel else "**N/A**",
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("TODAY_AT"),
                            value=current_datetime(),
                            inline=False
                        )
                        
                        await logs_channel.send(embed=embed)

                    if before.self_stream != after.self_stream:
                        if after.self_stream:
                            action = language_strings.get("STREAM_STARTED_TITLE")
                            color = nextcord.Color.dark_green()
                        else:
                            action = language_strings.get("STREAM_ENDED_TITLE")
                            color = nextcord.Color.dark_red()
                            
                        embed = nextcord.Embed(
                            title=action,
                            color=color
                        )
                        embed.add_field(
                            name=language_strings.get("USER"),
                            value=member.mention,
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("VC_NAME"),
                            value=f"<#{after.channel.id if after.channel else before.channel.id}>",
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("TODAY_AT"),
                            value=current_datetime(),
                            inline=True
                        )
                        
                        await logs_channel.send(embed=embed)

                    if before.mute != after.mute or before.deaf != after.deaf:
                        action, color, channel_name = None, None, None

                        if before.mute != after.mute:
                            if after.mute:
                                action = language_strings.get("MUTED_VC")
                                color = nextcord.Color.dark_red()
                            else:
                                action = language_strings.get("UNMUTED_VC")
                                color = nextcord.Color.dark_green()
                            channel_name = after.channel.id if after.channel else "Unknown"

                        if before.deaf != after.deaf:
                            if after.deaf:
                                action = language_strings.get("DEAFENED")
                                color = nextcord.Color.dark_red()
                            else:
                                action = language_strings.get("UNDEAFENED")
                                color = nextcord.Color.dark_green()
                            channel_name = after.channel.id if after.channel else "Unknown"

                        if action is not None:
                            async for entry in member.guild.audit_logs(action=nextcord.AuditLogAction.member_update, limit=1):
                                if entry.target.id == member.id:
                                    moderator = entry.user
                                    embed = nextcord.Embed(
                                        title=action,
                                        color=color
                                    )
                                    embed.add_field(
                                        name=language_strings.get("USER"),
                                        value=member.mention,
                                        inline=False
                                    )
                                    embed.add_field(
                                        name=language_strings.get("USER_ID"),
                                        value=member.id,
                                        inline=False
                                    )
                                    embed.add_field(
                                        name=language_strings.get("MODERATOR"),
                                        value=moderator.mention,
                                        inline=False
                                    )
                                    embed.add_field(
                                        name=language_strings.get("MODERATOR_ID"),
                                        value=moderator.id,
                                        inline=False
                                    )
                                    embed.add_field(
                                        name=language_strings.get("CHANNEL"),
                                        value=f"<#{channel_name}>",
                                        inline=False
                                    )
                                    embed.add_field(
                                        name=language_strings.get("TODAY_AT"),
                                        value=current_datetime(),
                                        inline=True
                                    )
                                    await logs_channel.send(embed=embed)
                                    return

        except Exception as e:
            print(f"Error in on_voice_state_update: {e}")

def setup(bot):
    bot.add_cog(VoiceEvents(bot))