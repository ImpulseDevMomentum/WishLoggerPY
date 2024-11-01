from utils.imports import *

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="server", description="Check info about the server")
    async def server(self, interaction: Interaction):
        guild = interaction.guild

        guild_name = guild.name
        guild_id = guild.id
        guild_owner = guild.owner
        guild_owner_mention = guild_owner.mention if guild_owner else "Unknown"
        guild_region = guild.region
        guild_verification_level = guild.verification_level
        guild_member_count = guild.member_count
        guild_created_at = guild.created_at.strftime('%B %d, %Y')
        guild_icon_url = guild.icon.url if guild.icon else None

        members = guild.members
        users = len([member for member in members if not member.bot])
        bots = len([member for member in members if member.bot])

        embed = nextcord.Embed(title='<:info:1247959011605741579> Server Information Card', color=nextcord.Color.blurple())
        embed.set_thumbnail(url=guild_icon_url)
        embed.add_field(name='<:browsefotor:1245656463163002982> **Server Name**', value=guild_name, inline=False)
        embed.add_field(name='<:ID:1247954367953240155> **Server ID**', value=guild_id, inline=False)
        embed.add_field(name='<:Owner0:1234084745932177428> **Server Owner**', value=guild_owner_mention, inline=False)
        embed.add_field(name='<:settings:1247982015207440384> **Region**', value=guild_region, inline=False)
        embed.add_field(name='<:settings:1247982015207440384> **Verification Level**', value=guild_verification_level, inline=False)
        embed.add_field(name='<:members:1245656464778068039> **Total Members**', value=guild_member_count, inline=False)
        embed.add_field(name='<:time:1247976543678894182> **Created at**', value=guild_created_at, inline=False)

        embed.add_field(name="<:Member:1247954369639481498> **Users**", value=users, inline=False)

        embed.add_field(name="<:Apps:1248355147424338003> **Bots**", value=bots, inline=False)

        await interaction.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Server(bot))