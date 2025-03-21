import logging
import json
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)


BACKEND_URL = "http://localhost:8000"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = "7767127433:AAEW9Gkw8k-th6dSvrW6_o-ci09mgvGXmIg"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text(
        "Hello! I am your interactive chatbot. Send me any message and I will process it!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message when the command /help is issued."""
    await update.message.reply_text("Send me any text and I will process it for you!")


def agent(user_input):
    response = requests.post(
        f"{BACKEND_URL}/agent/",
        params={"query": user_input},
    )
    result = response.json()

    return result["output"]


async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process the user message and return a response."""
    user_input = update.message.text

    processed_output = agent(user_input)

    await update.message.reply_text(processed_output)


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Add message handler for regular text messages
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, process_message)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
