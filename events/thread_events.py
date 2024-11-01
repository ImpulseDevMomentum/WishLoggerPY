from utils.imports import *

class ThreadEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        try:
            channel_log_id = load_server_logs_channel_id(thread.guild.id)
            server_language = get_server_language(thread.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)

            if channel_log_id is not None:
                logs_channel = nextcord.utils.get(thread.guild.text_channels, id=int(channel_log_id))
                if logs_channel is not None:
                    async for entry in thread.guild.audit_logs(action=nextcord.AuditLogAction.thread_delete, limit=1):
                        moderator = entry.user

                        embed = nextcord.Embed(title=language_strings.get("THREAD_DELETED_TITLE"), color=nextcord.Color.dark_red())
                        embed.add_field(name=language_strings.get("THREAD_NAME"), value=thread.name, inline=False)
                        embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                        embed.add_field(name=language_strings.get("MODERATOR_ID"), value=moderator.id, inline=False)
                        embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                        await logs_channel.send(embed=embed)
                        break
        except Exception as e:
            print(f"Error in on_thread_delete: {e}")

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        try:
            channel_log_id = load_server_logs_channel_id(thread.guild.id)
            server_language = get_server_language(thread.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)

            if channel_log_id is not None:
                logs_channel = nextcord.utils.get(thread.guild.text_channels, id=int(channel_log_id))
                if logs_channel is not None:
                    async for entry in thread.guild.audit_logs(action=nextcord.AuditLogAction.thread_create, limit=1):
                        moderator = entry.user

                        embed = nextcord.Embed(title=language_strings.get("THREAD_CREATED_TITLE"), color=nextcord.Color.dark_green())
                        embed.add_field(name=language_strings.get("THREAD_NAME"), value=f"<#{thread.id}>", inline=False)
                        embed.add_field(name=language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                        embed.add_field(name=language_strings.get("MODERATOR_ID"), value=moderator.id, inline=False)
                        embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                        await logs_channel.send(embed=embed)
                        break
        except Exception as e:
            print(f"Error in on_thread_create: {e}")

    def format_time(self, seconds):
        if seconds < 60:
            return f"{seconds} {self.language_strings.get('SECONDS')}"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} {self.language_strings.get('MINUTES')}"
        else:
            hours = seconds // 3600
            return f"{hours} {self.language_strings.get('HOURS')}"

    @commands.Cog.listener()
    async def on_thread_update(self, before, after):
        try:
            channel_log_id = load_server_logs_channel_id(after.guild.id)
            server_language = get_server_language(after.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                self.language_strings = json.load(file)

            if channel_log_id is not None:
                logs_channel = nextcord.utils.get(after.guild.text_channels, id=int(channel_log_id))
                if logs_channel is not None:
                    async for entry in after.guild.audit_logs(action=nextcord.AuditLogAction.thread_update, limit=1):
                        moderator = entry.user

                        embed = nextcord.Embed(title=self.language_strings.get("THREAD_UPDATED_TITLE"), color=nextcord.Color.blue())
                        embed.add_field(name=self.language_strings.get("THREAD_NAME"), value=f"<#{after.id}>", inline=False)
                        embed.add_field(name=self.language_strings.get("MODERATOR"), value=moderator.mention, inline=False)
                        embed.add_field(name=self.language_strings.get("MODERATOR_ID"), value=moderator.id, inline=False)

                        if before.name != after.name:
                            embed.add_field(name=self.language_strings.get("THREAD_NAME_CHANGE"), value=f"{before.name} -> {after.name}", inline=False)

                        if not before.archived and after.archived:
                            embed.add_field(name=self.language_strings.get("THREAD_ARCHIVED_CHANGE"), value="<:on0:1234134687572688896>", inline=False)
                        elif before.archived and not after.archived:
                            embed.add_field(name=self.language_strings.get("THREAD_ARCHIVED_CHANGE"), value="<:off0:1234134671332479107> ", inline=False)

                        if not before.locked and after.locked:
                            embed.add_field(name=self.language_strings.get("THREAD_LOCKED_TITLE"), value="<:on0:1234134687572688896>", inline=False)
                        elif before.locked and not after.locked:
                            embed.add_field(name=self.language_strings.get("THREAD_LOCKED_TITLE"), value="<:off0:1234134671332479107>", inline=False)
                        
                        if before.slowmode_delay != after.slowmode_delay:
                            if after.slowmode_delay > 0:
                                formatted_time = self.format_time(after.slowmode_delay)
                                embed.add_field(name=self.language_strings.get("THREAD_SLOWMODE_CHANGED"), value=f"{formatted_time}", inline=False)
                            else:
                                embed.add_field(name=self.language_strings.get("THREAD_SLOWMODE_DISABLED"), value='', inline=False)

                        embed.add_field(name=self.language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                        await logs_channel.send(embed=embed)
                        break
        except Exception as e:
            print(f"Error in on_thread_update: {e}")

def setup(bot):
    bot.add_cog(ThreadEvents(bot))