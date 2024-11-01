from utils.imports import *
from utils.token import TOKEN


intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
wish = commands.Bot(command_prefix="/", intents=intents)

for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        wish.load_extension(f'events.{filename[:-3]}')

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        wish.load_extension(f'commands.{filename[:-3]}')

@wish.event
async def on_ready():
    print(f'Wish is ready. Logged in as {wish.user.name} ({wish.user.id})')

    conn = sqlite3.connect('servers.db')
    c = conn.cursor()

    for guild in wish.guilds:
        server_id = str(guild.id)
        server_name = guild.name
        
        c.execute('SELECT role_logs_channel_id FROM servers WHERE server_id = ?', (server_id,))
        result = c.fetchone()
        
        if result is None:
            try:
                default_log_channel_id = None
                default_log_channel_name = None
                c.execute("""
                    INSERT INTO servers (
                        server_id, server_name, role_logs_channel_id, role_logs_channel_name, 
                        server_logs_channel_id, server_logs_channel_name, 
                        member_logs_channel_id, member_logs_channel_name, 
                        message_logs_channel_id, message_logs_channel_name, 
                        reaction_logs_channel_id, reaction_logs_channel_name, 
                        language
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'en_eu')
                """, (
                    server_id, server_name, 
                    default_log_channel_id, default_log_channel_name,
                    default_log_channel_id, default_log_channel_name,
                    default_log_channel_id, default_log_channel_name,
                    default_log_channel_id, default_log_channel_name,
                    default_log_channel_id, default_log_channel_name
                ))
                conn.commit()
            except Exception as e:
                print(f'Failed to add server log information for {server_name} ({server_id}): {e}')

    conn.close()
    server_count = len(wish.guilds)
    await wish.change_presence(activity=nextcord.Game(name=f"/help | {server_count} servers"))
    print('Server information check complete.')

wish.run(TOKEN)