from utils.imports import *
from datetime import timedelta
import humanfriendly

class ModerationTimeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="mute", description="Temporarily timeout a user")
    async def timeout(
        self,
        interaction: Interaction,
        member: nextcord.Member = SlashOption(description="User who will be muted"),
        time: str = SlashOption(description="Duration of mute (e.g., '1h', '2d')", required=True, default=None),
        reason: str = SlashOption(description="Reason for muting the user", required=False, default="No reason provided"),
        notify: bool = SlashOption(description="Notify the user about the mute", required=False, default=False)
    ):
        if interaction.user.guild_permissions.mute_members or interaction.user.guild_permissions.administrator or interaction.guild.owner == interaction.user:
            if member.top_role >= interaction.user.top_role:
                return await interaction.response.send_message("<:PermDenied:1248352895854973029> You cannot mute this user because they have a higher or equal role.", ephemeral=True)
            
            if member.guild_permissions.administrator or member == interaction.guild.owner:
                return await interaction.response.send_message("<:PermDenied:1248352895854973029> You cannot mute this user because they are an administrator or the owner.", ephemeral=True)

            try:
                if time:
                    time_seconds = humanfriendly.parse_timespan(time)
                    timeout_duration = timedelta(seconds=time_seconds)
                else:
                    timeout_duration = None
            except humanfriendly.InvalidTimespan as e:
                return await interaction.response.send_message(f"Invalid time format: {str(e)}", ephemeral=True)
            
            if timeout_duration:
                await member.edit(timeout=nextcord.utils.utcnow() + timeout_duration)
                duration_str = humanfriendly.format_timespan(time_seconds)
            else:
                await member.edit(timeout=None)
                duration_str = "indefinitely"
            
            await interaction.response.send_message(f"<:Fine:1248352477502246932> <@{member.id}> has been muted for {duration_str} because **{reason}**", ephemeral=True)

            if notify:
                embed = nextcord.Embed(
                    title="<:timeoutclock:1247969146038259783> You have been muted",
                    description=f"You have been muted in `{interaction.guild.name}`.",
                    color=nextcord.Color.red()
                )
                embed.add_field(name="<:reason:1247971720938258565> Reason", value=f"`{reason}`", inline=False)
                embed.set_footer(text="If you believe this is a mistake, please contact the server administrators.")

                if timeout_duration:
                    embed.add_field(name="<:time:1247976543678894182> Duration", value=f"`{duration_str}`", inline=False)

                try:
                    await member.send(embed=embed)
                except nextcord.HTTPException:
                    pass
        
        else:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permission to use this command.", ephemeral=True)

def setup(bot):
    bot.add_cog(ModerationTimeout(bot))