import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True  # Required for DM functionality
bot = commands.Bot(command_prefix="!", intents=intents)

async def setup():
    await bot.add_cog(DeployCog(bot))

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot is online: {bot.user} (ID: {bot.user.id})")
    print("------")

# Load the cog after bot is ready
@bot.event
async def on_connect():
    from deploy_cog import DeployCog
    await bot.add_cog(DeployCog(bot))

bot.run(TOKEN)
