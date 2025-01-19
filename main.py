import logging
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from handlers import chat, start, messages
from config import TELEGRAM_TOKEN
from data_save import dp, user_actions



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def start_bot():
    commands = [
        BotCommand(command='start', description='Начать'),
        BotCommand(command='chat_with_giga', description='Пообщаться'),
        BotCommand(command='end_chat_with_giga', description='Устал общаться'),
    ]

    await bot.set_my_commands(commands)
    logger.info("Команды зарегистрированы.")

async def main():
    user_actions()
    dp.include_routers(start.router, chat.router, messages.router)
    dp.startup.register(start_bot)

    try:
        print("Бот запущен...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    finally:
        await bot.session.close()
        print("Бот остановлен")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())