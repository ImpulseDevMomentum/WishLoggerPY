from utils.imports import *
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, AuditLogAction, Embed, Color, User
from datetime import datetime

class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_audit_log_entries(self, guild, user_id, action):
        entries = []
        async for entry in guild.audit_logs(limit=None, action=action):
            if entry.target.id == user_id and not entry.user.bot:
                entries.append(entry)
        return entries

    def create_embed(self, user, entries, title, interaction_user):
        embed = Embed(
            title=f"<:browsefotor:1245656463163002982> {title} for {user.display_name} ({user.id})",
            color=Color.red(),
            timestamp=datetime.utcnow()
        )

        displayed_entries = entries[:25]
        for entry in displayed_entries:
            embed.add_field(
                name=f"<:Moderator:1247954371925512243> **Action by** {entry.user}",
                value=f"<:time:1247976543678894182> **Date:** {entry.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n<:reason:1247971720938258565> **Reason:** {entry.reason or 'No reason provided'}\n\u200b",
                inline=False
            )

        if len(entries) > 25:
            embed.add_field(
                name="More Records",
                value=f"And {len(entries) - 25} more entries...",
                inline=False
            )

        embed.set_footer(text=f"Requested by {interaction_user.display_name}", icon_url=interaction_user.avatar.url)
        return embed

    def create_summary_message(self, user, entries, action):
        return f"<:NotFine:1248352479599661056> {user.mention} has too many **{action}s.** They were {action}ed **{len(entries)} times.**"

    @nextcord.slash_command(name="ban-history", description="Shows the ban history of a user")
    async def ban_history(self, interaction: Interaction, user: User = SlashOption(name="user", description="Select the user")):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permissions to use this command.", ephemeral=True)
            return

        ban_entries = await self.get_audit_log_entries(interaction.guild, user.id, AuditLogAction.ban)

        if not ban_entries:
            await interaction.response.send_message(f"<:NotFine:1248352479599661056> No ban records found for {user.mention}.", ephemeral=True)
            return

        if len(ban_entries) > 25:
            message = self.create_summary_message(user, ban_entries, "ban")
            await interaction.response.send_message(message, ephemeral=True)
        else:
            embed = self.create_embed(user, ban_entries, "Ban History", interaction.user)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @nextcord.slash_command(name="kick-history", description="Shows the kick history of a user")
    async def kick_history(self, interaction: Interaction, user: User = SlashOption(name="user", description="Select the user")):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permissions to use this command.", ephemeral=True)
            return

        kick_entries = await self.get_audit_log_entries(interaction.guild, user.id, AuditLogAction.kick)

        if not kick_entries:
            await interaction.response.send_message(f"<:NotFine:1248352479599661056> No kick records found for {user.mention}.", ephemeral=True)
            return

        if len(kick_entries) > 25:
            message = self.create_summary_message(user, kick_entries, "kick")
            await interaction.response.send_message(message, ephemeral=True)
        else:
            embed = self.create_embed(user, kick_entries, "Kick History", interaction.user)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @nextcord.slash_command(name="mute-history", description="Shows the mute history of a user")
    async def timeout_history(self, interaction: Interaction, user: User = SlashOption(name="user", description="Select the user")):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permissions to use this command.", ephemeral=True)
            return

        timeout_entries = await self.get_audit_log_entries(interaction.guild, user.id, AuditLogAction.member_update)

        if not timeout_entries:
            await interaction.response.send_message(f"<:NotFine:1248352479599661056> No timeout records found for {user.mention}.", ephemeral=True)
            return

        if len(timeout_entries) > 25:
            message = self.create_summary_message(user, timeout_entries, "timeout")
            await interaction.response.send_message(message, ephemeral=True)
        else:
            embed = self.create_embed(user, timeout_entries, "Timeout History", interaction.user)
            await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(History(bot))