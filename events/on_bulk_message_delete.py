from utils.imports import *

class BulkMessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        if len(messages) > 0:
            server_language = get_server_language(messages[0].guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)

            channel_log_id = load_message_logs_channel_id(messages[0].guild.id)
            if channel_log_id is not None:
                channel = nextcord.utils.get(messages[0].guild.text_channels, id=int(channel_log_id))
                if channel is not None:
                    embed = nextcord.Embed(title=language_strings.get("MASS_MESSAGE_DELETE_TITLE"), color=nextcord.Color.red())
                    embed.add_field(name=language_strings.get("CHANNEL"), value=messages[0].channel.mention, inline=False)
                    
                    for message in messages:
                        if not message.author.bot:
                            content = message.content
                            attachments = message.attachments
                            stickers = message.stickers
                            attachment_info = "\n".join([f"[{attachment.filename}]({attachment.url})" for attachment in attachments]) if attachments else language_strings.get("NO_ATTACHMENTS", language_strings.get("ATTACHMENTS", "**None**"))
                            
                            if any(invite_link in content for invite_link in ["discord.gg/", "discord.com/invite/"]):
                                warning_message = f"```diff\n- {language_strings.get('MESSAGE_HAD_INVITE')}\n```"
                            else:
                                warning_message = ""

                            embed.add_field(name=f"{language_strings.get('DELETED_BY')} {message.author}", value=f"{language_strings.get('CONTENT')}: ```{content}```", inline=False)
                            
                            if message.reactions:
                                reactions_info = ""
                                for reaction in message.reactions:
                                    reactions_info += f"{reaction.emoji} ({reaction.count}) "
                                embed.add_field(name=language_strings.get("REACTIONS"), value=reactions_info, inline=False)

                            if attachments:
                                embed.add_field(name=language_strings.get("ATTACHMENTS_FIELD"), value=attachment_info, inline=False)

                            if stickers:
                                stickers_info = " ".join([sticker.name for sticker in stickers])
                                embed.add_field(name=language_strings.get("STICKERS_FIELD"), value=stickers_info, inline=False)
                                
                            if warning_message:
                                embed.add_field(name=language_strings.get("WARNING_LINK_IN_MESSAGE"), value=warning_message, inline=False)
                    
                    embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
                    
                    await channel.send(embed=embed)

                    for message in messages:
                        attachments = message.attachments
                        stickers = message.stickers

                        for attachment in attachments:
                            if attachment.width and attachment.height:
                                try:
                                    await channel.send(content=f"||Spoiler: {attachment.filename}||", file=await attachment.to_file(spoiler=True))
                                except nextcord.errors.NotFound:
                                    pass
                            elif attachment.size <= 9999999999999:
                                try:
                                    await channel.send(content=f"||Spoiler: {attachment.filename}||", file=await attachment.to_file(spoiler=True))
                                except nextcord.errors.NotFound:
                                    pass

                        for sticker in stickers:
                            try:
                                embed_sticker = nextcord.Embed(title=language_strings.get("STICKER"), color=nextcord.Color.dark_red())
                                embed_sticker.set_image(url=sticker.url)
                                await channel.send(embed=embed_sticker)
                            except Exception as e:
                                print(f"Error sending sticker: {e}")
def setup(bot):
    bot.add_cog(BulkMessageDelete(bot))