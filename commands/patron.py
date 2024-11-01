from utils.imports import *

class Patron(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="patreon", description="Support us on Patreon")
    async def patreon(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="Support Us on Patreon!",
            description=(
                "If you'd like to support our project, click the link below to visit our Patreon. "
                "Please note that joining is purely voluntary and you will not receive any additional "
                "benefits. However, your contribution will help us continue to grow the project. "
                "A $1 donation goes a long way, and we greatly appreciate your support!"
            ),
            color=0x1E90FF
        )
        embed.add_field(
            name="Patreon Link", 
            value="[Visit our Patreon](https://www.patreon.com/wishdc/membership)", 
            inline=False
        )
        embed.set_footer(text="Thank you for supporting us!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Patron(bot))
