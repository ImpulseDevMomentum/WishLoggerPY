from utils.imports import *
import nextcord
from nextcord.ext import commands
import json
import io

TRUNCATE_LIMIT = 480

class ReactionEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        guild = reaction.message.guild
        server_language = get_server_language(guild.id)
        language_file = f'language/{server_language}.json'

        try:
            with open(language_file, 'r') as file:
                language_strings = json.load(file)
        except FileNotFoundError:
            print(f"Language file not found: {language_file}")
            return

        channel_log_id = load_reaction_logs_channel_id(guild.id)
        logs_channel = nextcord.utils.get(guild.text_channels, id=int(channel_log_id))

        try:
            if not reaction.message:
                message = await reaction.message.channel.fetch_message(reaction.message.id)
        except Exception as e:
            print(f"Could not fetch message: {e}")
            return

        if logs_channel:
            original_content = reaction.message.content or language_strings.get("NO_CONTENT")
            truncated_content = (
                original_content[:TRUNCATE_LIMIT] + "..." if len(original_content) > TRUNCATE_LIMIT else original_content
            )

            embed = nextcord.Embed(
                title=language_strings.get("REACTION_REMOVED_TITLE"), 
                color=nextcord.Color.red()
            )
            embed.add_field(
                name=language_strings.get("USER"), 
                value=user.mention, 
                inline=True
            )
            embed.add_field(
                name=language_strings.get("MESSAGE"), 
                value=reaction.message.jump_url, 
                inline=True
            )
            embed.add_field(
                name=language_strings.get("EMOJI"), 
                value=str(reaction.emoji), 
                inline=True
            )
            embed.add_field(
                name=language_strings.get("CHANNEL"), 
                value=reaction.message.channel.mention, 
                inline=True
            )
            embed.add_field(
                name=language_strings.get("MESSAGE_CONTENT"), 
                value=f"```{truncated_content}```", 
                inline=False
            )
            embed.add_field(
                name=language_strings.get("USER_ID"), 
                value=user.id, 
                inline=True
            )
            embed.add_field(
                name=language_strings.get("MESSAGE_ID"), 
                value=reaction.message.id, 
                inline=True
            )
            embed.add_field(
                name=language_strings.get("TODAY_AT"), 
                value=current_datetime(), 
                inline=True
            )

            await logs_channel.send(embed=embed)

            if len(original_content) > TRUNCATE_LIMIT:
                file_data = io.BytesIO(f"{language_strings.get('FULL_MESSAGE_CONTENT_IN_EMOJI_LOG')}\n{original_content}".encode('utf-8'))
                await logs_channel.send(file=nextcord.File(file_data, filename=f"message_content_{reaction.message.id}.txt"))

def setup(bot):
    bot.add_cog(ReactionEvents(bot))