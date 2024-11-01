from utils.imports import *
import os

class MessageEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        server_language = get_server_language(before.guild.id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        channel_log_id = load_message_logs_channel_id(before.guild.id)
        
        if channel_log_id is not None:
            channel = nextcord.utils.get(before.guild.text_channels, id=int(channel_log_id))
            if channel is not None:
                if before.content != after.content:
                    truncate_length = 710
                    message_url = f"https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"
                    embed = nextcord.Embed(title=language_strings.get("EDITED_MESSAGE_TITLE"), color=nextcord.Color.dark_orange())
                    embed.add_field(name=language_strings.get("USER"), value=before.author.mention, inline=True)
                    
                    def truncate_message(message):
                        if len(message) > truncate_length:
                            return message[:truncate_length] + "..."
                        return message

                    original_message = truncate_message(before.content)
                    edited_message = truncate_message(after.content)

                    embed.add_field(name=language_strings.get("ORIGINAL_MESSAGE"), value=original_message, inline=False)
                    embed.add_field(name=language_strings.get("EDITED_MESSAGE"), value=edited_message, inline=False)
                    
                    embed.add_field(name=language_strings.get("JUMP_TO_MESSAGE"), value=f"[{language_strings.get('CLICK_HERE')}]({message_url})", inline=False)
                    embed.add_field(name=language_strings.get("CHANNEL"), value=before.channel.mention, inline=False)
                    embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=False)

                    if len(before.content) > truncate_length or len(after.content) > truncate_length:
                        file_content = (
                            f"{language_strings.get('MESSAGE_EDITED_ORIGINAL_BEFORE')}\n{before.content}\n\n"
                            f"{language_strings.get('MESSAGE_EDITED_ORIGINAL_AFTER')}\n{after.content}\n"
                        )
                        file_name = f"message_edit_{before.id}.txt"
                        with open(file_name, 'w', encoding='utf-8') as file:
                            file.write(file_content)
                        
                        await channel.send(embed=embed)
                        await channel.send(file=nextcord.File(file_name))

                        os.remove(file_name)
                    else:
                        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(MessageEdit(bot))