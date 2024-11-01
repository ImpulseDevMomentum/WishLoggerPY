from utils.imports import *
import os
import json

def load_previous_pinned_ids(channel_id):
    if not os.path.exists("pinned_messages.json"):
        return set()

    with open("pinned_messages.json", "r") as file:
        data = json.load(file)
        return set(data.get(str(channel_id), []))

def save_current_pinned_ids(channel_id, pinned_ids):
    if os.path.exists("pinned_messages.json"):
        with open("pinned_messages.json", "r") as file:
            data = json.load(file)
    else:
        data = {}

    data[str(channel_id)] = list(pinned_ids)

    with open("pinned_messages.json", "w") as file:
        json.dump(data, file, indent=4)

class PinEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        guild = channel.guild
        server_language = get_server_language(guild.id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        channel_log_id = load_message_logs_channel_id(guild.id)
        logs_channel = nextcord.utils.get(guild.text_channels, id=int(channel_log_id))

        if logs_channel:
            current_pins = await channel.pins()
            current_pinned_ids = {pin.id for pin in current_pins}
            
            previous_pinned_ids = load_previous_pinned_ids(channel.id)
            
            new_pins = current_pinned_ids - previous_pinned_ids
            removed_pins = previous_pinned_ids - current_pinned_ids

            if new_pins:
                for message_id in new_pins:
                    try:
                        message = await channel.fetch_message(message_id)
                        embed = nextcord.Embed(
                            title=language_strings.get("MESSAGE_PINNED_TITLE"), 
                            color=nextcord.Color.green()
                        )
                        embed.add_field(
                            name=language_strings.get("CHANNEL"), 
                            value=channel.mention, 
                            inline=True
                        )
                        embed.add_field(
                            name=language_strings.get("MESSAGE"), 
                            value=message.jump_url, 
                            inline=True
                        )
                        embed.add_field(
                            name=language_strings.get("MESSAGE_CONTENT"), 
                            value=message.content or language_strings.get("NO_CONTENT"), 
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("TODAY_AT"), 
                            value=current_datetime(), 
                            inline=True
                        )
                        embed.set_footer(text=f"{language_strings.get('MESSAGE_ID')}: {message.id}")
                        await logs_channel.send(embed=embed)
                    except nextcord.NotFound:
                        embed = nextcord.Embed(
                            title=language_strings.get("MESSAGE_PINNED_TITLE"), 
                            color=nextcord.Color.green()
                        )
                        embed.add_field(
                            name=language_strings.get("CHANNEL"), 
                            value=channel.mention, 
                            inline=True
                        )
                        embed.add_field(
                            name=language_strings.get("MESSAGE_CONTENT"), 
                            value=language_strings.get("MESSAGE_NOT_FOUND"), 
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("TODAY_AT"), 
                            value=current_datetime(), 
                            inline=True
                        )
                        embed.set_footer(text=language_strings.get("MESSAGE_NOT_RETRIEVABLE"))
                        await logs_channel.send(embed=embed)

            if removed_pins:
                for message_id in removed_pins:
                    try:
                        message = await channel.fetch_message(message_id)
                        embed = nextcord.Embed(
                            title=language_strings.get("MESSAGE_UNPINNED_TITLE"), 
                            color=nextcord.Color.red()
                        )
                        embed.add_field(
                            name=language_strings.get("CHANNEL"), 
                            value=channel.mention, 
                            inline=True
                        )
                        embed.add_field(
                            name=language_strings.get("MESSAGE_CONTENT"), 
                            value=message.content or language_strings.get("NO_CONTENT"), 
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("TODAY_AT"), 
                            value=current_datetime(), 
                            inline=True
                        )
                        embed.set_footer(text=f"{language_strings.get('MESSAGE_ID')}: {message.id}")
                        await logs_channel.send(embed=embed)
                    except nextcord.NotFound:
                        embed = nextcord.Embed(
                            title=language_strings.get("MESSAGE_UNPINNED_TITLE"), 
                            color=nextcord.Color.red()
                        )
                        embed.add_field(
                            name=language_strings.get("CHANNEL"), 
                            value=channel.mention, 
                            inline=True
                        )
                        embed.add_field(
                            name=language_strings.get("MESSAGE_CONTENT"), 
                            value=language_strings.get("MESSAGE_NOT_FOUND"), 
                            inline=False
                        )
                        embed.add_field(
                            name=language_strings.get("TODAY_AT"), 
                            value=current_datetime(), 
                            inline=True
                        )
                        embed.set_footer(text=language_strings.get("MESSAGE_NOT_RETRIEVABLE"))
                        await logs_channel.send(embed=embed)
            
            save_current_pinned_ids(channel.id, current_pinned_ids)

def setup(bot):
    bot.add_cog(PinEvents(bot))