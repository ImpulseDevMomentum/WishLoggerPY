from utils.imports import *

class Terms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="terms", description="View Wish's Terms of Service")
    async def terms(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="Terms of Service",
            description=(
                "Click the link below to view Wish's Terms of Service. "
                "It's important to review these terms to understand your rights and obligations."
            ),
            color=0x1E90FF
        )
        embed.add_field(
            name="Terms of Service", 
            value="[View Terms of Service](https://wishbot.xyz/impulse/Wishpage/Terms-of-Service.html)", 
            inline=False
        )
        embed.set_footer(text="Thank you for using Wish!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Terms(bot))
