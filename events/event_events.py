from utils.imports import *

class EventLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_scheduled_event_create(self, event):
        guild = event.guild
        server_language = get_server_language(guild.id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        logs_channel_id = load_server_logs_channel_id(guild.id)
        if logs_channel_id is not None:
            logs_channel = nextcord.utils.get(guild.text_channels, id=int(logs_channel_id))
            if logs_channel:
                embed = nextcord.Embed(
                    title=language_strings.get("NEW_SCHEDULED_EVENT_CREATED_TITLE"),
                    color=nextcord.Color.green()
                )
                embed.add_field(name=language_strings.get("EVENT_NAME"), value=event.name, inline=False)
                embed.add_field(name=language_strings.get("EVENT_ID"), value=str(event.id), inline=False)
                embed.add_field(name=language_strings.get("DESCRIPTION_EVENT"), value=event.description if event.description else language_strings.get("NONE"), inline=False)
                embed.add_field(name=language_strings.get("PRIVACY_LEVEL"), value=event.privacy_level.name, inline=False)
                embed.add_field(name=language_strings.get("CHANNEL"), value=event.channel.mention if event.channel else language_strings.get("NONE"), inline=False)
                embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                if event.image:
                    embed.set_image(url=event.image.url)
                if event.creator:
                    embed.set_author(name=event.creator.name, icon_url=event.creator.avatar.url if event.creator.avatar else None)

                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_scheduled_event_delete(self, event):
        guild = event.guild
        server_language = get_server_language(guild.id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        logs_channel_id = load_server_logs_channel_id(guild.id)
        if logs_channel_id is not None:
            logs_channel = nextcord.utils.get(guild.text_channels, id=int(logs_channel_id))
            if logs_channel:
                embed = nextcord.Embed(
                    title=language_strings.get("SCHEDULED_EVENT_DELETED_TITLE"),
                    color=nextcord.Color.red()
                )
                embed.add_field(name=language_strings.get("EVENT_NAME"), value=event.name, inline=False)
                embed.add_field(name=language_strings.get("EVENT_ID"), value=str(event.id), inline=False)
                embed.add_field(name=language_strings.get("DESCRIPTION_EVENT"), value=event.description if event.description else language_strings.get("NONE"), inline=False)
                embed.add_field(name=language_strings.get("PRIVACY_LEVEL"), value=event.privacy_level.name, inline=False)
                embed.add_field(name=language_strings.get("CHANNEL"), value=event.channel.mention if event.channel else language_strings.get("NONE"), inline=False)
                embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                if event.image:
                    embed.set_image(url=event.image.url)
                if event.creator:
                    embed.set_author(name=event.creator.name, icon_url=event.creator.avatar.url if event.creator.avatar else None)

                await logs_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(EventLogger(bot))