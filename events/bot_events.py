from utils.imports import *

class ServerEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: nextcord.Guild):
        server_id = guild.id
        server_name = guild.name
        language = "en_eu"
        
        role_logs_channel_id = None
        role_logs_channel_name = None
        server_logs_channel_id = None
        server_logs_channel_name = None
        member_logs_channel_id = None
        member_logs_channel_name = None
        message_logs_channel_id = None
        message_logs_channel_name = None
        reaction_logs_channel_id = None
        reaction_logs_channel_name = None

        conn = sqlite3.connect('servers.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO servers (
                server_id, server_name, role_logs_channel_id, role_logs_channel_name, 
                server_logs_channel_id, server_logs_channel_name, 
                member_logs_channel_id, member_logs_channel_name, 
                message_logs_channel_id, message_logs_channel_name, 
                reaction_logs_channel_id, reaction_logs_channel_name, 
                language
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            server_id, server_name, role_logs_channel_id, role_logs_channel_name, 
            server_logs_channel_id, server_logs_channel_name, 
            member_logs_channel_id, member_logs_channel_name, 
            message_logs_channel_id, message_logs_channel_name, 
            reaction_logs_channel_id, reaction_logs_channel_name, 
            language
        ))
        conn.commit()
        conn.close()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: nextcord.Guild):
        server_id = guild.id

        conn = sqlite3.connect('servers.db')
        c = conn.cursor()
        c.execute("""
            DELETE FROM servers WHERE server_id = ?
        """, (server_id,))
        conn.commit()
        conn.close()

def setup(bot):
    bot.add_cog(ServerEvents(bot))