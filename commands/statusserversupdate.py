from utils.imports import *
from utils.allowed_users import allowed_user_ids

class ServersUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="serversupdate", description="Update servers status via command")
    async def performance(self, interaction: nextcord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        if interaction.user.id not in allowed_user_ids:
            server_language = get_server_language(interaction.guild.id)
            language_file = f'language/{server_language}.json'
            
            try:
                with open(language_file, 'r') as file:
                    language_strings = json.load(file)
                await interaction.response.send_message(language_strings.get("ACCESS_DENIED"), ephemeral=True)
            except FileNotFoundError:
                await interaction.response.send_message("Language file not found. Please contact the administrator.", ephemeral=True)
            return

        server_count = len(self.bot.guilds)
        await self.bot.change_presence(activity=nextcord.Game(name=f"/help | {server_count} servers"))
        await interaction.response.send_message(f"Server status was updated to {server_count} servers.", ephemeral=True)

def setup(bot):
    bot.add_cog(ServersUpdate(bot))