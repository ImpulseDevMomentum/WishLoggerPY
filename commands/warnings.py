from utils.imports import *

class ModerationWarnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="warnings", description="Show all warnings for the server")
    async def warnings(self, interaction: nextcord.Interaction):
        conn = sqlite3.connect('warns.db')
        c = conn.cursor()
        c.execute("SELECT UserID, Reason, CaseID FROM warns WHERE ServerID = ?", (interaction.guild.id,))
        warnings_data = c.fetchall()
        conn.close()

        if not warnings_data:
            await interaction.send("No warnings found for this server.", ephemeral=True)
            return

        max_embed_length = 4096
        embed_content = ""
        embeds = []
        embed = nextcord.Embed(title=f"<:Warns:1282061874594320426> Warnings for {interaction.guild.name}", color=nextcord.Color.dark_blue())
        
        for user_id, reason, case_id in warnings_data:
            member = interaction.guild.get_member(user_id)
            user_str = f"<:Member:1247954369639481498> {member} ({user_id})" if member else f"({user_id})"
            field_content = f"**<:ID:1247954367953240155> Case ID:** {case_id}\n**<:reason:1247971720938258565> Reason:** {reason}\n"
            
            if len(embed_content) + len(field_content) > max_embed_length:
                embed.add_field(name="", value=embed_content, inline=False)
                embeds.append(embed)
                embed = nextcord.Embed(title=f"<:Warns:1282061874594320426> Warnings for {interaction.guild.name} (Continued)", color=nextcord.Color.dark_blue())
                embed_content = field_content
            else:
                embed_content += f"**{user_str}**\n{field_content}"

        if embed_content:
            embed.add_field(name="Warnings", value=embed_content, inline=False)
            embeds.append(embed)

        for emb in embeds:
            await interaction.send(embed=emb, ephemeral=True)

def setup(bot):
    bot.add_cog(ModerationWarnings(bot))