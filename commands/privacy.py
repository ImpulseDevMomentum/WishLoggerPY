from utils.imports import *

class Privacy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="privacy", description="View Wish's Privacy Policy")
    async def privacy(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="Privacy Policy",
            description=(
                "Click the link below to view Wish's Privacy Policy. "
                "It's important to understand how we handle your personal information."
            ),
            color=0x1E90FF
        )
        embed.add_field(
            name="Privacy Policy", 
            value="[View Privacy Policy](https://wishbot.xyz/impulse/Wishpage/Privacy-Policy.html)", 
            inline=False
        )
        embed.set_footer(text="Thank you for your trust!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Privacy(bot))