from aiogram import Router, F
from aiogram.types import Message
from utils import user_giga_chat_active, user_messages, ask_gigachat

router = Router()

@router.message(F.text)
async def handle_giga_chat(message: Message):
    user_id = message.from_user.id
    if user_id not in user_giga_chat_active or not user_giga_chat_active[user_id]:
        await message.answer("Для начала общения с ИИ ГигаЧат используйте команду /chat_with_giga.")
        return
    
    user_message = message.text

    if user_id not in user_messages:
        user_messages[user_id] = [
            {"role": "system", "content": "Ты психолог, который помогает пользователю с его ментальными проблемами, отвечает на вопросы и поддерживает."}
        ]

    user_messages[user_id].append({"role": "user", "content": user_message})

    assistant_reply = ask_gigachat(user_messages[user_id])
    print(user_messages)

    if assistant_reply:
        user_messages[user_id].append({"role": "assistant", "content": assistant_reply})
        await message.answer(assistant_reply)
    else:
        await message.answer("Произошла ошибка при обращении к ИИ. Попробуйте позже.")
