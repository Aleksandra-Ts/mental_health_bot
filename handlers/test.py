from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackQuery
from aiogram.filters import Command

router = Router()

questions = [
    {
        "question": "Как вы обычно реагируете на конфликт с другом?",
        "answers": [
            {"text": "Пытаюсь понять точку зрения друга и найти компромисс.", "id": "q1_a1"},
            {"text": "Пытаюсь доказать свою правоту.", "id": "q1_a2"},
            {"text": "Избегаю конфликта.", "id": "q1_a3"},
            {"text": "Злюсь и обижаюсь.", "id": "q1_a4"}
        ]
    },
    {
        "question": "Как вы справляетесь со стрессом?",
        "answers": [
            {"text": "Занимаюсь спортом или медитацией.", "id": "q2_a1"},
            {"text": "Обсуждаю с друзьями или семьей.", "id": "q2_a2"},
            {"text": "Пытаюсь решить проблему самостоятельно.", "id": "q2_a3"},
            {"text": "Чувствую себя перегруженным и не знаю, что делать.", "id": "q2_a4"}
        ]
    },
    {
        "question": "Как вы относитесь к критике?",
        "answers": [
            {"text": "Принимаю конструктивную критику и использую ее для улучшения.", "id": "q3_a1"},
            {"text": "Чувствую себя обиженным, но пытаюсь понять.", "id": "q3_a2"},
            {"text": "Злюсь и защищаюсь.", "id": "q3_a3"},
            {"text": "Игнорирую критику.", "id": "q3_a4"}
        ]
    }
]

answer_map = {}
for i, question in enumerate(questions):
    for answer in question["answers"]:
        answer_map[answer["id"]] = answer["text"]

user_answers = {}

current_question = 0

@router.message(Command("emotional_intelligence_test"))
async def start_test(message: Message):
    global current_question
    user_id = message.from_user.id
    user_answers[user_id] = []
    
    buttons = []
    for answer in questions[current_question]["answers"]:
        buttons.append([InlineKeyboardButton(text=answer["text"], callback_data=answer["id"])])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await message.answer(questions[current_question]["question"], reply_markup=keyboard)

@router.callback_query()
async def handle_answer(query: CallbackQuery):
    global current_question
    user_id = query.from_user.id
    user_answer_id = query.data
    user_answer = answer_map[user_answer_id]
    
    user_answers[user_id].append(user_answer)
    
    if current_question < len(questions) - 1:
        current_question += 1
        
        buttons = []
        for answer in questions[current_question]["answers"]:
            buttons.append([InlineKeyboardButton(text=answer["text"], callback_data=answer["id"])])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await query.answer()
        await query.message.edit_text(questions[current_question]["question"], reply_markup=keyboard)
    else:
        await query.answer()
        await query.message.edit_text("Тест завершен. Результаты:")
        
        score = 0
        for i, answer in enumerate(user_answers[user_id]):
            if i == 0 and answer == questions[i]["answers"][0]["text"]:
                score += 1
            elif i == 1 and answer == questions[i]["answers"][0]["text"]:
                score += 1
            elif i == 2 and answer == questions[i]["answers"][0]["text"]:
                score += 1
        
        if score == 3:
            await query.message.answer("Вы обладаете высоким эмоциональным интеллектом. Вы хорошо справляетесь с конфликтами, стрессом и критикой.")
        elif score == 2:
            await query.message.answer("У вас средний уровень эмоционального интеллекта. Вы можете улучшить свои навыки в некоторых областях.")
        else:
            await query.message.answer("У вас низкий уровень эмоционального интеллекта. Рекомендуется работать над улучшением навыков в области конфликтов, стресса и критики.")
        
        current_question = 0
