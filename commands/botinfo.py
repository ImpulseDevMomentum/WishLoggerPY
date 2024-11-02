from utils.imports import *

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="information", description="Display information about the bot")
    async def display_bot_info(self, interaction: Interaction):
        server_count = len(self.bot.guilds)
        member_count = sum(guild.member_count for guild in self.bot.guilds)
        latency = f"{round(self.bot.latency * 1000)}ms"
        embed = nextcord.Embed(
            title="<:settings:1247982015207440384> About **Wish**",
            color=0x7289da
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1231737186391691314/1234082260773507093/Wishp.jpg?ex=6662daab&is=6661892b&hm=b3adb4f19522d99d2f78a71b38b36762dd8d7f38accd903c171704f4e24b86a9&")
        embed.add_field(name="<:info:1247959011605741579> Wish History", value="Wish was initially a long-term idea, but when we finally agreed to invest time in it, it simply became our mini hobby. Now, Wish is one of the biggest projects we've ever undertaken", inline=False)
        embed.add_field(name="<:info:1247959011605741579> Server Count", value=f"Wish is in {server_count} servers")
        embed.add_field(name="<:members:1245656464778068039> Members Count", value=f"Wish watches over {member_count} members")
        embed.add_field(name="<:6300pingconnection:1248350905800327250> Latency", value=f"My response time is: {latency}")
        embed.add_field(name="<:members:1245656464778068039> Creators", value=f"Wish was being programed by <@1122846756124774470>")
        embed.add_field(name="<:8859discordrolesfromvega:1248350895347863624> Discord Server", value="[Support Server](https://discord.gg/B3jZpkAuYB)", inline=False)
        embed.add_field(name="<:1626onlineweb:1248350904051302450> Website", value="[Wish Website](https://wishbot.xyz)", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(BotInfo(bot))
