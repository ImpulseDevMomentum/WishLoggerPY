from utils.imports import *

class StickerEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_stickers_update(self, guild, before, after):
        added_stickers = [sticker for sticker in after if sticker not in before]
        removed_stickers = [sticker for sticker in before if sticker not in after]

        channel_log_id = load_reaction_logs_channel_id(guild.id)
        logs_channel = nextcord.utils.get(guild.text_channels, id=int(channel_log_id))

        if not logs_channel:
            return

        server_language = get_server_language(guild.id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        if added_stickers:
            for sticker in added_stickers:
                async for entry in guild.audit_logs(action=nextcord.AuditLogAction.sticker_create, limit=1):
                    if entry.target.id == sticker.id:
                        user = entry.user

                embed = nextcord.Embed(title=language_strings.get("STICKER_ADDED_TITLE"), color=nextcord.Color.dark_green())
                embed.add_field(name=language_strings.get("NEW_STICKER"), value=sticker.name, inline=False)
                embed.add_field(name=language_strings.get("ADDED_BY"), value=user.mention, inline=False)
                embed.set_image(url=sticker.url)

                if sticker.description:
                    embed.add_field(name=language_strings.get("DESCRIPTION_STICKER"), value=sticker.description, inline=False)

                embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
                await logs_channel.send(embed=embed)

        if removed_stickers:
            for sticker in removed_stickers:
                async for entry in guild.audit_logs(action=nextcord.AuditLogAction.sticker_delete, limit=1):
                    if entry.target.id == sticker.id:
                        user = entry.user

                embed = nextcord.Embed(title=language_strings.get("STICKER_REMOVED_TITLE"), color=nextcord.Color.dark_red())
                embed.add_field(name=language_strings.get("REMOVED_STICKER"), value=sticker.name, inline=False)
                embed.add_field(name=language_strings.get("REMOVED_BY"), value=user.mention, inline=False)
                embed.set_image(url=sticker.url)
                embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
                await logs_channel.send(embed=embed)

        modified_stickers = []

        for before_sticker in before:
            for after_sticker in after:
                if before_sticker.id == after_sticker.id:
                    changes = {}
                    if before_sticker.name != after_sticker.name:
                        changes['name'] = (before_sticker.name, after_sticker.name)
                    if before_sticker.description != after_sticker.description:
                        changes['description'] = (before_sticker.description, after_sticker.description)
                    
                    if changes:
                        modified_stickers.append((before_sticker, after_sticker, changes))

        if modified_stickers:
            embed = nextcord.Embed(title=language_strings.get("STICKERS_UPDATED_TITLE"), color=nextcord.Color.orange())
            for before_sticker, after_sticker, changes in modified_stickers:
                async for entry in guild.audit_logs(action=nextcord.AuditLogAction.sticker_update, limit=1):
                    if entry.target.id == after_sticker.id:
                        user = entry.user

                description = ""
                if 'name' in changes:
                    description += f"{language_strings.get('NAME_STICKER')}: {before_sticker.name} {language_strings.get('TO_STICKER')} {after_sticker.name}\n"
                if 'description' in changes:
                    description += f"{language_strings.get('DESCRIPTION_STICKER')}: {before_sticker.description} {language_strings.get('TO_STICKER')} {after_sticker.description}\n"
                
                embed.add_field(name=before_sticker.name, value=description, inline=False)
                embed.add_field(name=language_strings.get("MODIFIED_BY"), value=user.mention, inline=False)
                embed.set_image(url=after_sticker.url)
            
            embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
            await logs_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(StickerEvents(bot))