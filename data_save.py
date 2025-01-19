from pathlib import Path
import csv
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram import types, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime
from models import Form

dp = Dispatcher(storage=MemoryStorage())

USER_INFO = Path('user_info.csv')
USER_ACTIVITIES = Path('user_activities.csv')

def read_user_info():
    user_info = {}
    if USER_INFO.exists():
        with open(USER_INFO, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for line in reader:
                user_id, name, gender, age, feelings = line
                user_info[user_id] = {
                    'name': name,
                    'gender': gender,
                    'age': age,
                    'feelings': feelings
                }
    return user_info

def save_user_info():
    with open(USER_INFO, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for user_id, info in user_info.items():
            writer.writerow([user_id, info['name'], info['gender'], info['age'], info['feelings']])

def update(user_id, info):
    if user_id in user_info:
        for key in info:
            user_info[key] = info[key]
        
        save_user_info()


user_info = read_user_info()

def user_actions():
    if not USER_ACTIVITIES.exists():
        with open(USER_ACTIVITIES, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'timestamp', 'message'])

class Middleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, types.Update) and event.message:
            user_id = str(event.message.from_user.id)
            state = await data['state'].get_state()
            print(Form, state)
            message = event.message.text
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(USER_ACTIVITIES, "a", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([user_id, timestamp, message])
            
            if event.message.text == '/start':
                return await handler(event, data)
            
            if state in [Form.name.state, Form.age.state, Form.gender.state]:
                return await handler(event, data)
            
            if user_id not in user_info:
                await data['bot'].send_message(user_id,
                    "Вы не зарегистрированы. Пожалуйста, используйте команду /start для регистрации.")
                return
            
        return await handler(event, data)

dp.update.middleware(Middleware())

