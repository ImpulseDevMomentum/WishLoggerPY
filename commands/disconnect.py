from utils.imports import *

class Disconnect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="disconnect", description="Disconnect a user from voice chat")
    async def disconnect(self, interaction: Interaction, user: nextcord.Member):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        bot_member = guild.get_member(self.bot.user.id)

        if user.voice is None:
            await interaction.response.send_message(f"<:NotFine:1248352479599661056> {user.mention} isn't in a voice channel", ephemeral=True)
            return

        if bot_member.top_role <= user.top_role:
            await interaction.response.send_message(f"<:NotFine:1248352479599661056> I can't disconnect {user.mention} because their role is higher or equal to mine", ephemeral=True)
            return

        if not (member.guild_permissions.manage_channels or member == guild.owner or member.guild_permissions.administrator):
            await interaction.response.send_message(f"<:PermDenied:1248352895854973029> You don't have permission to use this command", ephemeral=True)
            return

        try:
            await user.move_to(None)
            await interaction.response.send_message(f"<:Fine:1248352477502246932> {user.mention} has been disconnected from voice chat", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"<:NotFine:1248352479599661056> Failed to disconnect {user.mention}", ephemeral=True)

def setup(bot):
    bot.add_cog(Disconnect(bot))