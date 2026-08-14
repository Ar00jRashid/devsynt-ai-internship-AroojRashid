import os
import asyncio
import discord
import aiohttp
from dotenv import load_dotenv


# ============================================================
# LOAD .ENV FROM THE SAME FOLDER AS bot.py
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE, override=True)


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")


# ============================================================
# DEBUG - SHOW WHAT WAS LOADED
# ============================================================

print("========================================")
print("SlotWise Configuration")
print("========================================")

print("Token loaded:", bool(DISCORD_BOT_TOKEN))

if DISCORD_BOT_TOKEN:
    print("Token length:", len(DISCORD_BOT_TOKEN))

print("Webhook URL:", repr(N8N_WEBHOOK_URL))

print("========================================")


# ============================================================
# VALIDATE ENVIRONMENT VARIABLES
# ============================================================

if not DISCORD_BOT_TOKEN:
    raise RuntimeError(
        "DISCORD_BOT_TOKEN is missing from .env"
    )

if not N8N_WEBHOOK_URL:
    raise RuntimeError(
        "N8N_WEBHOOK_URL is missing from .env"
    )


# ============================================================
# DISCORD INTENTS
# ============================================================

intents = discord.Intents.default()

# Required to read normal Discord messages
intents.message_content = True


# ============================================================
# DISCORD CLIENT
# ============================================================

client = discord.Client(intents=intents)


# ============================================================
# BOT READY
# ============================================================

@client.event
async def on_ready():

    print("----------------------------------------")
    print(f"SlotWise is online as {client.user}")
    print("----------------------------------------")


# ============================================================
# RECEIVE DISCORD MESSAGE
# ============================================================

@client.event
async def on_message(message):

    # --------------------------------------------------------
    # Ignore messages sent by the bot itself
    # --------------------------------------------------------

    if message.author == client.user:
        return


    # --------------------------------------------------------
    # Only respond in #slotwise-booking
    # --------------------------------------------------------

    if message.channel.name != "slotwise-booking":
        return


    # --------------------------------------------------------
    # Get user's message
    # --------------------------------------------------------

    user_message = message.content.strip()


    if not user_message:
        return


    # --------------------------------------------------------
    # Display message in CMD
    # --------------------------------------------------------

    print(
        f"{message.author}: {user_message}"
    )


    # --------------------------------------------------------
    # Prepare data for n8n
    # --------------------------------------------------------

    payload = {

        "username": str(message.author),

        "user_id": str(message.author.id),

        "channel_id": str(message.channel.id),

        "channel_name": message.channel.name,

        "message": user_message
    }


    # --------------------------------------------------------
    # Send message to n8n
    # --------------------------------------------------------

    try:

        timeout = aiohttp.ClientTimeout(
            total=30
        )

        async with aiohttp.ClientSession(
            timeout=timeout
        ) as session:

            async with session.post(
                N8N_WEBHOOK_URL,
                json=payload
            ) as response:

                print(
                    f"n8n HTTP status: {response.status}"
                )

                response_text = await response.text()

                print(
                    f"n8n response: {response_text}"
                )


                # ------------------------------------------------
                # Check HTTP status
                # ------------------------------------------------

                if response.status >= 400:

                    raise RuntimeError(
                        f"n8n returned HTTP {response.status}: "
                        f"{response_text}"
                    )


                # ------------------------------------------------
                # Try to read JSON response
                # ------------------------------------------------

                try:

                    data = await response.json(
                        content_type=None
                    )

                except Exception:

                    data = {
                        "reply": response_text
                    }


                # ------------------------------------------------
                # Extract reply from n8n
                # ------------------------------------------------

                if isinstance(data, dict):

                    reply = data.get(
                        "reply",
                        "Sorry, I didn't receive a valid response from n8n."
                    )

                else:

                    reply = str(data)


                # ------------------------------------------------
                # Send n8n response back to Discord
                # ------------------------------------------------

                await message.channel.send(
                    reply
                )


    # --------------------------------------------------------
    # Connection / request error
    # --------------------------------------------------------

    except asyncio.TimeoutError:

        print(
            "Error communicating with n8n: request timed out."
        )

        await message.channel.send(
            "Sorry, SlotWise took too long to respond. "
            "Please try again."
        )


    except Exception as e:

        print(
            f"Error communicating with n8n: {e}"
        )

        await message.channel.send(
            "Sorry, I couldn't connect to SlotWise right now."
        )


# ============================================================
# START BOT
# ============================================================

client.run(DISCORD_BOT_TOKEN)