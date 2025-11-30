# Telegram User Saver Bot

This bot saves new members in a group to a local SQLite database and shows them on command.

## Features
- Saves `telegram_id` and `username` of any new member who joins a group with the bot
- Command `/134950` outputs the list of all saved users

## Setup
1. Clone repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the environment template and add your bot token:
   ```bash
   cp .env.example .env
   # edit .env and set BOT_TOKEN
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

## Files
- `bot.py` – main bot script
- `database.py` – SQLite helpers
- `config.py` – loads `BOT_TOKEN` from environment

## Notes
- The database file `users.db` will be created automatically in the project root.
- The dump command number `134950` can be changed by editing `bot.py`.