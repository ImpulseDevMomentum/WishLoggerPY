from utils.imports import *

class UnbanUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="unban", description="Unban a user from the server")
    async def unban_user(self, interaction: nextcord.Interaction):
        if not (interaction.user.guild_permissions.ban_members or interaction.user.guild_permissions.administrator or interaction.user == interaction.guild.owner):
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permissions to use this command.", ephemeral=True)
            return

        try:
            bans = await interaction.guild.bans().flatten()
            if not bans:
                await interaction.response.send_message(f"<:NotFine:1248352479599661056> No banned users found.", ephemeral=True)
                return

            limited_bans = bans[:19]
            options = []
            for ban_entry in limited_bans:
                reason = ban_entry.reason if ban_entry.reason else 'No reason provided'
                truncated_reason = reason[:100] if len(reason) <= 100 else reason[:97] + '...'

                options.append(
                    nextcord.SelectOption(
                        label=f"{ban_entry.user.name}#{ban_entry.user.discriminator}",
                        description=f"Reason: {truncated_reason}",
                        value=str(ban_entry.user.id)
                    )
                )

            select_menu = nextcord.ui.Select(
                placeholder="Choose a user to unban",
                options=options,
                min_values=1,
                max_values=1
            )

            async def select_callback(interaction: nextcord.Interaction):
                user_id = select_menu.values[0]
                user = await self.bot.fetch_user(user_id)
                await interaction.guild.unban(user)
                await interaction.response.send_message(f"<:Fine:1248352477502246932> User {user.mention} has been unbanned.", ephemeral=True)

            select_menu.callback = select_callback

            search_button = nextcord.ui.Button(label="Search", style=nextcord.ButtonStyle.primary)

            async def search_button_callback(interaction: nextcord.Interaction):
                modal = nextcord.ui.Modal(title="Search Banned Users")
                
                search_input = nextcord.ui.TextInput(
                    label="Enter username or part of it",
                    placeholder="Username",
                    min_length=1,
                    max_length=100
                )

                modal.add_item(search_input)

                async def modal_callback(interaction: nextcord.Interaction):
                    search_query = search_input.value.lower()
                    matching_bans = [
                        ban_entry for ban_entry in bans
                        if search_query in f"{ban_entry.user.name}#{ban_entry.user.discriminator}".lower()
                    ]

                    if matching_bans:
                        new_options = []
                        for ban_entry in matching_bans:
                            reason = ban_entry.reason if ban_entry.reason else 'No reason provided'
                            truncated_reason = reason[:100] if len(reason) <= 100 else reason[:97] + '...'

                            new_options.append(
                                nextcord.SelectOption(
                                    label=f"{ban_entry.user.name}#{ban_entry.user.discriminator}",
                                    description=f"Reason: {truncated_reason}",
                                    value=str(ban_entry.user.id)
                                )
                            )

                        select_menu.options = new_options
                        await interaction.response.edit_message(content="Select a user to unban:", view=view)
                    else:
                        await interaction.response.send_message(f"<:NotFine:1248352479599661056> No users matching '{search_query}' found.", ephemeral=True)

                modal.callback = modal_callback

                await interaction.response.send_modal(modal)

            search_button.callback = search_button_callback

            view = nextcord.ui.View()
            view.add_item(select_menu)
            view.add_item(search_button)

            await interaction.response.send_message("Select a user to unban:", view=view, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"<:Warning:1248654084500885526> An error occurred: {str(e)}", ephemeral=True)

def setup(bot):
    bot.add_cog(UnbanUser(bot))