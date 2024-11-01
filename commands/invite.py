from utils.imports import *

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="invite", description="Invite Wish to your server")
    async def invite(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="Invite Wish to Your Server!",
            description=(
                "Click the link below to invite Wish to your server. "
                "We appreciate your support and hope you enjoy using our bot!"
            ),
            color=0x1E90FF
        )
        embed.add_field(
            name="Invite Link", 
            value="[Invite Wish](https://discord.com/oauth2/authorize?client_id=1230554087443927060)", 
            inline=False
        )
        embed.set_footer(text="Thank you for supporting us!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Invite(bot))