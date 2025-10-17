import asyncio
import logging
import os
from typing import Optional

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message, ReactionTypeEmoji, User
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
REACTION_EMOJI = os.getenv("REACTION_EMOJI")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is required")

if not REACTION_EMOJI or not REACTION_EMOJI.strip():
    raise RuntimeError("REACTION_EMOJI environment variable must be a non-empty emoji")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("reaction-bot")

dispatcher = Dispatcher()
router = Router()
dispatcher.include_router(router)

_bot_identity: Optional[User] = None


# Cache bot identity once during startup so we can avoid reacting to our own messages.
@dispatcher.startup.register
async def cache_bot_identity(bot: Bot) -> None:
    global _bot_identity
    _bot_identity = await bot.get_me()
    logger.info("Bot online as @%s reacting with %s", _bot_identity.username, REACTION_EMOJI)


@router.message()
async def react_to_message(message: Message, bot: Bot) -> None:
    if message.chat.type == ChatType.CHANNEL and not message.chat.is_forum:
        return

    author_id = message.from_user.id if message.from_user else None
    if _bot_identity and author_id == _bot_identity.id:
        return

    reaction = ReactionTypeEmoji(emoji=REACTION_EMOJI)

    try:
        # Apply the configured emoji reaction to every incoming message.
        await bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id, reaction=[reaction])
    except TelegramAPIError as error:
        logger.warning("Failed to react in chat %s message %s: %s", message.chat.id, message.message_id, error)


async def main() -> None:
    bot = Bot(BOT_TOKEN)
    await dispatcher.start_polling(bot, allowed_updates=["message"])


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
