# Standard library imports
import asyncio
import logging
import random

# Third-party imports
from telegram import Bot

# Local imports
from config import ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from database import Database
from sentence_generator import SentenceGenerator

"""
Main entry point for the Dark Thoughts Bot.

This script runs an infinite loop that periodically generates and sends
unique AI-generated sentences to a specified Telegram channel. It handles
database connections, sentence generation, and message delivery while
maintaining proper error logging.
"""

# Configure logging with INFO level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_random_sentence():
    """
    Generate and send a unique sentence to the Telegram channel.
    
    This function:
    1. Initializes database connection
    2. Creates a sentence generator instance
    3. Generates a unique sentence
    4. Saves it to the database
    5. Sends it to the Telegram channel
    
    Exceptions are caught and logged to prevent program termination.
    """
    try:
        # Initialize required components
        db = Database()
        generator = SentenceGenerator(ANTHROPIC_API_KEY, db)
        bot = Bot(TELEGRAM_BOT_TOKEN)

        # Generate and save unique sentence
        sentence = await generator.generate_unique_sentence()
        db.save_sentence(sentence)
        
        # Send to Telegram and log success
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=sentence)
        logger.info(f"Successfully sent message: {sentence}")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")

async def main():
    """
    Main program loop that runs indefinitely.
    
    Continuously generates and sends sentences with random intervals
    between 600 and 6000 seconds (10 to 100 minutes) to prevent predictable
    posting patterns and maintain user engagement.
    """
    while True:
        await send_random_sentence()
        await asyncio.sleep(random.randint(600, 6000))

if __name__ == "__main__":
    # Start the async event loop
    asyncio.run(main())
