from utils.imports import *

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="embed", description="Send a custom embed to a channel")
    async def send_embed(
        self,
        interaction: Interaction,
        title: str,
        description: str,
        color: str,
        channel: nextcord.TextChannel,
        footer_text: str = None,
        footer_icon_url: str = None,
        image_url: str = None,
        author_name: str = None,
        author_icon_url: str = None,
    ):
        if interaction.user.guild_permissions.administrator or interaction.user == interaction.guild.owner:
            try:
                color = nextcord.Color(value=int(color, 16))
            except ValueError:
                await interaction.response.send_message("<:NotFine:1248352479599661056> Invalid color format. Please provide a valid [hex color code](https://www.color-hex.com). **Example** `004225`", ephemeral=True)
                return
            
            embed = nextcord.Embed(title=title, description=description, color=color)
            
            if footer_text:
                embed.set_footer(text=footer_text, icon_url=footer_icon_url)
            
            if image_url:
                embed.set_image(url=image_url)
            
            if author_name:
                embed.set_author(name=author_name, icon_url=author_icon_url)
            
            try:
                await channel.send(embed=embed)
                await interaction.response.send_message("<:Fine:1248352477502246932> Embed sent successfully!", ephemeral=True)
            except:
                await interaction.response.send_message("<:NotFine:1248352479599661056> Failed to send embed. Please check the channel permissions and try again.", ephemeral=True)
        else:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You do not have permission to use this command.", ephemeral=True)

def setup(bot):
    bot.add_cog(Embed(bot))