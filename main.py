import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta
import pytz
import asyncio
import os

TOKEN = os.getenv("TOKEN")
GUILD_ID = 946757939316817951
CHANNEL_ID = 1395839181867188365
ROLE_NAME = "GTA HUB"

# Timezone
tz = pytz.timezone("Europe/Berlin")  # UTC+2 (CEST)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

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
    print(f"[READY] Logged in as {bot.user}")
    reminder_loop.start()

@tasks.loop(minutes=1)
async def reminder_loop():
    now = datetime.now(tz)
    reminder_time = now + timedelta(minutes=10)
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("[ERROR] Channel not found.")
        return

    for activity, info in schedule.items():
        if reminder_time.strftime("%A") in info["days"]:
            for time_str in info["times"]:
                try:
                    # Parse target time and build datetime for today
                    target_time = datetime.strptime(time_str, "%H:%M").time()
                    activity_datetime = tz.localize(datetime.combine(reminder_time.date(), target_time))

                    # Compare within 60 seconds tolerance
                    if abs((activity_datetime - reminder_time).total_seconds()) < 60:
                        guild = bot.get_guild(GUILD_ID)
                        role = discord.utils.get(guild.roles, name=ROLE_NAME)
                        mention = role.mention if role else f"@{ROLE_NAME}"
                        msg = f"{mention} Reminder: **{activity}** starts in 10 minutes at {time_str} CEST!"
                        await channel.send(msg)
                        print(f"[REMINDER SENT] {msg}")
                    else:
                        print(f"[SKIPPED] {activity} at {time_str} — no time match")
                except Exception as e:
                    print(f"[ERROR] Failed to process {activity} at {time_str}: {e}")

bot.run(TOKEN)
