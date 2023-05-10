from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter, Text
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
import os
from keyboards.keyboard_menu import DefKey, GenKey, AgeKey
from lexicon.lexicon_ru import welcome_text
from models import methods as mt
import aioredis
from dotenv import load_dotenv
from aiogram.fsm.storage.redis import RedisStorage


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

bot: Bot = Bot(os.environ.get('API_TOKEN'))
redis = aioredis.from_url(os.environ.get('REDISURL'))
storage: RedisStorage = RedisStorage(redis=redis)
dp: Dispatcher = Dispatcher(storage=storage)
user_dict = {}


class Question(StatesGroup):
    starting = State()
    is_alc = State()
    like_k = State()
    cook_k = State()
    know_rec = State()
    gender = State()
    age = State()


@dp.message(Command(commands='start'), StateFilter(default_state))
async def starting_comm(msg: Message, state: FSMContext):
    if len(mt.get_data(msg.from_user.id)) == 0:
        await msg.answer(text=welcome_text)
        await state.set_state(Question.starting)
    else:
        await msg.answer('Вы уже прошли опрос, спасибо за ваши ответы!')


@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def cancel_comm(msg: Message, state: FSMContext):
    await msg.answer(text="Вы отменили прохождение опроса\n\n"
                          "Чтобы вернуться, отправьте /start")
    await state.clear()


@dp.message(Command(commands='cancel'))
async def cancel_comm(msg: Message):
    await msg.answer(text="Вы уже отменили прохождение опроса ранее\n\n"
                          "Чтобы вернуться, отправьте /start")


@dp.message(Command(commands='poll'), StateFilter(Question.starting))
async def polling_starting(msg: Message, state: FSMContext):
    yes_button = InlineKeyboardButton(text='Да',
                                      callback_data='1')
    no_button = InlineKeyboardButton(text='Нет',
                                     callback_data='no')
    undefined_button = InlineKeyboardButton(text='Затрудняюсь ответить',
                                            callback_data='0')
    keyboard: list[list[InlineKeyboardButton]] = [[yes_button, no_button],
                                                  [undefined_button]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await msg.answer(text='Употребляете ли вы алкоголь?', reply_markup=markup)
    await state.set_state(Question.is_alc)


@dp.callback_query(StateFilter(Question.is_alc), Text(text='no'))
async def stop_polling(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Спасибо за прохождение опроса!')
    await state.clear()


@dp.callback_query(StateFilter(Question.is_alc), Text(text=['1', '0']))
async def do_you_like(callback: CallbackQuery, state: FSMContext):
    await state.update_data(is_alc=callback.data)
    await callback.message.edit_text(text='Нравятся ли вам алкогольные коктейли?',
                                  reply_markup=DefKey.markup)
    await state.set_state(Question.like_k)


@dp.callback_query(StateFilter(Question.like_k), Text(text=[str(i) for i in range(5)]))
async def cooking_time(callback: CallbackQuery, state: FSMContext):
    await state.update_data(like_k=callback.data)
    await callback.message.edit_text(text='Нравится ли вам готовить алкогольные коктейли?',
                                     reply_markup=DefKey.markup)
    await state.set_state(Question.cook_k)


@dp.callback_query(StateFilter(Question.cook_k), Text(text=[str(i) for i in range(5)]))
async def she_know(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cook_k=callback.data)
    await callback.message.edit_text(text='Хотели бы узнать больше рецептов '
                                          'для вашего домашнего бара?',
                                     reply_markup=DefKey.markup)
    await state.set_state(Question.know_rec)


@dp.callback_query(StateFilter(Question.know_rec), Text(text=[str(i) for i in range(5)]))
async def gender_reveal(callback: CallbackQuery, state: FSMContext):
    await state.update_data(know_rec=callback.data)
    await callback.message.edit_text(text='Укажите ваш пол', reply_markup=GenKey.markup)
    await state.set_state(Question.gender)


@dp.callback_query(StateFilter(Question.gender), Text(text=['м', 'ж']))
async def age_rev(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    await callback.message.edit_text(text='Введите ваш возраст', reply_markup=AgeKey.markup)
    await state.set_state(Question.age)


@dp.callback_query(StateFilter(Question.age), Text(text=[str(i) for i in range(1, 5)]))
async def process_age_sent(callback: CallbackQuery, state: FSMContext):
    await state.update_data(age=callback.data)
    await callback.message.answer('Спасибо за прохождение опроса!')
    await callback.message.delete()
    user_dict[callback.from_user.id] = await state.get_data()
    mt.insert_cus(callback.from_user.id, user_dict[callback.from_user.id]['gender'],
                  user_dict[callback.from_user.id]['age'])
    mt.insert_fp(callback.from_user.id, user_dict[callback.from_user.id]['is_alc'],
                 user_dict[callback.from_user.id]['like_k'],
                 user_dict[callback.from_user.id]['cook_k'], user_dict[callback.from_user.id]['know_rec'])
    await state.clear()


if __name__ == '__main__':
    dp.run_polling(bot)
