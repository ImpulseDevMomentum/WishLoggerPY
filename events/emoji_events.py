from utils.imports import *

class EmojiEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        added_emojis = [emoji for emoji in after if emoji not in before]
        removed_emojis = [emoji for emoji in before if emoji not in after]

        channel_log_id = load_server_logs_channel_id(guild.id)
        logs_channel = nextcord.utils.get(guild.text_channels, id=int(channel_log_id))

        if not logs_channel:
            return
        
        server_language = get_server_language(guild.id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        if added_emojis:
            added_emojis_str = "\n".join(f"{emoji} (:{emoji.name}:)" for emoji in added_emojis)
            audit_log_entries = await guild.audit_logs(action=nextcord.AuditLogAction.emoji_create, limit=len(added_emojis)).flatten()
            added_by = {entry.target.id: entry.user for entry in audit_log_entries}

            embed = nextcord.Embed(title=language_strings.get("EMOJIS_ADDED_TITLE"), color=nextcord.Color.dark_green())
            embed.add_field(name=language_strings.get("NEW_EMOJIS"), value=added_emojis_str, inline=False)
            for emoji in added_emojis:
                user = added_by.get(emoji.id, "Unknown")
                embed.add_field(name=language_strings.get("ADDED_BY"), value=f"{user.mention if user != 'Unknown' else 'Unknown'}", inline=False)
            embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
            await logs_channel.send(embed=embed)

        if removed_emojis:
            removed_emojis_str = "\n".join(f"{emoji} (:{emoji.name}:)" for emoji in removed_emojis)
            audit_log_entries = await guild.audit_logs(action=nextcord.AuditLogAction.emoji_delete, limit=len(removed_emojis)).flatten()
            removed_by = {entry.target.id: entry.user for entry in audit_log_entries}

            embed = nextcord.Embed(title=language_strings.get("EMOJIS_REMOVED_TITLE"), color=nextcord.Color.dark_red())
            embed.add_field(name=language_strings.get("REMOVED_EMOJIS"), value=removed_emojis_str, inline=False)
            for emoji in removed_emojis:
                user = removed_by.get(emoji.id, "Unknown")
                embed.add_field(name=language_strings.get("REMOVED_BY"), value=f"{user.mention if user != 'Unknown' else 'Unknown'}", inline=False)
            embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
            await logs_channel.send(embed=embed)
        
        renamed_emojis = []
        for before_emoji in before:
            for after_emoji in after:
                if before_emoji.id == after_emoji.id and before_emoji.name != after_emoji.name:
                    renamed_emojis.append((before_emoji, after_emoji))

        if renamed_emojis:
            audit_log_entries = await guild.audit_logs(action=nextcord.AuditLogAction.emoji_update, limit=len(renamed_emojis)).flatten()
            renamed_by = {entry.target.id: entry.user for entry in audit_log_entries}
            
            embed = nextcord.Embed(title=language_strings.get("EMOJIS_RENAMED_TITLE"), color=nextcord.Color.orange())
            for before_emoji, after_emoji in renamed_emojis:
                user = renamed_by.get(after_emoji.id, "Unknown")
                embed.add_field(
                    name=language_strings.get("EMOJI_RENAMED"),
                    value=f"{before_emoji} (:{before_emoji.name}:) {language_strings.get('TO_EMOJI')} (:{after_emoji.name}:) {language_strings.get('BY')} {user.mention if user != 'Unknown' else 'Unknown'}",
                    inline=False
                )
            embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
            await logs_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(EmojiEvents(bot))