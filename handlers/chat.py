from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from utils import user_giga_chat_active, user_messages

router = Router()

@router.message(Command("chat_with_giga")) 
async def chat_with_giga(message: Message): 
    print("Команда /chat_with_giga вызвана.") 
    user_id = message.from_user.id 
 
    if user_id in user_giga_chat_active and user_giga_chat_active[user_id]: 
        await message.answer("Вы уже находитесь в чате с ИИ ГигаЧат. Напишите ваше сообщение:") 
        return 
    user_giga_chat_active[user_id] = True 
    if user_id not in user_messages: 
        user_messages[user_id] = [] 
    await message.answer("Вы можете начать общение с ИИ ГигаЧат. Напишите ваше сообщение:") 
 
 
@router.message(Command("end_chat_with_giga")) 
async def end_chat_with_giga(message: Message): 
    print("Команда /end_chat_with_giga вызвана.") 
    user_id = message.from_user.id 
     
    if user_id in user_giga_chat_active and user_giga_chat_active[user_id]: 
        user_giga_chat_active[user_id] = False 
        await message.answer("Вы завершили общение с ИИ ГигаЧат. Если захотите поговорить снова, используйте команду /chat_with_giga.") 
    else: 
        await message.answer("Вы не находитесь в чате с ИИ ГигаЧат. Используйте команду /chat_with_giga для начала общения.")
