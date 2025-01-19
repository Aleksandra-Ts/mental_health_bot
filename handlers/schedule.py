import asyncio
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from config import TELEGRAM_TOKEN
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from data_save import user_info

bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

daily_exercises = [
    "Дыхательное упражнение: Сидите удобно, закройте глаза и сосредоточьтесь на дыхании. Дышите глубоко и медленно.",
    "Медитация: Сидите удобно, закройте глаза и сосредоточьтесь на настоящем моменте. Пусть ваши мысли проходят мимо, не задерживаясь на них.",
    "Осознанное движение: Занимайтесь йогой или просто ходите, сосредотачиваясь на ощущениях в теле.",
]

async def send_daily_exercise():
    exercise = random.choice(daily_exercises)
    
    for user_id in user_info.keys():
        try:
            await bot.send_message(user_id, exercise)
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

async def send_daily_reminder():
    for user_id in user_info.keys():
        try:
            await bot.send_message(user_id, "Время отметить свое самочувствие! Используйте команду /feelings")
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

scheduler = AsyncIOScheduler()

scheduler.add_job(send_daily_exercise, "cron", hour=8, minute=0)
scheduler.add_job(send_daily_exercise, "cron", hour=20, minute=0)
scheduler.add_job(send_daily_reminder, "cron", hour=12, minute=0)