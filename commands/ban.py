from utils.imports import *

class ModerationBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="ban", description="Ban a user from the server")
    async def ban(
        self,
        interaction: Interaction,
        member: nextcord.Member = SlashOption(description="User who will be banned"),
        reason: str = SlashOption(description="Reason for banning the user", required=False),
        notify: bool = SlashOption(description="Notify the user about the ban", required=False, default=False)
    ):
        guild = interaction.guild
        bot_member = guild.get_member(self.bot.user.id)

        if Interaction.user == member:
            interaction.response.send_message("<:PermDenied:1248352895854973029> You can't ban yourself from this server.")

        if bot_member.top_role <= member.top_role:
            await interaction.response.send_message(f"<:NotFine:1248352479599661056> I can't ban {member.mention} because their role is higher or equal to mine", ephemeral=True)
            return


        if interaction.user.guild_permissions.ban_members or interaction.user.guild_permissions.administrator or interaction.user == interaction.guild.owner:
            await member.ban(reason=reason)
            if notify:
                embed = nextcord.Embed(
                    title="<:banned:1247971710150377523> You have been banned",
                    description=f"You have been banned from `{interaction.guild.name}`",
                    color=nextcord.Color.red()
                )
                if reason:
                    embed.add_field(name="<:reason:1247971720938258565> Reason", value=f"`{reason}`", inline=False)
                embed.set_footer(text="If you believe this is a mistake, please contact the server administrators.")

                try:
                    await member.send(embed=embed)
                except nextcord.HTTPException:
                    pass
            try:
                await interaction.response.send_message(f"<:Fine:1248352477502246932> {member} has been banned from the server for **{reason}**", ephemeral=True)
            except Exception:
                await interaction.response.send_message(f"<:NotFine:1248352479599661056> Failed to ban {member.mention}.", ephemeral=True)
        else:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permissions to this command.", ephemeral=True)

def setup(bot):
    bot.add_cog(ModerationBan(bot))