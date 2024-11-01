from nextcord.ext import commands
import nextcord

class Invites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="invites", description="Show user's invite statistics")
    async def invites(self, interaction: nextcord.Interaction, user: nextcord.Member):
        total_invites = 0
        active_invites = []
        for invite in await interaction.guild.invites():
            if invite.inviter == user:
                total_invites += invite.uses
                active_invites.append(invite)

        embed = nextcord.Embed(
            title=f"{user.display_name}'s Invites",
            description=f"{user.mention} has invited {total_invites} people.",
            color=nextcord.Color.blue()
        )
        embed.set_thumbnail(url=user.avatar.url)
        
        if active_invites:
            for invite in active_invites:
                embed.add_field(
                    name=f"Invite Code: {invite.code}",
                    value=f"Uses: {invite.uses}",
                    inline=False
                )
        else:
            embed.add_field(
                name="Active Invites",
                value="No active invite links.",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Invites(bot))