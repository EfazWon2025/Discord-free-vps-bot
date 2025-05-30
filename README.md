# Discord VPS Bot

A Discord bot that simulates VPS deployments with slash commands.

## Features
- `/deploy <os> <cpu>` - Deploy a new VPS (32GB RAM automatically allocated)
- `/delete_vps` - Delete your existing VPS
- Role-based access control
- Channel restriction
- DM notifications with SSH details
- One VPS per user restriction

## Setup
1. Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications)
2. Invite the bot to your server with these permissions:
   - `applications.commands`
   - `bot` (with "Send Messages" and "Manage Roles" permissions)
3. Create a `.env` file with your credentials (see `.env.example`)
4. Install requirements: `pip install -r requirements.txt`
5. Run the bot: `python bot.py`

## Environment Variables
- `DISCORD_TOKEN` - Your bot token
- `ALLOWED_ROLE` - Role name required to use commands
- `ALLOWED_CHANNEL_ID` - Channel ID where commands can be used
