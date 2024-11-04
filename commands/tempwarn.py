from utils.imports import *

def add_warn(server_id, user_id, reason, temp, case_id):
    conn = sqlite3.connect('warns.db')
    c = conn.cursor()
    c.execute("INSERT INTO warns (CaseID, ServerID, UserID, Reason, Temp) VALUES (?, ?, ?, ?, ?)",
              (case_id, server_id, user_id, reason, temp))
    conn.commit()
    conn.close()

def remove_warn(case_id):
    conn = sqlite3.connect('warns.db')
    c = conn.cursor()
    c.execute("DELETE FROM warns WHERE CaseID=?", (case_id,))
    conn.commit()
    conn.close()

def generate_unique_case_id():
    while True:
        case_id = generate_case_id()
        conn = sqlite3.connect('warns.db')
        c = conn.cursor()
        c.execute("SELECT * FROM warns WHERE CaseID=?", (case_id,))
        if not c.fetchone():
            conn.close()
            return case_id
        conn.close()

def generate_case_id():
    return random.randint(100000, 99999)

def parse_duration(duration_str):
    units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    match = re.match(r'(\d+)([smhd])$', duration_str)
    if match:
        value, unit = match.groups()
        return int(value) * units[unit]
    return None

async def schedule_warn_removal(case_id, duration, interaction, member, reason, start_time):
    await asyncio.sleep(duration)
    remove_warn(case_id)
    await send_warn_deleted_log(interaction, member, reason, start_time, duration)

async def send_warn_deleted_log(interaction, member, reason, start_time, duration):
    end_time = str(start_time) + str(duration)
    embed_warn_deleted_log = nextcord.Embed(title="<:None0:1233827940895166655> Temporary Warn Deleted", color=nextcord.Color.red())
    embed_warn_deleted_log.add_field(name="<:Moderator:1247954371925512243> **Moderator**", value=f"<@{interaction.user.id}>", inline=False)
    embed_warn_deleted_log.add_field(name="<:ID:1247954367953240155> **Moderator ID**", value=interaction.user.id, inline=False)
    embed_warn_deleted_log.add_field(name="<:Member:1247954369639481498> **User**", value=f"<@{member.id}>", inline=False)
    embed_warn_deleted_log.add_field(name="<:ID:1247954367953240155> **User ID**", value=member.id, inline=False)
    embed_warn_deleted_log.add_field(name="<:reason:1247971720938258565> **Reason**", value=reason if reason else "No reason provided", inline=False)
    embed_warn_deleted_log.add_field(name="<:time:1247976543678894182> **Duration**", value=format_duration(duration), inline=False)
    embed_warn_deleted_log.add_field(name="<:time:1247976543678894182> **Today at**", value=current_datetime(), inline=True)

    channel_log_id = load_member_logs_channel_id(interaction.guild.id)
    if channel_log_id:
        channel_log_id = interaction.guild.get_channel(int(channel_log_id))
        await channel_log_id.send(embed=embed_warn_deleted_log)

def format_duration(duration):
    days, remainder = divmod(duration, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

class TempWarnButton(nextcord.ui.Button):
    def __init__(self, member, reason, case_id, duration, interaction):
        super().__init__(label="Temp Warn without logging", style=nextcord.ButtonStyle.danger, emoji="<:NotFine:1248352479599661056>")
        self.member = member
        self.reason = reason
        self.case_id = case_id
        self.duration = duration
        self.interaction = interaction

    async def callback(self, interaction: nextcord.Interaction):
        server_id = interaction.guild.id
        user_id = self.member.id
        add_warn(server_id, user_id, self.reason, True, self.case_id)
        start_time = interaction.created_at

        asyncio.create_task(schedule_warn_removal(self.case_id, self.duration, interaction, self.member, self.reason, start_time))

        self.disabled = True
        await interaction.response.edit_message(view=self.view)
        await interaction.followup.send(f'<:Fine:1248352477502246932> {self.member.mention} has been temporarily warned for **{self.reason}** with Case ID: {self.case_id}', ephemeral=True)

class TempWarn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="tempwarn", description="Temporarily warn user")
    async def tempwarn(self, interaction: Interaction, member: nextcord.Member, duration: str, *, reason=None):
        if interaction.user.guild_permissions.administrator or interaction.user == interaction.guild.owner or interaction.user.guild_permissions.manage_messages:
            server_id = interaction.guild.id
            user_id = member.id
            case_id = generate_unique_case_id()
            duration_seconds = parse_duration(duration)
            
            if duration_seconds is None or duration_seconds > 172800:
                await interaction.response.send_message("<:PermDenied:1248352895854973029> Invalid duration. Please specify a duration of up to 2 days.", ephemeral=True)
                return

            channel_log_id = load_member_logs_channel_id(interaction.guild.id)
            
            if channel_log_id:
                embed_warn_log = nextcord.Embed(title="<:SUSSY:1247976542471061667> User Temporarily Warned", color=nextcord.Color.dark_blue())
                embed_warn_log.add_field(name="<:ID:1247954367953240155> **Warn ID**", value=case_id, inline=False)
                embed_warn_log.add_field(name="<:Moderator:1247954371925512243> **Moderator**", value=f"<@{interaction.user.id}>", inline=False)
                embed_warn_log.add_field(name="<:ID:1247954367953240155> **Moderator ID**", value=interaction.user.id, inline=False)
                embed_warn_log.add_field(name="<:Member:1247954369639481498> **User**", value=f"<@{member.id}>", inline=False)
                embed_warn_log.add_field(name="<:ID:1247954367953240155> **User ID**", value=member.id, inline=False)
                embed_warn_log.add_field(name="<:reason:1247971720938258565> **Reason**", value=reason, inline=False)
                embed_warn_log.add_field(name="<:time:1247976543678894182> **Duration**", value=duration, inline=False)
                embed_warn_log.add_field(name="<:time:1247976543678894182> **Today at**", value=current_datetime(), inline=True)

                channel_log_id = interaction.guild.get_channel(int(channel_log_id))
                await channel_log_id.send(embed=embed_warn_log)

                add_warn(server_id, user_id, reason, True, case_id)
                start_time = interaction.created_at
                asyncio.create_task(schedule_warn_removal(case_id, duration_seconds, interaction, member, reason, start_time))
            else:
                embed_no_log_channel = nextcord.Embed(title="<:NotFine:1248352479599661056> Logging Channel Not Set", color=nextcord.Color.orange())
                embed_no_log_channel.add_field(name="Notice", value="Hey! You haven't set a logging channel. Without it, information about warns is limited. Please set your channel via `/setlogging` command!", inline=False)
                view = nextcord.ui.View(timeout=None)
                view.add_item(TempWarnButton(member, reason, case_id, duration_seconds, interaction))

                await interaction.response.send_message(embed=embed_no_log_channel, view=view, ephemeral=True)
                return

            await interaction.response.send_message(f'<:Fine:1248352477502246932> {member.mention} has been temporarily warned for **{reason}** for {duration} with Case ID: {case_id}', ephemeral=True)
        else:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You do not have permission to use this command.", ephemeral=True)

def setup(bot):
    bot.add_cog(TempWarn(bot))
