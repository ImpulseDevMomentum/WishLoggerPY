from utils.imports import *

WEBHOOKS_STATE_FILE = "webhooks_state.json"

def load_webhooks_state():
    if os.path.exists(WEBHOOKS_STATE_FILE):
        with open(WEBHOOKS_STATE_FILE, "r") as file:
            return json.load(file)
    return {}

def save_webhooks_state(state):
    with open(WEBHOOKS_STATE_FILE, "w") as file:
        json.dump(state, file, indent=4)

class WebhookEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
        guild = channel.guild
        guild_id = str(guild.id)
        channel_id = str(channel.id)
        server_language = get_server_language(guild.id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            language_strings = json.load(file)

        channel_log_id = load_server_logs_channel_id(guild.id)
        
        if channel_log_id is not None:
            log_channel = nextcord.utils.get(guild.text_channels, id=int(channel_log_id))
            
            current_webhooks = await channel.webhooks()
            current_webhooks_state = {str(webhook.id): {"name": webhook.name, "avatar": str(webhook.avatar)} for webhook in current_webhooks}
            
            state = load_webhooks_state()
            guild_state = state.get(guild_id, {})
            previous_webhooks_state = guild_state.get(channel_id, {})
            
            new_webhooks = set(current_webhooks_state) - set(previous_webhooks_state)
            deleted_webhooks = set(previous_webhooks_state) - set(current_webhooks_state)
            updated_webhooks = {
                webhook_id for webhook_id in current_webhooks_state 
                if webhook_id in previous_webhooks_state 
                and (
                    current_webhooks_state[webhook_id]["name"] != previous_webhooks_state[webhook_id]["name"]
                    or current_webhooks_state[webhook_id]["avatar"] != previous_webhooks_state[webhook_id]["avatar"]
                )
            }

            for webhook_id in new_webhooks:
                webhook = nextcord.utils.get(current_webhooks, id=int(webhook_id))
                avatar_url = webhook.avatar.url if webhook.avatar else nextcord.Embed.Empty
                creator = await guild.fetch_member(webhook.user.id) if webhook.user else None
                creator_mention = creator.mention if creator else language_strings.get("UNKNOWN")
                embed = nextcord.Embed(
                    title=language_strings.get("WEBHOOK_CREATED_TITLE"), 
                    color=nextcord.Color.green()
                )
                embed.add_field(
                    name=language_strings.get("CHANNEL"),
                    value=channel.mention
                )
                embed.add_field(
                    name=f"{language_strings.get('WEBHOOK')}: {webhook.name}",
                    value=(
                        f"{language_strings.get('AVATAR')}: [{language_strings.get('AVATAR_WEBHOOK')}]({avatar_url})\n"
                        f"{language_strings.get('URL')}: [URL]({webhook.url})\n"
                        f"{language_strings.get('CREATOR')}: {creator_mention}"
                    )
                )
                embed.add_field(
                    name=language_strings.get("TODAY_AT"), 
                    value=current_datetime(), 
                    inline=True
                )
                await log_channel.send(embed=embed)

            for webhook_id in deleted_webhooks:
                webhook_data = previous_webhooks_state[webhook_id]

                async for entry in guild.audit_logs(limit=1, action=nextcord.AuditLogAction.webhook_delete):
                    if str(entry.target.id) == webhook_id:
                        moderator = entry.user.mention
                        break
                else:
                    moderator = language_strings.get("UNKNOWN")

                embed = nextcord.Embed(
                    title=language_strings.get("WEBHOOK_DELETED_TITLE"), 
                    color=nextcord.Color.red()
                )
                embed.add_field(
                    name=language_strings.get("CHANNEL"),
                    value=channel.mention
                )
                embed.add_field(
                    name=language_strings.get("WEBHOOK"),
                    value=webhook_data["name"]
                )
                embed.add_field(
                    name=language_strings.get("MODERATOR_WEBHOOK"),
                    value=moderator
                )
                embed.add_field(
                    name=language_strings.get("TODAY_AT"), 
                    value=current_datetime()
                )
                await log_channel.send(embed=embed)

            for webhook_id in updated_webhooks:
                webhook = nextcord.utils.get(current_webhooks, id=int(webhook_id))
                old_name = previous_webhooks_state[webhook_id]["name"]
                new_name = webhook.name
                old_avatar = previous_webhooks_state[webhook_id]["avatar"]
                new_avatar = str(webhook.avatar)

                creator = await guild.fetch_member(webhook.user.id) if webhook.user else None
                creator_mention = creator.mention if creator else language_strings.get("UNKNOWN")

                async for entry in guild.audit_logs(limit=1, action=nextcord.AuditLogAction.webhook_update):
                    if str(entry.target.id) == webhook_id:
                        moderator = entry.user.mention
                        break
                else:
                    moderator = language_strings.get("UNKNOWN")

                embed = nextcord.Embed(
                    title=f"{language_strings.get('WEBHOOK_UPDATED_TITLE').format(new_name=new_name)}",
                    color=nextcord.Color.gold()
                )
                embed.add_field(
                    name=language_strings.get("CHANNEL"),
                    value=channel.mention
                )

                if old_name != new_name and old_avatar == new_avatar:
                    embed.add_field(
                        name=language_strings.get("WEBHOOK_NAME_UPDATED"),
                        value=(
                            f"**{old_name}** {language_strings.get('TO')} **{new_name}**\n"
                            f"{language_strings.get('URL')}: [URL]({webhook.url})\n"
                            f"{language_strings.get('CREATOR')}: {creator_mention}\n"
                            f"{language_strings.get('MODERATOR_WEBHOOK')}: {moderator}"
                        )
                    )
                elif old_name == new_name and old_avatar != new_avatar:
                    embed.add_field(
                        name=language_strings.get("WEBHOOK_AVATAR_UPDATED"),
                        value=(
                            f"{language_strings.get('AVATAR')}: [{language_strings.get('OLD_AVATAR')}]({old_avatar}) {language_strings.get('TO')} [{language_strings.get('NEW_AVATAR')}]({new_avatar})\n"
                            f"{language_strings.get('URL')}: [URL]({webhook.url})\n"
                            f"{language_strings.get('CREATOR')}: {creator_mention}\n"
                            f"{language_strings.get('MODERATOR_WEBHOOK')}: {moderator}"
                        )
                    )
                else:
                    embed.add_field(
                        name=language_strings.get("WEBHOOK_UPDATED"),
                        value=(
                            f"**{old_name}** {language_strings.get('TO')} **{new_name}**\n"
                            f"{language_strings.get('AVATAR')}: [{language_strings.get('OLD_AVATAR')}]({old_avatar}) {language_strings.get('TO')} [{language_strings.get('NEW_AVATAR')}]({new_avatar})\n"
                            f"{language_strings.get('URL')}: [URL]({webhook.url})\n"
                            f"{language_strings.get('CREATOR')}: {creator_mention}\n"
                            f"{language_strings.get('MODERATOR_WEBHOOK')}: {moderator}"
                        )
                    )
                embed.add_field(
                    name=language_strings.get("TODAY_AT"), 
                    value=current_datetime(), 
                    inline=True
                )
                await log_channel.send(embed=embed)

            if guild_id not in state:
                state[guild_id] = {}
            state[guild_id][channel_id] = current_webhooks_state
            save_webhooks_state(state)

def setup(bot):
    bot.add_cog(WebhookEvents(bot))