from utils.imports import *

def update_log_channel(server_id, server_name, log_type, channel_log_id, channel_log_name):
    conn = sqlite3.connect('servers.db')
    c = conn.cursor()

    if log_type == "Role Logs":
        c.execute('''
            UPDATE servers SET
            role_logs_channel_id = ?, role_logs_channel_name = ?,
            server_name = ?
            WHERE server_id = ?
        ''', (channel_log_id, channel_log_name, server_name, server_id))
    elif log_type == "Server Logs":
        c.execute('''
            UPDATE servers SET
            server_logs_channel_id = ?, server_logs_channel_name = ?,
            server_name = ?
            WHERE server_id = ?
        ''', (channel_log_id, channel_log_name, server_name, server_id))
    elif log_type == "Member Logs":
        c.execute('''
            UPDATE servers SET
            member_logs_channel_id = ?, member_logs_channel_name = ?,
            server_name = ?
            WHERE server_id = ?
        ''', (channel_log_id, channel_log_name, server_name, server_id))
    elif log_type == "Message Logs":
        c.execute('''
            UPDATE servers SET
            message_logs_channel_id = ?, message_logs_channel_name = ?,
            server_name = ?
            WHERE server_id = ?
        ''', (channel_log_id, channel_log_name, server_name, server_id))
    elif log_type == "Reaction Logs":
        c.execute('''
            UPDATE servers SET
            reaction_logs_channel_id = ?, reaction_logs_channel_name = ?,
            server_name = ?
            WHERE server_id = ?
        ''', (channel_log_id, channel_log_name, server_name, server_id))
    else:
        c.execute('''
            UPDATE servers SET
            role_logs_channel_id = ?, role_logs_channel_name = ?,
            server_logs_channel_id = ?, server_logs_channel_name = ?,
            member_logs_channel_id = ?, member_logs_channel_name = ?,
            message_logs_channel_id = ?, message_logs_channel_name = ?,
            reaction_logs_channel_id = ?, reaction_logs_channel_name = ?,
            server_name = ?
            WHERE server_id = ?
        ''', (
            channel_log_id, channel_log_name,
            channel_log_id, channel_log_name,
            channel_log_id, channel_log_name,
            channel_log_id, channel_log_name,
            channel_log_id, channel_log_name,
            server_name, server_id
        ))

    conn.commit()
    conn.close()



class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="setlogging", description="Set the logging channel")
    async def setlogging(self, interaction: Interaction, 
                         channel: nextcord.TextChannel = SlashOption(description="Select a channel for logging"),
                         log_type: str = SlashOption(description="Select log type", choices=["All Logs", "Role Logs", "Server Logs", "Member Logs", "Message Logs", "Reaction Logs"], required=False)):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permissions to this command.", ephemeral=True)
            return

        server_id = interaction.guild.id
        server_name = interaction.guild.name
        channel_log_id = channel.id
        channel_log_name = channel.name

        if log_type:
            update_log_channel(server_id, server_name, log_type, channel_log_id, channel_log_name)
        else:
            update_log_channel(server_id, server_name, "All Logs", channel_log_id, channel_log_name)

        await interaction.response.send_message(f"Logging channel for {log_type or 'All Logs'} has been set to {channel.mention}", ephemeral=True)

def setup(bot):
    bot.add_cog(Logging(bot))
