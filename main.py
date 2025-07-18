import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta
import pytz
import asyncio
import os
TOKEN = os.getenv("TOKEN")
GUILD_ID = 946757939316817951  # Replace if needed
CHANNEL_ID = 1395839181867188365
ROLE_NAME = "GTA HUB"

# Timezone
tz = pytz.timezone("Europe/Berlin")  # UTC+2 (CEST)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Schedule format: {"Activity Name": {"days": [list_of_days], "times": ["HH:MM"]}}
schedule = {
    "Trafficking mission": {
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "times": ["14:00", "18:00", "22:00"]
    },
    "Naval Traffic": {
        "days": ["Tuesday", "Thursday", "Saturday"],
        "times": ["03:00", "09:00", "15:00", "21:00"]
    },
    "Chemical distribution": {
        "days": ["Tuesday", "Thursday"],
        "times": ["14:00", "19:00"]
    },
    "Blow up their vehicles": {
        "days": ["Tuesday", "Thursday", "Saturday", "Sunday"],
        "times": ["19:00", "23:00"]
    },
    "Maintenance of MM": {
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "times": ["21:00"]
    },
    "OT": {
        "days": ["Tuesday"],
        "times": ["21:00"]
    },
    "Aquatic Search": {
        "days": ["Monday", "Saturday", "Sunday"],
        "times": ["19:00"]
    }
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    reminder_loop.start()

@tasks.loop(minutes=1)
async def reminder_loop():
    now = datetime.now(tz)
    reminder_time = now + timedelta(minutes=10)
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found.")
        return

    for activity, info in schedule.items():
        if reminder_time.strftime("%A") in info["days"]:
            for time_str in info["times"]:
                activity_dt = tz.localize(datetime.strptime(reminder_time.strftime("%Y-%m-%d") + " " + time_str, "%Y-%m-%d %H:%M"))
                if activity_dt.strftime("%Y-%m-%d %H:%M") == reminder_time.strftime("%Y-%m-%d %H:%M"):
                    # Mention role by name (needs role to exist in server)
                    guild = bot.get_guild(GUILD_ID)
                    role = discord.utils.get(guild.roles, name=ROLE_NAME)
                    mention = role.mention if role else f"@{ROLE_NAME}"
                    await channel.send(f"{mention} Reminder: **{activity}** starts in 10 minutes at {time_str} CEST!")

bot.run(TOKEN)
