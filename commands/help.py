from utils.imports import *

class HelpView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.select(
        placeholder="Choose a category",
        options=[
            nextcord.SelectOption(label="Moderation", description="Moderation commands"),
            nextcord.SelectOption(label="Admin", description="Admin commands"),
            nextcord.SelectOption(label="Warns", description="Warns commands"),
            nextcord.SelectOption(label="Logging", description="Logging commands"),
            nextcord.SelectOption(label="Other", description="Miscellaneous commands")
        ]
    )
    async def select_callback(self, select: nextcord.ui.Select, interaction: nextcord.Interaction):
        category = select.values[0]
        
        if category == "Moderation":
            embed = nextcord.Embed(
                title="Command List (Moderation)",
                description="Here are the available moderation commands:",
                color=nextcord.Color.purple()
            )
            embed.add_field(name="/clear", value="**/clear (amount)** - Deletes a number of messages", inline=False)
            embed.add_field(name="/user", value="**/user (user)** - View user's information", inline=False)
            embed.add_field(name="/slowmode", value="**/slowmode (seconds)** - Set slowmode for channel", inline=False)
            embed.add_field(name="/ban", value="**/ban (user) (reason)** - Ban a user", inline=False)
            embed.add_field(name="/unban", value="**/unban (user id)** - Unban a user", inline=False)
            embed.add_field(name="/kick", value="**/kick (user) (reason)** - Kick a user", inline=False)
            embed.add_field(name="/mute", value="**/mute (user) (time)** - Mute a user", inline=False)
            embed.add_field(name="/unmute", value="**/unmute (user)** - Unmute a user", inline=False)
        
        elif category == "Admin":
            embed = nextcord.Embed(
                title="Command List (Admin)",
                description="Here are the available admin commands:",
                color=nextcord.Color.purple()
            )
            embed.add_field(name="/setlogging", value="**/setlogging (channel)** - Set the logging channel", inline=False)

        elif category == "Warns":
            embed = nextcord.Embed(
                title="Command List (Warns)",
                description="Here are the available warning-related commands:",
                color=nextcord.Color.purple()
            )
            embed.add_field(name="/warn", value="**/warn (user) (reason)** - Issue a warning", inline=False)
            embed.add_field(name="/tempwarn", value="**/tempwarn (user) (duration) (reason) ** - Issue a temporary warning", inline=False)
            embed.add_field(name="/delwarn", value="**/delwarn (user) (case_id)** - Delete a warning", inline=False)
            embed.add_field(name="/chwarn", value="**/chwarn (user) (case_id)** - Change warning reason", inline=False)
            embed.add_field(name="/uwarn", value="**/uwarn (user) (case_id)** - Transfer warning", inline=False)
            embed.add_field(name="/adelwarn", value="**/adelwarn (user)** - Delete all warnings for a user", inline=False)
            embed.add_field(name="/warnlist", value="**/warnlist (user)** - View a user's warnings", inline=False)
            embed.add_field(name="/warnings", value="**/warnings** - View all server warnings", inline=False)

        elif category == "Other":
            embed = nextcord.Embed(
                title="Command List (Other)",
                description="Here are some miscellaneous commands, including snapshots:",
                color=nextcord.Color.purple()
            )
            embed.add_field(name="/help", value="**/help** - Show this help menu", inline=False)
            embed.add_field(name="/server", value="**/server** - Show server information", inline=False)
            embed.add_field(name="/embed", value="**/embed (title, description, color)** - Create a custom embed", inline=False)
            embed.add_field(name="/config info", value="View your server configuration", inline=False)
            embed.add_field(name="/config reset", value="Reset your server configuration to default", inline=False)
            embed.add_field(name="/snapshot create", value="Create a snapshot of your server", inline=False)
            embed.add_field(name="/snapshot delete", value="Delete an existing snapshot", inline=False)
            embed.add_field(name="/snapshot build", value="Rebuild your server from a snapshot", inline=False)
            embed.add_field(name="/snapshot check", value="Check the details of your current snapshot", inline=False)
            embed.add_field(name="/snapshot download", value="Download a snapshot file", inline=False)

        elif category == "Logging":
            embed = nextcord.Embed(
                title="Command List (Logging)",
                description="Here are logging commands:",
                color=nextcord.Color.purple()
            )
            embed.add_field(name="/setlogging `[channel]`", value="Setting up all logs on one channel: /setlogging `[channel]` or /setlogging `[channel]` `[All Logs]`", inline=False)
            embed.add_field(name="/setlogging `[channel]` `[Type]`", value="Setting up **Members Logging** on a specific channel: /setlogging `[member-logs]` `[Member Logs]`", inline=False)

        await interaction.response.edit_message(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="help", description="Display available commands")
    async def help_command(self, interaction: nextcord.Interaction):
        help_view = HelpView()
        help_embed = nextcord.Embed(
            title="Help Menu",
            description="Choose a category to view available commands.",
            color=nextcord.Color.purple()
        )

        await interaction.response.send_message(embed=help_embed, view=help_view, ephemeral=True)

def setup(bot):
    bot.add_cog(Help(bot))