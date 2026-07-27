# Telegram Banking Bot

A simple virtual banking bot for Telegram, built with python-telegram-bot and designed for easy deployment on Railway.

## Features

- Check account balance
- Deposit virtual funds
- Withdraw virtual funds
- Simple in-memory data storage (can be upgraded to PostgreSQL)

## Deployment on Railway

1. Fork or clone this repository.
2. Create a new bot via [@BotFather](https://t.me/botfather) on Telegram and copy the token.
3. On Railway, click "New Project" -> "Deploy from GitHub repo" and select this repo.
4. Add the `TELEGRAM_BOT_TOKEN` environment variable with your token.
5. Deploy and start using your bot.

## Local Development

1. Clone the repo: `git clone <your-repo-url>`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your `TELEGRAM_BOT_TOKEN`.
6. Run the bot: `python main.py`

## Important Note

⚠️ This bot is a **simulation**. It is not connected to real banking systems and should not be used to manage real money or financial data [citation:3][citation:8].
