from aiogram import Dispatcher
from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    gender = State()
    age = State()
    feelings = State()