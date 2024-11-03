from utils.imports import *

class ModerationChangeWarnReason(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="chwarn", description="Change warning reason for a user")
    async def change_warn_reason(
        self,
        interaction: Interaction,
        member: nextcord.Member = SlashOption(description="Member whose warning reason will be changed"),
        case_id: int = SlashOption(description="Case ID of the warning to be changed"),
        new_reason: str = SlashOption(description="New reason for the warning")
    ):
        if interaction.user.guild_permissions.administrator or interaction.user == interaction.guild.owner:
            conn = sqlite3.connect('warns.db')
            c = conn.cursor()
            
            c.execute("SELECT Reason FROM warns WHERE ServerID = ? AND UserID = ? AND CaseID = ?", 
                      (interaction.guild.id, member.id, case_id))
            old_reason_row = c.fetchone()
            
            if old_reason_row:
                old_reason = old_reason_row[0]
                
                c.execute("UPDATE warns SET Reason = ? WHERE ServerID = ? AND UserID = ? AND CaseID = ?",
                          (new_reason, interaction.guild.id, member.id, case_id))
                conn.commit()
                
                if c.rowcount > 0:
                    await interaction.response.send_message(f"<:Fine:1248352477502246932> Successfully changed warning reason for ID **{case_id}** to **{new_reason}** for {member.mention}", ephemeral=True)

                    channel_log_id = load_member_logs_channel_id(interaction.guild.id)
                    server_language = get_server_language(interaction.guild.id)
                    language_file = f'language/{server_language}.json'

                    with open(language_file, 'r') as file:
                        language_strings = json.load(file)
                    
                    if channel_log_id:
                        channel_log_id = interaction.guild.get_channel(int(channel_log_id))
                        embed_warn_logdec = nextcord.Embed(title=language_strings.get("CHWARN_TITLE"), color=nextcord.Color.dark_blue())
                        embed_warn_logdec.add_field(name=language_strings.get("MODERATOR"), value=f"<@{interaction.user.id}>", inline=True)
                        embed_warn_logdec.add_field(name=language_strings.get("MODERATOR_ID"), value=interaction.user.id, inline=True)
                        embed_warn_logdec.add_field(name="", value="", inline=False)
                        embed_warn_logdec.add_field(name=language_strings.get("USER"), value=f"<@{member.id}>", inline=True)
                        embed_warn_logdec.add_field(name=language_strings.get("USER_ID"), value=member.id, inline=True)
                        embed_warn_logdec.add_field(name="", value="", inline=False)
                        embed_warn_logdec.add_field(name=language_strings.get("OLD"), value=old_reason, inline=True)
                        embed_warn_logdec.add_field(name=language_strings.get("NEW"), value=new_reason, inline=True)
                        embed_warn_logdec.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=False)

                        await channel_log_id.send(embed=embed_warn_logdec)
                else:
                    await interaction.response.send_message(f"<:NotFine:1248352479599661056> No matching warnings found for the specified user and case ID **{case_id}**.", ephemeral=True)
            else:
                await interaction.response.send_message(f"<:NotFine:1248352479599661056> No matching warnings found for the specified user and case ID **{case_id}**.", ephemeral=True)
            
            conn.close()
        else:
            server_language = get_server_language(interaction.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)
            await interaction.response.send_message(language_strings.get("PERMISSIONS_DENIED"), ephemeral=True)

def setup(bot):
    bot.add_cog(ModerationChangeWarnReason(bot))
