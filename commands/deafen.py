from utils.imports import *

class Deafen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="deafen", description="Toggle deafen for a user on voice chat")
    async def deafen(
        self, 
        interaction: Interaction, 
        user: nextcord.Member = SlashOption(description="User you want to deafen/undeafen", required=True)
):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        bot_member = guild.get_member(self.bot.user.id)

        if user.voice is None:
            await interaction.response.send_message(f"<:NotFine:1248352479599661056> {user.mention} isn't in a voice channel", ephemeral=True)
            return

        if bot_member.top_role <= user.top_role:
            await interaction.response.send_message(f"<:NotFine:1248352479599661056> I can't deafen/undeafen {user.mention} because their role is higher or equal to mine", ephemeral=True)
            return

        if not (member.guild_permissions.deafen_members or member == guild.owner or member.guild_permissions.administrator):
            await interaction.response.send_message(f"<:PermDenied:1248352895854973029> You don't have permission to use this command", ephemeral=True)
            return

        try:
            current_deafen_status = user.voice.deaf
            new_deafen_status = not current_deafen_status
            await user.edit(deafen=new_deafen_status)
            action = "deafened" if new_deafen_status else "undeafened"
            await interaction.response.send_message(f"<:Fine:1248352477502246932> {user.mention} has been {action}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"<:NotFine:1248352479599661056> Failed to deafen/undeafen {user.mention}.", ephemeral=True)

def setup(bot):
    bot.add_cog(Deafen(bot))