from utils.imports import *

class ModerationWarnList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="warnlist", description="Show list of warnings for a user")
    async def warn_list(
        self, 
        interaction: nextcord.Interaction, 
        member: nextcord.Member = SlashOption(description="Member to check warnings", required=True)):
        conn = sqlite3.connect('warns.db')
        c = conn.cursor()
        c.execute("SELECT CaseID, Reason FROM warns WHERE ServerID = ? AND UserID = ?",
                  (interaction.guild.id, member.id))
        warnings = c.fetchall()
        conn.close()

        if not warnings:
            await interaction.send("<:NotFine:1248352479599661056> No warnings found for this user.", ephemeral=True)
            return

        max_embed_length = 4096
        embed_content = ""
        embeds = []
        embed = nextcord.Embed(title=f"<:Fine:1248352477502246932> Warnings for {member}", color=nextcord.Color.dark_blue())
        
        for index, (case_id, reason) in enumerate(warnings, start=1):
            warning_entry = f"**<:reportmessage0:1233828792368369694> Warning {index}**\n<:ID:1247954367953240155> Case ID: {case_id}\n<:reason:1247971720938258565> Reason: {reason}\n"
            
            if len(embed_content) + len(warning_entry) > max_embed_length:
                embed.add_field(name="Warnings", value=embed_content, inline=False)
                embeds.append(embed)
                embed = nextcord.Embed(title=f"<:Fine:1248352477502246932> Warnings for {member} (Continued)", color=nextcord.Color.dark_blue())
                embed_content = warning_entry
            else:
                embed_content += warning_entry

        if embed_content:
            embed.add_field(name="Warnings", value=embed_content, inline=False)
            embeds.append(embed)

        for emb in embeds:
            await interaction.send(embed=emb, ephemeral=True)

def setup(bot):
    bot.add_cog(ModerationWarnList(bot))