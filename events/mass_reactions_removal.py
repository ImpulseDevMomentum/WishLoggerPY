from utils.imports import *





class RawReactionRemoval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_clear(self, payload):
        guild_id = payload.guild_id
        logs_channel_id = load_reaction_logs_channel_id(guild_id)
        if logs_channel_id is not None:
            logs_channel = nextcord.utils.get(self.bot.get_all_channels(), id=int(logs_channel_id))
            if logs_channel:
                guild = self.bot.get_guild(guild_id)
                if guild:
                    channel = guild.get_channel(payload.channel_id)
                    message = await channel.fetch_message(payload.message_id)
                    if message:
                        server_language = get_server_language(guild_id)
                        language_file = f'language/{server_language}.json'

                        with open(language_file, 'r') as file:
                            language_strings = json.load(file)

                        embed = nextcord.Embed(
                            title=language_strings.get("MASS_REACTIONS_CLEARED_TITLE"),
                            color=nextcord.Color.orange()
                        )
                        embed.add_field(
                            name=language_strings.get("MESSAGE"),
                            value=f"[Jump to Message]({message.jump_url})",
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("CHANNEL"),
                            value=message.channel.mention,
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("TODAY_AT"),
                            value=current_datetime(),
                            inline=True
                        )
                        await logs_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(RawReactionRemoval(bot))
