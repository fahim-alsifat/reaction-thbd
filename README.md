# Telegram Reaction Bots

Create a fleet of Telegram bots that automatically react to every message in a chat with a specific emoji. This repository holds the shared Python runtime, plus individual environment files so each bot can be deployed independently (for example onto Railway).

## Tech Stack
- Python 3.11+
- [aiogram 3](https://docs.aiogram.dev/en/latest/) — async Telegram Bot API client
- Deployment target: Railway (or any platform that supports long-running Python processes)

## How it Works
1. Each bot loads two environment variables: `BOT_TOKEN` and `REACTION_EMOJI`.
2. The shared `bot.py` script listens for every incoming message.
3. For each message, the bot invokes `set_message_reaction` with its configured emoji.
4. A single codebase powers all bots; only the env file changes.

## Project Layout
```
bot.py
requirements.txt
.env.thumbsup
.env.heart
.env.grin
.env.heart_eyes
.env.fire
.env.kiss
.env.warm
.env.look
.env.cool
.env.hundred
.env.tear
.env.warm2
.env.clap
.env.raise
.env.grin2
```

The `.env.*` files ship with placeholders — replace the `BOT_TOKEN` values with real tokens from @BotFather before deploying. Duplicate emojis are intentional to match Telegram's most-used reactions list.

## Local Setup
1. **Install dependencies**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. **Choose an env file** (for example `.env.heart`) and load it:
   ```powershell
   copy .env.heart .env
   # Edit .env and paste the token from BotFather
   ```
   The script uses standard environment variables, so you can also export them manually instead of creating `.env`.
3. **Run the bot locally**
   ```powershell
   python bot.py
   ```

## Environment Files
| File | Emoji | Suggested Bot Name |
|------|-------|--------------------|
| `.env.thumbsup` | 👍 | `ReactionBotThumb` |
| `.env.heart` | ❤️ | `ReactionBotHeart` |
| `.env.grin` | 😁 | `ReactionBotGrin` |
| `.env.heart_eyes` | 😍 | `ReactionBotAdore` |
| `.env.fire` | 🔥 | `ReactionBotFire` |
| `.env.kiss` | 👄 | `ReactionBotKiss` |
| `.env.warm` | 🥰 | `ReactionBotWarm` |
| `.env.look` | 👀 | `ReactionBotLook` |
| `.env.cool` | 😎 | `ReactionBotCool` |
| `.env.hundred` | 💯 | `ReactionBotHundred` |
| `.env.tear` | 😢 | `ReactionBotTear` |
| `.env.warm2` | 🥰 | `ReactionBotWarm2` |
| `.env.clap` | 👏 | `ReactionBotClap` |
| `.env.raise` | 🙌 | `ReactionBotRaise` |
| `.env.grin2` | 😁 | `ReactionBotGrin2` |

Each file contains the two expected keys:
```
BOT_TOKEN=PASTE_TELEGRAM_BOT_TOKEN
REACTION_EMOJI=🔁
```
Replace `🔁` with the correct emoji for that bot.

## Railway Deployment Guide
1. Push this repository to GitHub (e.g. `telegram-reaction-bots`).
2. In Railway, click **New Project → Deploy from GitHub** and select the repo.
3. For each bot you want to run:
   - Create a new Railway project instance.
   - Set the **Project Name** to match the bot (e.g. `ReactionBot ❤️`).
   - Add environment variables:
     - `BOT_TOKEN` — paste the BotFather token for that bot.
     - `REACTION_EMOJI` — paste the emoji.
   - Build command: `pip install -r requirements.txt`
   - Start command: `python bot.py`
4. Enable Auto Deploy for each Railway project so updates ship automatically when you push to GitHub.
5. Invite each bot to your target chats and grant admin rights so they can send reactions.

Repeat the Railway deployment process 15 times, swapping in the correct token and emoji each time.

## Testing Checklist
- Confirm the bot account is an admin in the chat (reaction permission required).
- Send a test message and ensure the bot reacts instantly with the configured emoji.
- Review Railway logs for any errors (token invalid, missing permissions, etc.).

Happy reacting! 🎉
