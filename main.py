import asyncio
from telegram import Bot
from config import ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from database import Database
from sentence_generator import SentenceGenerator
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_random_sentence():
    try:
        db = Database()
        generator = SentenceGenerator(ANTHROPIC_API_KEY, db)
        bot = Bot(TELEGRAM_BOT_TOKEN)

        sentence = await generator.generate_unique_sentence()
        db.save_sentence(sentence)
        
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=sentence)
        logger.info(f"Successfully sent message: {sentence}")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")

async def main():
    while True:
        await send_random_sentence()
        await asyncio.sleep(random.randint(30, 600))

if __name__ == "__main__":
    asyncio.run(main())
