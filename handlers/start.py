from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from models import Form
from data_save import user_info
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from data_save import save_user_info

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if user_id in user_info:
        await message.answer("Вы уже зарегистрированы!")
        return
    
    await message.answer('Привет! Введите ФИ (в формате Фамилия Имя):')
    await state.set_state(Form.name)


@router.message(F.text, Form.name)
async def input_name(message: Message, state: FSMContext):
    if len(message.text.split()) != 2 or not all(word[0].isupper() for word in message.text.split()):
        await message.answer("Некоректный ввод! Введите в формате: Фамилия Имя")
        return

    user_id = str(message.from_user.id)
    user_info[user_id] = {'name': message.text}

    age_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="0-18"), KeyboardButton(text="18-25"), KeyboardButton(text="25-50"), KeyboardButton(text="50-75"), KeyboardButton(text="75+")]
        ],
        resize_keyboard=True
    )

    await message.answer("Имя принято! Теперь укажите, сколько вам лет:", reply_markup=age_keyboard)
    await state.set_state(Form.age)

@router.message(F.text, Form.age)
async def input_age(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)

    if message.text not in ['0-18', '18-25', '25-50', '50-75', '75+'] or message.text.isdigit():
        await message.answer("Пожалуйста, выберите из предложенного списка, либо введите целое число:")
        return

    user_info[user_id]['age'] = message.text
    await message.answer('Вы выбрали возраст: ' + user_info[user_id]['age'], reply_markup=ReplyKeyboardRemove())

    gender_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")]
        ],
        resize_keyboard=True
    )

    await message.answer('Теперь укажите ваш пол:', reply_markup=gender_keyboard)
    await state.set_state(Form.gender)

@router.message(F.text, Form.gender)
async def input_gender(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    
    if message.text not in ['Мужской', 'Женский']:
        await message.answer('Пожалуйста, укажите ваш пол (мужской/женский):')
        return

    user_info[user_id]['gender'] = message.text
    user_info[user_id]['feelings'] = '-'

    await message.answer('Вы выбрали пол: ' + user_info[user_id]['gender'], reply_markup=ReplyKeyboardRemove())

    save_user_info()
    await message.answer(
        'Вы успешно зарегистрировались. Теперь я буду вашим персональным помощником в вашем ментальном состоянии.\n'
        'Если у вас возникнут какие-то проблемы или захочется поделиться чем-то радостным, не стесняйтесь написать мне.\n')
    await state.clear()




