from utils.imports import *

class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @wish.slash_command(name="role", description="Role management commands")
    async def role(self, interaction: Interaction):
        pass

    @role.subcommand(name="add", description="Add a role to a member")
    async def role_add(
        self, 
        interaction: Interaction, 
        member: nextcord.Member = SlashOption(description="A member of your server", required=True), 
        role: nextcord.Role = SlashOption(description="A role of your choice", required=True)
    ):
        if interaction.user != interaction.guild.owner:
            if not interaction.user.guild_permissions.manage_roles:
                server_language = get_server_language(interaction.guild.id)
                language_file = f'language/{server_language}.json'

                with open(language_file, 'r') as file:
                    language_strings = json.load(file)

                await interaction.response.send_message(language_strings.get('PERMISSIONS_DENIED'), ephemeral=True)
                return

            if role >= interaction.user.top_role:
                await interaction.response.send_message(
                    "<:PermDenied:1248352895854973029> You cannot assign roles higher or equal to your highest role.",
                    ephemeral=True
                )
                return

        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                "<:PermDenied:1248352895854973029> I cannot assign a role higher than or equal to my highest role.",
                ephemeral=True
            )
            return

        await member.add_roles(role)
        await interaction.response.send_message(
            f"<:Fine:1248352477502246932> Successfully added {role.mention} to {member.mention}.", 
            ephemeral=True
        )

    @role.subcommand(name="remove", description="Remove a role from a member")
    async def role_remove(
        self, 
        interaction: Interaction, 
        member: nextcord.Member = SlashOption(description="A member of your server", required=True), 
        role: nextcord.Role = SlashOption(description="A role of your choice", required=True)
    ):
        if interaction.user != interaction.guild.owner:
            if not interaction.user.guild_permissions.manage_roles:
                server_language = get_server_language(interaction.guild.id)
                language_file = f'language/{server_language}.json'

                with open(language_file, 'r') as file:
                    language_strings = json.load(file)

                await interaction.response.send_message(language_strings.get('PERMISSIONS_DENIED'), ephemeral=True)
                return

            if role >= interaction.user.top_role:
                await interaction.response.send_message(
                    "<:PermDenied:1248352895854973029> You cannot remove roles higher or equal to your highest role.",
                    ephemeral=True
                )
                return

        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                "<:PermDenied:1248352895854973029> I cannot remove a role higher than or equal to my highest role.",
                ephemeral=True
            )
            return

        await member.remove_roles(role)
        await interaction.response.send_message(
            f"<:Fine:1248352477502246932> Successfully removed {role.mention} from {member.mention}.", 
            ephemeral=True
        )

def setup(bot):
    bot.add_cog(RoleManagement(bot))