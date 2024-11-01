from utils.imports import *

class ModerationDelWarn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="delwarn", description="Delete a warning for a specific user")
    async def del_warn(
        self,
        interaction: Interaction,
        member: nextcord.Member = nextcord.SlashOption(
            description="The member whose warning you want to delete",
            required=True
        ),
        case_id: int = nextcord.SlashOption(
            description="The ID of the warning case to delete",
            required=True
        ),
        reason: str = nextcord.SlashOption(
            description="The reason for deleting the warning",
            required=False,
            default="**No reason provided**"
        )
    ):
        if interaction.user.guild_permissions.administrator or interaction.user == interaction.guild.owner:
            server_language = get_server_language(interaction.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)

            conn = sqlite3.connect('warns.db')
            c = conn.cursor()
            
            c.execute("SELECT * FROM warns WHERE ServerID = ? AND UserID = ? AND CaseID = ?",
                      (interaction.guild.id, member.id, case_id))
            result = c.fetchone()
            
            if result:
                c.execute("DELETE FROM warns WHERE ServerID = ? AND UserID = ? AND CaseID = ?",
                          (interaction.guild.id, member.id, case_id))
                conn.commit()
                conn.close()

                await interaction.response.send_message(f"<:Fine:1248352477502246932> Warning with ID **{case_id}** for {member.mention} has been deleted.", ephemeral=True)
                
                channel_log_id = load_member_logs_channel_id(interaction.guild.id)

                if channel_log_id:
                    channel_log_id = interaction.guild.get_channel(int(channel_log_id))
                    embed_warn_logde = nextcord.Embed(title=language_strings.get("WARN_DELETED_TITLE"), color=nextcord.Color.dark_blue())
                    embed_warn_logde.add_field(name=language_strings.get("MODERATOR"), value=f"<@{interaction.user.id}>", inline=True)
                    embed_warn_logde.add_field(name=language_strings.get("MODERATOR_ID"), value=interaction.user.id, inline=True)
                    embed_warn_logde.add_field(name="", value="", inline=False)
                    embed_warn_logde.add_field(name=language_strings.get("USER"), value=f"<@{member.id}>", inline=True)
                    embed_warn_logde.add_field(name=language_strings.get("USER_ID"), value=member.id, inline=True)
                    embed_warn_logde.add_field(name=language_strings.get("REASON"), value=reason, inline=False)
                    embed_warn_logde.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)

                    await channel_log_id.send(embed=embed_warn_logde)
                    
            else:
                await interaction.response.send_message(language_strings.get("SPEC_USER_OR_CASE_NOT_FOUND_ERR"), ephemeral=True)
        else:
            await interaction.response.send_message(language_strings.get("PERMISSIONS_DENIED"), ephemeral=True)

def setup(bot):
    bot.add_cog(ModerationDelWarn(bot))
