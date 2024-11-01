from utils.imports import *
import psutil
from utils.allowed_users import allowed_user_ids

class Performance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="performance", description="Check wish performance via command")
    async def performance(self, interaction: nextcord.Interaction):
        if interaction.user.id not in allowed_user_ids:
            server_language = get_server_language(interaction.guild.id)
            language_file = f'language/{server_language}.json'

            with open(language_file, 'r') as file:
                language_strings = json.load(file)
            await interaction.response.send_message(language_strings.get("ACCESS_DENIED"), ephemeral=True)
            return
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count(logical=True)

        memory_info = psutil.virtual_memory()
        total_memory = round(memory_info.total / (1024 ** 3), 2)
        used_memory = round(memory_info.used / (1024 ** 3), 2)
        memory_usage_percent = memory_info.percent

        disk_info = psutil.disk_usage('/')
        total_disk = round(disk_info.total / (1024 ** 3), 2)
        used_disk = round(disk_info.used / (1024 ** 3), 2)
        disk_usage_percent = disk_info.percent

        net_info = psutil.net_io_counters()
        bytes_sent = round(net_info.bytes_sent / (1024 ** 2), 2)
        bytes_recv = round(net_info.bytes_recv / (1024 ** 2), 2)

        boot_time = psutil.boot_time()
        uptime = round((psutil.time.time() - boot_time) / 3600, 2)

        embed = nextcord.Embed(
            title="Server Performance Stats",
            color=nextcord.Color.green()
        )

        embed.add_field(name="CPU Usage", value=f"{cpu_usage}% ({cpu_count} cores)", inline=False)
        embed.add_field(name="Memory Usage", value=f"{used_memory}GB/{total_memory}GB ({memory_usage_percent}%)", inline=False)
        embed.add_field(name="Disk Usage", value=f"{used_disk}GB/{total_disk}GB ({disk_usage_percent}%)", inline=False)
        embed.add_field(name="Network Usage", value=f"Sent: {bytes_sent}MB, Received: {bytes_recv}MB", inline=False)
        embed.add_field(name="System Uptime", value=f"{uptime} hours", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Performance(bot))