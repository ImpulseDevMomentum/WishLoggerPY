from utils.imports import *
import nextcord
from nextcord.ext import commands
import sqlite3

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="config", description="Configuration commands group")
    async def config(self, interaction: nextcord.Interaction):
        pass

    @config.subcommand(name="info", description="Show the current configuration")
    async def info(self, interaction: nextcord.Interaction):
        if interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> Only the server **owner** can view the configuration.", ephemeral=True)
            return
        server_id = str(interaction.guild.id)
        conn = sqlite3.connect('servers.db')
        c = conn.cursor()
        c.execute('SELECT * FROM servers WHERE server_id = ?', (server_id,))
        result = c.fetchone()
        conn.close()

        if result:
            embed = nextcord.Embed(title="Server Configuration", color=nextcord.Color.blue())
            embed.add_field(name="Server ID", value=result[0], inline=False)
            embed.add_field(name="Server Name", value=result[1], inline=False)
            embed.add_field(name="Role Logs Channel ID", value=result[2], inline=False)
            embed.add_field(name="Role Logs Channel Name", value=result[3], inline=True)
            embed.add_field(name="Server Logs Channel ID", value=result[4], inline=False)
            embed.add_field(name="Server Logs Channel Name", value=result[5], inline=True)
            embed.add_field(name="Member Logs Channel ID", value=result[6], inline=False)
            embed.add_field(name="Member Logs Channel Name", value=result[7], inline=True)
            embed.add_field(name="Message Logs Channel ID", value=result[8], inline=False)
            embed.add_field(name="Message Logs Channel Name", value=result[9], inline=True)
            embed.add_field(name="Reaction Logs Channel ID", value=result[10], inline=False)
            embed.add_field(name="Reaction Logs Channel Name", value=result[11], inline=True)
            embed.add_field(name="Language", value=result[12], inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("<:NotFine:1248352479599661056> No configuration found for this server.", ephemeral=True)

    @config.subcommand(name="reset", description="Reset the current configuration")
    async def reset(self, interaction: nextcord.Interaction):
        if interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> Only the server **owner** can reset the configuration.", ephemeral=True)
            return

        embed = nextcord.Embed(
            title="Warning",
            description="<:Warning:1248654084500885526> You are about to reset your server configuration. Logs, channels, cache, and other configs will be set to default. Are you sure you want to proceed?",
            color=nextcord.Color.red()
        )
        button = nextcord.ui.Button(label="Reset Configuration", style=nextcord.ButtonStyle.danger)

        async def button_callback(interaction):
            if interaction.user.id != interaction.guild.owner_id:
                await interaction.response.send_message("<:PermDenied:1248352895854973029> Only the server **owner** can reset the configuration.", ephemeral=True)
                return

            server_id = str(interaction.guild.id)
            conn = sqlite3.connect('servers.db')
            c = conn.cursor()
            c.execute("""
                UPDATE servers SET
                    role_logs_channel_id = NULL,
                    role_logs_channel_name = NULL,
                    server_logs_channel_id = NULL,
                    server_logs_channel_name = NULL,
                    member_logs_channel_id = NULL,
                    member_logs_channel_name = NULL,
                    message_logs_channel_id = NULL,
                    message_logs_channel_name = NULL,
                    reaction_logs_channel_id = NULL,
                    reaction_logs_channel_name = NULL,
                    language = 'en_eu'
                WHERE server_id = ?
            """, (server_id,))
            conn.commit()
            conn.close()
            await interaction.response.send_message("<:Fine:1248352477502246932> Configuration has been reset.", ephemeral=True)

        button.callback = button_callback
        view = nextcord.ui.View()
        view.add_item(button)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

def setup(bot):
    bot.add_cog(Config(bot))