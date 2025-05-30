import discord
from discord.ext import commands
from discord import app_commands
import os
import random

class DeployCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_role = os.getenv("ALLOWED_ROLE")
        self.allowed_channel_id = int(os.getenv("ALLOWED_CHANNEL_ID"))
        self.vps_records = {}  # {user_id: {"vps_id": int, "os": str, "cpu": int}}

    async def check_permissions(self, interaction: discord.Interaction):
        # Check role
        if self.allowed_role not in [role.name for role in interaction.user.roles]:
            await interaction.response.send_message(
                "❌ You do not have permission to use this command.",
                ephemeral=True
            )
            return False
        
        # Check channel
        if interaction.channel_id != self.allowed_channel_id:
            await interaction.response.send_message(
                "❌ This command is not allowed in this channel.",
                ephemeral=True
            )
            return False
        
        return True

    @app_commands.command(name="deploy", description="Deploy a simulated VPS")
    @app_commands.describe(
        os="Operating System (e.g., ubuntu, debian)",
        cpu="Number of CPU cores (minimum 1)"
    )
    async def deploy(self, interaction: discord.Interaction, os: str, cpu: int):
        # Check permissions
        if not await self.check_permissions(interaction):
            return

        # Check if user already has a VPS
        if interaction.user.id in self.vps_records:
            await interaction.response.send_message(
                "⚠️ You already have a VPS deployed. Delete it before creating a new one.",
                ephemeral=True
            )
            return

        # Validate CPU input
        if cpu < 1:
            await interaction.response.send_message(
                "❌ CPU must be at least 1 core.",
                ephemeral=True
            )
            return

        # Generate a random VPS ID
        vps_id = random.randint(1000, 9999)
        ram = 32768  # Fixed 32GB

        # Store VPS info
        self.vps_records[interaction.user.id] = {
            "vps_id": vps_id,
            "os": os,
            "cpu": cpu,
            "ram": ram
        }

        # Send response
        await interaction.response.send_message(
            f"🚀 Deploying VPS with OS: {os}, RAM: {ram}MB, CPU: {cpu} cores...\n"
            f"✅ VPS deployed successfully! VPS ID: #{vps_id}\n"
            f"📩 Check your DMs for the SSH connection details!"
        )

        # Send DM with SSH details
        try:
            await interaction.user.send(
                f"🔑 Your VPS #{vps_id} SSH connection details:\n\n"
                f"OS: {os}\n"
                f"CPU: {cpu} cores\n"
                f"RAM: {ram}MB\n\n"
                "```ssh user@tmate.io```\n"
                "Password: vps@1234"
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Could not send you a DM. Please enable DMs from server members.",
                ephemeral=True
            )

    @app_commands.command(name="delete_vps", description="Delete your existing VPS")
    async def delete_vps(self, interaction: discord.Interaction):
        # Check permissions
        if not await self.check_permissions(interaction):
            return

        # Check if user has a VPS
        if interaction.user.id not in self.vps_records:
            await interaction.response.send_message(
                "❌ You don't have any VPS to delete.",
                ephemeral=True
            )
            return

        # Delete VPS
        vps_id = self.vps_records[interaction.user.id]["vps_id"]
        del self.vps_records[interaction.user.id]
        
        await interaction.response.send_message(
            f"🗑️ VPS #{vps_id} has been deleted. You can now deploy a new one."
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        await ctx.send(f"❌ An error occurred: {str(error)}")
