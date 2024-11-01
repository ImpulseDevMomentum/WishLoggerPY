from utils.imports import *
import io

MB_CACHE = 8
WORD_LIMIT = 500

class MessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        server_language = get_server_language(message.guild.id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        channel_log_id = load_message_logs_channel_id(message.guild.id)
        
        if not message.author.bot and channel_log_id:
            channel = nextcord.utils.get(message.guild.text_channels, id=int(channel_log_id))
            if channel:
                attachments = message.attachments
                stickers = message.stickers
                content = message.content
                truncate_length = 850

                warning_message = (
                    f"```diff\n- {language_strings.get('MESSAGE_HAD_INVITE')}\n```"
                    if any(invite in content for invite in ["discord.gg/", "discord.com/invite/"])
                    else ""
                )

                truncated_content = (
                    content[:truncate_length] + "..." if len(content) > truncate_length else content
                )

                def truncate_field(value, max_length=1024):
                    return value[:max_length - 3] + "..." if len(value) > max_length else value

                embed = nextcord.Embed(title=language_strings.get("DELETED_MESSAGE_TITLE"), color=nextcord.Color.dark_red())
                embed.add_field(name=language_strings.get("USER"), value=message.author.mention)
                
                if truncated_content:
                    embed.add_field(name=language_strings.get("CONTENT"), value=f"```{truncate_field(truncated_content)}```", inline=False)
                
                if message.reactions:
                    reactions_info = " ".join(f"{reaction.emoji} ({reaction.count})" for reaction in message.reactions)
                    embed.add_field(name=language_strings.get("REACTIONS"), value=truncate_field(reactions_info), inline=False)
                
                if attachments:
                    attachment_info = "\n".join(f"[{attachment.filename}]({attachment.url})" for attachment in attachments)
                    embed.add_field(name=language_strings.get("ATTACHMENTS_FIELD"), value=truncate_field(attachment_info), inline=False)
                
                if stickers:
                    stickers_info = " ".join(sticker.name for sticker in stickers)
                    embed.add_field(name=language_strings.get("STICKERS_FIELD"), value=truncate_field(stickers_info), inline=False)
                
                embed.add_field(name=language_strings.get("CHANNEL"), value=message.channel.mention, inline=False)

                if warning_message:
                    embed.add_field(name=language_strings.get("WARNING_LINK_IN_MESSAGE"), value=truncate_field(warning_message), inline=False)

                embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                await channel.send(embed=embed)

                if len(content) > truncate_length:
                    file_data = io.BytesIO(f"{language_strings.get('MESSAGE_DELETED_FULL')}\n{content}".encode('utf-8'))
                    await channel.send(file=nextcord.File(file_data, filename=f"deleted_message_{message.id}.txt"))

                for attachment in attachments:
                    file_size_mb = attachment.size / (1024 * 1024)

                    if file_size_mb <= MB_CACHE:
                        file_type = (
                            "Video" if attachment.content_type.startswith("video") else
                            "Image" if attachment.content_type.startswith("image") else
                            "Audio" if attachment.content_type.startswith("audio") else
                            "File"
                        )

                        file_info_message = f"File: {attachment.filename} | Size: {file_size_mb:.2f} MB | Type: {file_type}"
                        await channel.send(file_info_message)

                        try:
                            await channel.send(file=await attachment.to_file(spoiler=True))
                        except nextcord.errors.NotFound:
                            continue
                    else:
                        if attachment.filename.endswith(('.txt', '.log')):
                            file_bytes = await attachment.read()
                            file_text = file_bytes.decode('utf-8', errors='ignore')
                            truncated_text = " ".join(file_text.split()[:WORD_LIMIT]) + "..."
                            truncated_file_data = io.BytesIO(truncated_text.encode('utf-8'))

                            await channel.send(
                                content=f"{language_strings.get('FILE_TRUNCATED_NOTICE').format(filename=attachment.filename, word_limit=WORD_LIMIT)}",
                                file=nextcord.File(truncated_file_data, filename=f"truncated_{attachment.filename}")
                            )
                        else:
                            await channel.send(
                                f"{language_strings.get('FILE_TOO_LARGE')}".format(
                                    attachment_filename=attachment.filename,
                                    attachment_size=f"{file_size_mb:.2f} MB",
                                    MAX_FILE_SIZE=MB_CACHE
                                )
                            )

                for sticker in stickers:
                    try:
                        embed_sticker = nextcord.Embed(title=language_strings.get("STICKER"), color=nextcord.Color.dark_red())
                        embed_sticker.set_image(url=sticker.url)
                        await channel.send(embed=embed_sticker)
                    except Exception:
                        pass

def setup(bot):
    bot.add_cog(MessageDelete(bot))