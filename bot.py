import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = 'MTM3ODAyMDA1ODI1MjcwNTgwMg.GjN8Kf.em_ZgWB2vqRoMdLDogdR7IBii4N73nx_b1im4Q' # TOKEN HERE
RAM_LIMIT = '8g'
SERVER_LIMIT = 12

intents = discord.Intents.default()
intents.message_content = True  # ← Add this line
intents.members = True          # ← Required for role checks

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
