from utils.imports import *

class ModerationChangeWarnUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="uwarn", description="Change warning user for another user")
    async def change_warn_user(
        self,
        interaction: Interaction,
        member: nextcord.Member = SlashOption(description="Member whose warning user will be changed"),
        new_member: nextcord.Member = SlashOption(description="New member whose warning user will be changed"),
        case_id: int = SlashOption(description="Case ID of the warning to be changed"),
        reason: str = SlashOption(description="Reason of the warning to be changed")
    ):
        if interaction.user.guild_permissions.administrator or interaction.user == interaction.guild.owner:
            conn = sqlite3.connect('warns.db')
            c = conn.cursor()
            c.execute("UPDATE warns SET UserID = ? WHERE ServerID = ? AND UserID = ? AND CaseID = ? AND Reason = ?",
                    (new_member.id, interaction.guild.id, member.id, case_id, reason))
            conn.commit()

            if c.rowcount > 0:
                await interaction.response.send_message(f"<:Fine:1248352477502246932> Successfully changed user from **{member.display_name}** to **{new_member.display_name}** for warnings with reason **{reason}** ID: {case_id})", ephemeral=True)
                
                channel_log_id = load_member_logs_channel_id(interaction.guild.id)
                server_language = get_server_language(interaction.guild.id)
                language_file = f'language/{server_language}.json'

                with open(language_file, 'r') as file:
                    language_strings = json.load(file)
                if channel_log_id:
                    channel_log_id = interaction.guild.get_channel(int(channel_log_id))
                    embed_warn_logdecu = nextcord.Embed(title=language_strings.get("UWARN_TITLE"), color=nextcord.Color.dark_blue())
                    embed_warn_logdecu.add_field(name=language_strings.get("MODERATOR"), value=f"<@{interaction.user.id}>", inline=True)
                    embed_warn_logdecu.add_field(name=language_strings.get("MODERATOR_ID"), value=interaction.user.id, inline=True)
                    embed_warn_logdecu.add_field(name="", value="", inline=False)
                    embed_warn_logdecu.add_field(name=language_strings.get("USER"), value=f"<@{member.id}>", inline=True)
                    embed_warn_logdecu.add_field(name=language_strings.get("USER_ID"), value=member.id, inline=True)
                    embed_warn_logdecu.add_field(name="", value="", inline=False)
                    embed_warn_logdecu.add_field(name=language_strings.get("OLD"), value=f"<@{member.id}>", inline=True)
                    embed_warn_logdecu.add_field(name=language_strings.get("NEW"), value=f"<@{new_member.id}>", inline=True)
                    embed_warn_logdecu.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=False)

                    await channel_log_id.send(embed=embed_warn_logdecu)
            else:
                server_language = get_server_language(interaction.guild.id)
                language_file = f'language/{server_language}.json'

                with open(language_file, 'r') as file:
                    language_strings = json.load(file)
                await interaction.response.send_message(language_strings.get("NO_MATCHING_FOUND_ERROR"), ephemeral=True)

            conn.close()
        else:
            server_language = get_server_language(interaction.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)
            await interaction.response.send_message(language_strings.get("PERMISSIONS_DENIED"), ephemeral=True)

def setup(bot):
    bot.add_cog(ModerationChangeWarnUser(bot))