from utils.imports import *

class Docs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="docs", description="View Wish's Documentation")
    async def docs(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="Wish's Documentation",
            description=(
                "Click the link below to access Wish's documentation. "
                "Here you'll find all the information you need to use our bot effectively."
            ),
            color=0x1E90FF
        )
        embed.add_field(
            name="Documentation Link", 
            value="View Documentation", 
            inline=False
        )
        embed.set_footer(text="Explore and get the most out of Wish!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Docs(bot))
