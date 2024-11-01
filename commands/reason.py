from utils.imports import *
import json

class ReasonCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="reason", description="Edit ban reason by Reason ID")
    async def reason(
        self, 
        interaction: nextcord.Interaction, 
        reasonid: str = SlashOption(description="Provide the reason ID to edit"), 
        reason: str = SlashOption(description="New reason to update")
    ):
        if not interaction.user.guild_permissions.ban_members and not interaction.user.guild_permissions.administrator and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permissions to this command.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        user_reason_data = self.load_ban_reason(guild_id, reasonid)

        if not user_reason_data:
            await interaction.response.send_message(f"<:Warning:1248654084500885526> Reason ID {reasonid} not found.", ephemeral=True)
            return

        log_message_id = user_reason_data.get("log_message_id")
        log_channel_id = user_reason_data.get("log_channel_id")

        if log_message_id and log_channel_id:
            channel = self.bot.get_channel(int(log_channel_id))
            try:
                message = await channel.fetch_message(int(log_message_id))
                embed = message.embeds[0]
                for i, field in enumerate(embed.fields):
                    if "Moderator, use /reason" in field.value or "Moderatorze, uzyj /reason" in field.value or "Moderatore, ispol'zuj /reason" in field.value or "Moderator, verwenden Sie /reason" in field.value or "Moderador, usa /reason" in field.value or "Moderator, pouzijte /reason" in field.value:
                        embed.set_field_at(i, name=field.name, value=reason, inline=field.inline)
                        break

                await message.edit(embed=embed)
                await interaction.response.send_message(f"<:Fine:1248352477502246932> Ban reason updated successfully for reason ID: {reasonid}.", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"<:NotFine:1248352479599661056> Failed to update the log embed: {str(e)}", ephemeral=True)
        else:
            await interaction.response.send_message(f"<:NotFine:1248352479599661056> Log message or channel not found for reason ID: {reasonid}.", ephemeral=True)

    def load_ban_reason(self, guild_id, reasonid):
        data = load_json('ban_reasons.json')
        if data and str(guild_id) in data and reasonid in data[str(guild_id)]:
            return data[str(guild_id)][reasonid]
        return None

    def save_ban_reason(self, guild_id, reasonid, reason_data):
        data = load_json('ban_reasons.json')
        if not data:
            data = {}

        if str(guild_id) not in data:
            data[str(guild_id)] = {}

        data[str(guild_id)][reasonid] = reason_data

        save_json('ban_reasons.json', data)

def setup(bot):
    bot.add_cog(ReasonCommand(bot))