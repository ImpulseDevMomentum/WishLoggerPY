from utils.imports import *
import json

class Language(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="language", description="Set server language")
    async def language(self, interaction: Interaction, language: str = nextcord.SlashOption(name="language", description="Choose the language", choices={"English": "en_eu", "Polski": "pl_pl", "Espanol": "es_es", "Deutsch": "ger_ger", "Cestina": "cs_cs", "Rossiya": "ru"})):
        server_language = get_server_language(interaction.guild.id)
        language_file = f'language/{server_language}.json'

        with open(language_file, 'r') as file:
            language_strings = json.load(file)
        
        if interaction.user.guild_permissions.administrator == True or interaction.user.guild_permissions.manage_channels == True or interaction.user.guild_permissions.manage_roles == True or interaction.user.guild.owner == True:
            server_id = str(interaction.guild.id)
            update_server_language(server_id, language)
            language_string = None
            if language == "en_eu":
                language_string = "<:usflag:1257369987421700149> English"
            elif language == "pl_pl":
                language_string = "<:plflag:1257369555639079062> Polski"
            elif language == "es_es":
                language_string = "<:esflag:1257369553600643134> Spanish"
            elif language == "ger_ger":
                language_string = "<:gerflag:1257369980576727123> German"
            elif language == "cs_cs":
                language_string = "<:csflag:1257369977984389281> Cestina"
            elif language == "ru":
                language_string = "<:ruflag:1257652750016188497> Rossiya"

            await interaction.response.send_message(f"Server language set to: {language_string}", ephemeral=True)
            
        else:
            await interaction.response.send_message(f"{language_strings.get('PERMISSIONS_DENIED')}", ephemeral=True)

def setup(bot):
    bot.add_cog(Language(bot))