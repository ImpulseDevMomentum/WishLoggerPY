from utils.imports import *

###############################################

def add_warn(server_id, user_id, reason, temp, case_id):
    conn = sqlite3.connect('warns.db')
    c = conn.cursor()
    c.execute("INSERT INTO warns (CaseID, ServerID, UserID, Reason, Temp) VALUES (?, ?, ?, ?, ?)",
              (case_id, server_id, user_id, reason, temp))
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
    return random.randint(100000, 999999)

#############################################

class WarnButton(nextcord.ui.Button):
    def __init__(self, member, reason, case_id):
        super().__init__(label="Warn without logging", style=nextcord.ButtonStyle.danger, emoji="<:NotFine:1248352479599661056>")
        self.member = member
        self.reason = reason
        self.case_id = case_id

    async def callback(self, interaction: nextcord.Interaction):
        server_id = interaction.guild.id
        user_id = self.member.id
        add_warn(server_id, user_id, self.reason, False, self.case_id)

        self.disabled = True
        await interaction.response.edit_message(view=self.view)
        
        await interaction.followup.send(f'<:Fine:1248352477502246932> {self.member.mention} has been warned for **{self.reason}** with Case ID: {self.case_id}', ephemeral=True)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="warn", description="Warn user from server")
    async def warn(self, interaction: Interaction, member: nextcord.Member, *, reason=None):
        if interaction.user.guild_permissions.administrator or interaction.user == interaction.guild.owner or interaction.user.guild_permissions.manage_messages:
            server_id = interaction.guild.id
            user_id = member.id
            case_id = generate_unique_case_id()

            amount_of_letters_in_reason = len(reason)

            channel_log_id = load_member_logs_channel_id(interaction.guild.id)

            server_language = get_server_language(interaction.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)

            if amount_of_letters_in_reason > 720:
                await interaction.response.send_message(f"<:NotFine:1248352479599661056> You can't use more than __720__ letters and symbols in the reason field.", ephemeral=True)
                return
                

            
            if channel_log_id:
                embed_warn_log = nextcord.Embed(title=language_strings.get("WARN_TITLE"), color=nextcord.Color.dark_blue())
                embed_warn_log.add_field(name=language_strings.get("WARN_ID"), value=case_id, inline=False)
                embed_warn_log.add_field(name=language_strings.get("MODERATOR"), value=f"<@{interaction.user.id}>", inline=True)
                embed_warn_log.add_field(name=language_strings.get("MODERATOR_ID"), value=interaction.user.id, inline=True)
                embed_warn_log.add_field(name="", value="", inline=False)
                embed_warn_log.add_field(name=language_strings.get("USER"), value=f"<@{member.id}>", inline=True)
                embed_warn_log.add_field(name=language_strings.get("USER_ID"), value=member.id, inline=True)
                embed_warn_log.add_field(name=language_strings.get("REASON"), value=reason, inline=False)
                embed_warn_log.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                channel_log_id = interaction.guild.get_channel(int(channel_log_id))
                await channel_log_id.send(embed=embed_warn_log)

                add_warn(server_id, user_id, reason, False, case_id)
            else:
                embed_no_log_channel = nextcord.Embed(title=language_strings.get("WARN_CHANNEL_NOT_SET_TITLE"), color=nextcord.Color.orange())
                embed_no_log_channel.add_field(name=language_strings.get("NOTICE"), value=language_strings.get("EMBED_NO_LOG_VALUE"), inline=False)
                view = nextcord.ui.View(timeout=None)
                view.add_item(WarnButton(member, reason, case_id))

                await interaction.response.send_message(embed=embed_no_log_channel, view=view, ephemeral=True)
                return

            await interaction.response.send_message(f'<:Fine:1248352477502246932> {member.mention} has been warned for **{reason}** with Case ID: {case_id}', ephemeral=True)
        else:
            server_language = get_server_language(interaction.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)
            await interaction.response.send_message(language_strings.get("PERMISSIONS_DENIED"), ephemeral=True)

def setup(bot):
    bot.add_cog(Moderation(bot))