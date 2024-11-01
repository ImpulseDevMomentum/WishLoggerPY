from utils.imports import *

class ModerationKick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="kick", description="Kick a user from the server")
    async def kick(
        self,
        interaction: Interaction,
        member: nextcord.Member = SlashOption(description="User who will be kicked"),
        reason: str = SlashOption(description="Reason for kicking the user", required=False),
        notify: bool = SlashOption(description="Notify the user about the kick", required=False, default=False)
    ):
        if interaction.user.guild_permissions.kick_members or interaction.user.guild_permissions.administrator or interaction.user == interaction.guild.owner:
            await member.kick(reason=reason)
            if notify:
                embed = nextcord.Embed(
                    title="<:SUSSY:1247976542471061667> You have been Kicked",
                    description=f"You have been kicked from `{interaction.guild.name}`",
                    color=nextcord.Color.red()
                )
                if reason:
                    embed.add_field(name="<:reason:1247971720938258565> Reason", value=f"`{reason}`", inline=False)
                embed.set_footer(text="If you believe this is a mistake, please contact the server administrators.")

                try:
                    await member.send(embed=embed)
                except nextcord.HTTPException:
                    pass

            await interaction.response.send_message(f"<:Fine:1248352477502246932> {member} has been kicked from the server for **{reason}**", ephemeral=True)
        else:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permissions to this command.**.", ephemeral=True)

def setup(bot):
    bot.add_cog(ModerationKick(bot))