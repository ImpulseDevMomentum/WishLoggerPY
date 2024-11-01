from utils.imports import *

class ModerationUnmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @wish.slash_command(name="unmute", description="Remove timeout from user")
    async def rtimeout(
        self,
        interaction: Interaction,
        member: nextcord.Member = SlashOption(description="User who will be unmuted"),
        reason: str = SlashOption(description="Reason for unmuting the user", required=False, default=None),
    ):
        if interaction.user.guild_permissions.mute_members or interaction.user.guild_permissions.administrator or interaction.guild.owner == interaction.user:
            if member.top_role >= interaction.user.top_role:
                return await interaction.response.send_message("<:PermDenied:1248352895854973029> You cannot unmute this user because they have a higher or equal role.", ephemeral=True)
            if member.guild_permissions.administrator or member == interaction.guild.owner:
                return await interaction.response.send_message("<:PermDenied:1248352895854973029> You cannot unmute this user because they are an administrator or the owner.", ephemeral=True)

            await member.edit(timeout=None)

            if reason is None:
                reason = "No reason provided"

            await interaction.response.send_message(f"<:Fine:1248352477502246932> <@{member.id}> has been unmuted because **{reason}**", ephemeral=True)
        
        else:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permissions to use this command.", ephemeral=True)
def setup(bot):
    bot.add_cog(ModerationUnmute(bot))