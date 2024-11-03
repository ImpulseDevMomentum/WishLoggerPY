import nextcord, datetime, json, asyncio, time, random, humanfriendly, re, pytz, os
from nextcord import Integration, Interaction, slash_command, SlashOption, ChannelType
from nextcord.ext import commands, tasks
from nextcord.utils import format_dt
from nextcord.ext.commands import Bot, Context
from nextcord.ui import View
import sqlite3
from datetime import datetime, timezone, timedelta
from typing import List, Tuple
client = nextcord.Client()
intents = nextcord.Intents.default()
intents = nextcord.Intents().all()
wish = commands.Bot(command_prefix="/", intents=intents)


########################################################################################################################################

def load_role_logs_channel_id(server_id):
    conn = sqlite3.connect('servers.db')
    c = conn.cursor()
    c.execute('''SELECT role_logs_channel_id FROM servers WHERE server_id = ?''', (server_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def load_server_logs_channel_id(server_id):
    conn = sqlite3.connect('servers.db')
    c = conn.cursor()
    c.execute('''SELECT server_logs_channel_id FROM servers WHERE server_id = ?''', (server_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def load_member_logs_channel_id(server_id):
    conn = sqlite3.connect('servers.db')
    c = conn.cursor()
    c.execute('''SELECT member_logs_channel_id FROM servers WHERE server_id = ?''', (server_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def load_message_logs_channel_id(server_id):
    conn = sqlite3.connect('servers.db')
    c = conn.cursor()
    c.execute('''SELECT message_logs_channel_id FROM servers WHERE server_id = ?''', (server_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def load_reaction_logs_channel_id(server_id):
    conn = sqlite3.connect('servers.db')
    c = conn.cursor()
    c.execute('''SELECT reaction_logs_channel_id FROM servers WHERE server_id = ?''', (server_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

####################################################################################################################################


def update_server_language(server_id, language):
    conn = sqlite3.connect('servers.db')
    c = conn.cursor()
    c.execute('''
        UPDATE servers
        SET language = ?
        WHERE server_id = ?
    ''', (language, server_id))
    conn.commit()
    conn.close()

def get_server_language(server_id):
    conn = sqlite3.connect('servers.db')
    c = conn.cursor()
    c.execute('''SELECT language FROM servers WHERE server_id = ?''', (server_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 'en_eu'

def current_datetime():
    current_logtime = datetime.now()
    current_datetime = datetime.now().strftime("**%m/%d/%Y, %H:%M**")
    return f"{current_datetime} {format_dt(current_logtime, style='R')}"

def format_timedelta(delta):
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"


###################### AUTOMOD


def create_automod_db():
    conn = sqlite3.connect('automod.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS automod_config
                 (server_id TEXT PRIMARY KEY,
                 channel_id TEXT,
                 working BOOLEAN)''')
    conn.commit()
    conn.close()

def add_entry(server_id, channel_id, working=False):
    conn = sqlite3.connect('automod.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO automod_config (server_id, channel_id, working) VALUES (?, ?, ?)",
              (str(server_id), str(channel_id), working))
    conn.commit()
    conn.close()

def get_config(server_id):
    conn = sqlite3.connect('automod.db')
    c = conn.cursor()
    c.execute("SELECT channel_id, working FROM automod_config WHERE server_id=?", (str(server_id),))
    result = c.fetchone()
    conn.close()
    return result

def check_automod_working(guild_id):
    conn = sqlite3.connect('automod.db')
    c = conn.cursor()
    c.execute("SELECT working FROM automod_config WHERE server_id=?", (str(guild_id),))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return False

def load_automod_channel_id(guild_id):
    conn = sqlite3.connect('automod.db')
    c = conn.cursor()
    c.execute('''SELECT channel_id FROM automod_config WHERE server_id = ?''', (guild_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def create_channels_table():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY,
            guild_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL,
            category_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_exception(guild_id, channel_id=None, category_id=None):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO channels (guild_id, channel_id, category_id) VALUES (?, ?, ?)
    ''', (guild_id, channel_id, category_id))
    conn.commit()
    conn.close()

def exception_exists(guild_id, channel_id=None, category_id=None):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    if channel_id:
        cursor.execute('''
            SELECT * FROM channels WHERE guild_id = ? AND channel_id = ?
        ''', (guild_id, channel_id))
    elif category_id:
        cursor.execute('''
            SELECT * FROM channels WHERE guild_id = ? AND category_id = ?
        ''', (guild_id, category_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def remove_exception(guild_id, channel_id=None, category_id=None):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    if channel_id:
        cursor.execute('''
            DELETE FROM channels WHERE guild_id = ? AND channel_id = ?
        ''', (guild_id, channel_id))
    elif category_id:
        cursor.execute('''
            DELETE FROM channels WHERE guild_id = ? AND category_id = ?
        ''', (guild_id, category_id))
    conn.commit()
    conn.close()

def contains_links(text):
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.search(pattern, text) is not None

def is_channel_or_category_exempt(guild_id, channel_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM channels WHERE guild_id = ? AND (channel_id = ? OR category_id IN (
            SELECT category_id FROM channels WHERE channel_id = ?
        ))
    ''', (guild_id, channel_id, channel_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None
