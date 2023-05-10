from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


class DefKey:
    yes_abs = InlineKeyboardButton(text='Точно да', callback_data='1')
    yes_noabs = InlineKeyboardButton(text='Скорее да', callback_data='2')
    no_noabs = InlineKeyboardButton(text='Скорее нет', callback_data='3')
    no_abs = InlineKeyboardButton(text='Точно нет', callback_data='4')
    undefined_button = InlineKeyboardButton(text='Затрудняюсь ответить', callback_data='0')
    keyboard: list[list[InlineKeyboardButton]] = [[yes_abs], [yes_noabs], [no_noabs], [no_abs], [undefined_button]]

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)


class GenKey:
    male_button = InlineKeyboardButton(text='Мужской ♂', callback_data='м')
    female_button = InlineKeyboardButton(text='Женский ♀', callback_data='ж')
    keyboard: list[list[InlineKeyboardButton]] = [[male_button, female_button]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)


class AgeKey:
    young = InlineKeyboardButton(text='18-25', callback_data='1')
    post_young = InlineKeyboardButton(text='25-35', callback_data='2')
    adult = InlineKeyboardButton(text='35-50', callback_data='3')
    old = InlineKeyboardButton(text='50+', callback_data='4')
    keyboard = [[young, post_young, adult, old]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)


# class BasedKey:
#     b1 = KeyboardButton(text='Точно да', callback_data='1')
#     b2 = KeyboardButton(text='Скорее да', callback_data='2')
#     b3 = KeyboardButton(text='Скорее нет', callback_data='3')
#     b4 = KeyboardButton(text='Точно нет', callback_data='4')
#     b5 = KeyboardButton(text='Точно да', callback_data='0')
#
#     keyboard = ReplyKeyboardMarkup(keyboard=[[b1], [b2], [b3], [b4], [b5]], resize_keyboard=True)


