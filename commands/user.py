from utils.imports import *
import sqlite3
from datetime import datetime, timezone

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def check_audit_logs(self, guild, user_id, action_type):
        async for entry in guild.audit_logs(action=action_type, limit=100):
            if entry.target.id == user_id:
                return True
        return False

    async def check_warns(self, user_id):
        conn = sqlite3.connect("warns.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM warns WHERE UserID = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    async def check_suspicious(self, member):
        now = datetime.now(timezone.utc)
        account_age = (now - member.created_at).days
        has_default_avatar = member.avatar is None
        
        is_new_account = account_age < 3
        is_suspicious = is_new_account or has_default_avatar
        
        return is_suspicious

    @nextcord.slash_command(name="user", description="Check info about users")
    async def user(self, interaction: nextcord.Interaction, member: nextcord.Member = None):
        if member is None:
            member = interaction.user

        guild = interaction.guild
        user_name = member.name
        user_id = member.id
        user_roles = [f"<@&{role.id}>" for role in member.roles if role.name != '@everyone']

        user_flags = [
            "<:HypeSquad20:1234084736826347570>" if member.public_flags.hypesquad_brilliance else "",
            "<:HypeSquad10:1234084738550071326>" if member.public_flags.hypesquad_balance else "",
            "<:HypeSquad00:1234084739921608784>" if member.public_flags.hypesquad_bravery else "",
            "<:ActiveDev0:1234084733986799668>" if member.public_flags.active_developer else "",
            "<:EarlyDev0:1234084744635875338>" if member.public_flags.early_verified_bot_developer else "",
            "<:Partner0:1234084741125247028>" if member.public_flags.partner else "",
            "<:Booster2:1261343522188169227>" if interaction.guild.premium_subscribers and member in interaction.guild.premium_subscribers else "",
            "<:Owner0:1234084745932177428>" if interaction.guild.owner_id == member.id else "",
            "<:DiscordStaff:1261343775255433237>" if member.public_flags.discord_certified_moderator else "",
            "<:discordapp0:1234105198956515361>" if member.bot and not member.public_flags.verified_bot else "",
            "<:verifiedapp0:1234105200411938938>" if member.bot and member.public_flags.verified_bot else "",
        ]

        now = datetime.now(timezone.utc)
        account_created_at = member.created_at.strftime('%B %d, %Y')
        join_date = member.joined_at.strftime('%B %d, %Y')
        
        account_age = now - member.created_at
        join_age = now - member.joined_at
        
        account_age_str = format_timedelta(account_age)
        join_age_str = format_timedelta(join_age)
        
        highest_role = member.top_role
        highest_role_mention = f"<@&{highest_role.id}>"
        highest_role_color = highest_role.color

        user_avatar_url = member.avatar.url if hasattr(member.avatar, 'url') else member.default_avatar.url

        user_info_embed = nextcord.Embed(title='<:Member:1247954369639481498> Member Information Card', color=highest_role_color)
        user_info_embed.set_thumbnail(url=user_avatar_url)
        user_info_embed.add_field(name='<:browsefotor:1245656463163002982> **Displayed Username**', value=user_name, inline=False)
        user_info_embed.add_field(name='<:ID:1247954367953240155> **User ID**', value=user_id, inline=False)
        user_info_embed.add_field(name='<:info:1247959011605741579> **User roles**', value=' '.join(user_roles), inline=False)
        user_info_embed.add_field(name='<:info:1247959011605741579> **Highest role**', value=highest_role_mention, inline=False)

        user_badges = ' '.join(flag for flag in user_flags if flag)
        user_info_embed.add_field(name='<:info:1247959011605741579> **User Badges**', value=user_badges if user_badges else "No badges", inline=False)
        user_info_embed.add_field(name=' <:time:1247976543678894182> **Joined Discord**', value=f'{account_created_at} ({account_age_str})', inline=False)
        user_info_embed.add_field(name='<:time:1247976543678894182> **Joined the server**', value=f'{join_date} ({join_age_str})', inline=False)

        was_banned = await self.check_audit_logs(guild, user_id, nextcord.AuditLogAction.ban)
        was_kicked = await self.check_audit_logs(guild, user_id, nextcord.AuditLogAction.kick)
        was_muted = await self.check_audit_logs(guild, user_id, nextcord.AuditLogAction.member_update)
        was_warned = await self.check_warns(user_id)
        is_suspicious = await self.check_suspicious(member)

        security_icon = "<:SecuritySafe:1294266337199259700>" if not (was_banned or was_kicked or was_muted or was_warned or is_suspicious) else "<:SecuritySuspicius:1294266339015266396>"
        security_embed_color = nextcord.Color.red() if (was_banned or was_kicked or was_muted or was_warned or is_suspicious) else nextcord.Color.green()

        security_embed = nextcord.Embed(title=f"{security_icon} Security Actions", color=security_embed_color)
        security_embed.set_thumbnail(url=user_avatar_url)
        security_embed.add_field(name='<:browsefotor:1245656463163002982> **Displayed Username**', value=user_name, inline=False)
        security_embed.add_field(name='<:ID:1247954367953240155> **User ID**', value=user_id, inline=False)
        security_embed.add_field(name="<:banned:1247971710150377523> Was Ever Banned?", value="<:Enabled:1248656166498730095> **Yes**" if was_banned else "<:Disabled:1248656164342988832> No", inline=True)
        security_embed.add_field(name="<:Kicked:1294264935001493555> Was Ever Kicked?", value="<:Enabled:1248656166498730095> **Yes**" if was_kicked else "<:Disabled:1248656164342988832> No", inline=True)
        security_embed.add_field(name="<:Muted:1247967288360173650> Was Ever Muted?", value="<:Enabled:1248656166498730095> **Yes**" if was_muted else "<:Disabled:1248656164342988832> No", inline=True)
        security_embed.add_field(name="<:WarnDeleted:1282056935549436009> Was Ever Warned?", value="<:Enabled:1248656166498730095> **Yes**" if was_warned else "<:Disabled:1248656164342988832> No", inline=True)
        security_embed.add_field(name="<:reportmessage0:1233828792368369694> Account is New", value="<:Enabled:1248656166498730095> **Yes**" if (datetime.now(timezone.utc) - member.created_at).days < 3 else "<:Disabled:1248656164342988832> No", inline=True)
        security_embed.add_field(name="<:reportmessage0:1233828792368369694> No Profile Picture", value="<:Enabled:1248656166498730095> **Yes**" if member.avatar is None else "<:Disabled:1248656164342988832> No", inline=True)
        security_embed.add_field(name="<:SUSSY:1247976542471061667> Suspicious Account", value="<:Enabled:1248656166498730095> **Yes**" if is_suspicious else "<:Disabled:1248656164342988832> No", inline=True)

        async def update_view(selected: str):
            view = nextcord.ui.View(timeout=None)

            user_info_button = nextcord.ui.Button(style=nextcord.ButtonStyle.green if selected == "user_info" else nextcord.ButtonStyle.gray, label="User Information", custom_id="user_info_button")
            async def user_info_callback(interaction: nextcord.Interaction):
                await interaction.response.edit_message(embed=user_info_embed, view=await update_view("user_info"))

            user_info_button.callback = user_info_callback
            view.add_item(user_info_button)

            security_actions_button = nextcord.ui.Button(style=nextcord.ButtonStyle.green if selected == "security_actions" else nextcord.ButtonStyle.gray, label="Security Actions", custom_id="security_actions_button")
            async def security_actions_callback(interaction: nextcord.Interaction):
                await interaction.response.edit_message(embed=security_embed, view=await update_view("security_actions"))

            security_actions_button.callback = security_actions_callback
            view.add_item(security_actions_button)

            can_ban = interaction.user.guild_permissions.ban_members or interaction.guild.owner_id == interaction.user.id or interaction.user.guild_permissions.administrator
            can_kick = interaction.user.guild_permissions.kick_members or interaction.guild.owner_id == interaction.user.id or interaction.user.guild_permissions.administrator

            ban_button = nextcord.ui.Button(style=nextcord.ButtonStyle.gray, label="Ban", custom_id="ban_button", disabled=selected != "security_actions" or not can_ban, emoji="<:banned:1247971710150377523>")
            kick_button = nextcord.ui.Button(style=nextcord.ButtonStyle.gray, label="Kick", custom_id="kick_button", disabled=selected != "security_actions" or not can_kick, emoji="<:Kicked:1294264935001493555>")

            async def ban_callback(interaction: nextcord.Interaction):
                if can_ban:
                    await member.ban(reason="Banned via slash security actions")
                    await interaction.response.send_message(f"<:Fine:1248352477502246932> {member.mention} has been banned.", ephemeral=True)
                else:
                    await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permission to ban members.", ephemeral=True)

            async def kick_callback(interaction: nextcord.Interaction):
                if can_kick:
                    await member.kick(reason="Kicked via security actions")
                    await interaction.response.send_message(f"<:Fine:1248352477502246932> {member.mention} has been kicked.", ephemeral=True)
                else:
                    await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permission to kick members.", ephemeral=True)

            ban_button.callback = ban_callback
            kick_button.callback = kick_callback

            view.add_item(ban_button)
            view.add_item(kick_button)

            return view

        await interaction.response.send_message(embed=user_info_embed, view=await update_view("user_info"), ephemeral=True)

def setup(bot):
    bot.add_cog(User(bot))