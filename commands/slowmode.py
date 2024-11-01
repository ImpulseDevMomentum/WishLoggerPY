from utils.imports import *
class Slowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="slowmode", description="Set slowmode for a channel")
    async def slowmode(self, interaction: Interaction, seconds: int):
        if interaction.user.guild_permissions.manage_channels:
            await interaction.channel.edit(slowmode_delay=seconds)
            await interaction.send(f"<:Fine:1248352477502246932> Slowmode is set to {seconds} second(s) on {interaction.channel.mention}", ephemeral=True)
        else:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permissions to use this command.", ephemeral=True)

def setup(bot):
    bot.add_cog(Slowmode(bot))