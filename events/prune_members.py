from utils.imports import *

class PruneMembersLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry):
        if entry.action == nextcord.AuditLogAction.member_prune:
            server_language = get_server_language(entry.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)

            channel_log_id = load_member_logs_channel_id(entry.guild.id)
            if channel_log_id is not None:
                channel = nextcord.utils.get(entry.guild.text_channels, id=int(channel_log_id))
                if channel is not None:
                    embed = nextcord.Embed(
                        title=language_strings.get("PRUNE_MEMBERS_TITLE"),
                        color=nextcord.Color.orange()
                    )
                    embed.add_field(name=language_strings.get("PRUNE_INITIATED_BY"), value=entry.user.mention, inline=False)
                    embed.add_field(name=language_strings.get("PRUNED_MEMBERS_COUNT"), value=str(entry.options["delete_member_days"]), inline=True)
                    embed.add_field(name=language_strings.get("TODAY_AT"), value=current_datetime(), inline=True)
                    
                    await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(PruneMembersLog(bot))
