from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from data_save import user_info, save_user_info
from utils import chain
from models import Form

router = Router()

@router.message(Command('advice'))
async def get_advice(message: Message):
    user_id = str(message.from_user.id)
    if user_id not in user_info:
        await message.answer('Пожалуйста, сначала зарегистрируйтесь.')
        return
    
    user_gender = user_info[user_id]['gender']
    user_age = user_info[user_id]['age']
    user_feelings = user_info[user_id]['feelings']
    
    response = chain.run(user_gender=user_gender, 
                         user_age=user_age, 
                         user_feelings=user_feelings)
    
    await message.answer(response)

@router.message(Command('feelings'))
async def start_feelings(message: Message, state: FSMContext):
    await message.answer('Расскажите, как вы себя чувствуете?')
    await state.set_state(Form.feelings)
    user_id = str(message.from_user.id)

@router.message(Form.feelings)
async def process_feedback(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user_info[user_id]['feelings'] = message.text
    save_user_info()
    await message.answer('Спасибо! Чтобы получить совет напишите команду /advice')
    await state.clear()