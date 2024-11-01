from utils.imports import *
from nextcord import ButtonStyle
from nextcord.ui import View, Button

class ConfirmClearView(View):
    def __init__(self, interaction: Interaction, amount: int, timeout=60):
        super().__init__(timeout=timeout)
        self.interaction = interaction
        self.amount = amount
        self.result = None

    @nextcord.ui.button(label="Confirm", style=ButtonStyle.danger)
    async def confirm_clear(self, button: Button, interaction: Interaction):
        await self.interaction.channel.purge(limit=self.amount)
        await self.interaction.followup.send(f"<:Fine:1248352477502246932> You've cleared {self.amount} message(s).", ephemeral=True)
        self.result = True
        self.stop()


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="clear", description="Clear some messages on your server")
    async def purge(
        self, 
        interaction: Interaction, 
        amount: int = SlashOption(description="Number of messages you want to clear", required=True)
):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)

        if member.guild_permissions.manage_messages or member == guild.owner or member.guild_permissions.administrator:
            limit = 100
            amount = max(1, min(amount, limit))

            if amount >= 100:
                await interaction.response.send_message("<:Warning:1248654084500885526> You can't purge more than __100__ messages", ephemeral=True)
            else:

                if amount >= 50:
                    embed_warning = nextcord.Embed(
                        title="<:NotFine:1248352479599661056> Warning!",
                        description=f"You're about to clear **{amount}** messages. Are you sure you want to do this?",
                        color=nextcord.Color.red()
                    )

                    view = ConfirmClearView(interaction, amount)

                    await interaction.response.send_message(embed=embed_warning, view=view, ephemeral=True)
                    await view.wait()
                else:
                    await interaction.channel.purge(limit=amount)
                    await interaction.response.send_message(f"<:Fine:1248352477502246932> You've cleared {amount} message(s).", ephemeral=True)

        else:
            await interaction.response.send_message("<:PermDenied:1248352895854973029> You don't have permission to use this command.", ephemeral=True)

def setup(bot):
    bot.add_cog(Clear(bot))