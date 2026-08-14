# devsynt-ai-internship-AroojRashid
DevSynt AI Automation Internship – Summer 2026 | Weekly tasks, progress updates, notes, screenshots, and internship deliverables.

# SlotWise — AI Restaurant Booking Concierge

SlotWise is an AI-powered restaurant booking concierge that allows users to interact with a restaurant through Discord. The system uses a Python Discord bot as the user-facing interface, n8n as the automation and conversation-processing layer, and Airtable for persistent conversation and booking data.

## Features

* Discord-based restaurant booking assistant
* AI intent detection using Google Gemini
* Restaurant reservation workflow
* Conversation/session state management
* Airtable database integration
* Booking date and time collection
* Party-size extraction
* Reservation confirmation
* Reservation cancellation flow
* Reservation modification flow
* Restaurant information responses
* Human-agent handoff
* Persistent user conversation state

## System Architecture

```text
Discord User
     ↓
Python Discord Bot
     ↓
n8n Webhook
     ↓
Get Conversation State
     ↓
Merge Session
     ↓
Intent Detection
     ↓
AI Agent + Google Gemini
     ↓
Intent Router
     ├── GREETING
     ├── BOOK
     ├── MODIFY
     ├── CANCEL
     ├── INFO
     ├── HUMAN
     └── UNKNOWN
     ↓
Airtable
     ↓
Response
     ↓
Discord User
```

The n8n workflow receives POST requests through the `slotwise` webhook and extracts the Discord username, user ID, channel information, and message.

## Booking Flow

When a user starts a booking, SlotWise creates or updates the user's conversation session and moves through several states:

```text
NEW
 ↓
AWAITING_PARTY_SIZE
 ↓
AWAITING_DATE
 ↓
AWAITING_TIME
 ↓
AWAITING_SLOT_CONFIRM
 ↓
Booking Confirmed
```

The workflow stores the conversation state in Airtable so that the bot can continue the booking when the user sends the next message.

## Technology Stack

* Python
* Discord API
* n8n
* Google Gemini 2.5 Flash Lite
* Airtable
* Webhooks
* JavaScript
* Python `venv`
* `.env` environment variables

The AI layer uses the `gemini-2.5-flash-lite` model for intent classification.

## Airtable

SlotWise uses Airtable to persist conversation and booking information.

The conversation table contains information such as:

* Discord User ID
* Username
* Booking Type
* Service
* Date
* Preferred Time
* Selected Slot
* State
* Updated At
* Notes
* Assignee
* Status

The workflow searches the Conversations table using the Discord User ID to retrieve the user's current session.

## Cancellation

When a cancellation/reset operation occurs, the conversation state is reset to:

```text
NEW
```

This allows the user to start a fresh booking session.

## Human Handoff

Users can request a human representative. SlotWise creates a handoff record containing the Discord User ID so the request can be handled by a human team member.

## Project Structure

```text
SlotWise/
│
├── bot.py
├── .env
├── .gitignore
└── README.md
```

> The `venv` folder should NOT be uploaded to GitHub.

## Environment Variables

Create a `.env` file containing your local credentials:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token
N8N_WEBHOOK_URL=your_n8n_webhook_url
```

Never publish real API keys, bot tokens, or credentials in a public repository.

## Running Locally

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd SlotWise
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
venv\Scripts\activate
```

### 4. Install dependencies

If you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create `.env` and add your Discord bot token and n8n webhook URL.

### 6. Run the bot

```bash
python bot.py
```

## n8n Workflow

The n8n workflow is responsible for:

1. Receiving Discord messages through the webhook
2. Extracting user information
3. Retrieving the user's Airtable conversation state
4. Detecting interruptions such as cancellation or human-agent requests
5. Classifying the user's intent
6. Routing the request
7. Managing booking stages
8. Saving booking information
9. Returning a response to the Discord bot

## Security

Do not commit the following files or secrets:

```text
.env
venv/
__pycache__/
*.pyc
```

Use `.gitignore` to prevent accidental exposure of credentials and unnecessary files.

## Project Status

SlotWise is a conversational restaurant booking automation system integrating Discord, Python, n8n, Google Gemini, and Airtable.

## Author

Arooj Rashid

AI Automation Engineer | LLM & RAG Developer | Python | Machine Learning

