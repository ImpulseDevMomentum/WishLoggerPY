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
