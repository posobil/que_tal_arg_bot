
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from services.file_handling import get_random_word, get_random_word_ru
from database.database import users_db


def create_menu_button() -> ReplyKeyboardBuilder:
    # Кнопка показать меню
    # Инициализируем билдер
    menu_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    # Создаем список с кнопками
    menu_button = KeyboardButton(text='Показать меню ⭐')
    # Распаковываем список с кнопками в билдер, указываем, что
    # в одном ряду должно быть 4 кнопки
    menu_builder.row(menu_button)
    return menu_builder.as_markup(resize_keyboard=True)

def create_course_buttons() -> InlineKeyboardMarkup:
    # создаю клавиатуру с выбором курсов
    course_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    course_builder.row(*[InlineKeyboardButton(text=f'Курс A{i}', callback_data=f'course_a{i}') for i in range(1,3)], width=1)
    return course_builder.as_markup(resize_keyboard=True)

def create_weeks_buttons(page) -> InlineKeyboardMarkup:
    # создаю клавиатуру с выбором курсов
    weeks_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    weeks_builder.row(*[InlineKeyboardButton(text=f'Неделя {i}', callback_data=f'week_{i}') for i in range(1,5)], width=1)
    return weeks_builder.as_markup(resize_keyboard=True)

def create_days_buttons(page) -> InlineKeyboardMarkup:
    # создаю клавиатуру с выбором курсов
    days_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    back_button: InlineKeyboardButton = InlineKeyboardButton(text='Назад ⬅️', callback_data=f'{page}')
    days_builder.row(*[InlineKeyboardButton(text=f'День {i}', callback_data=f'day_{i}') for i in range(1,6)], width=1)
    days_builder.row(back_button, width=1)
    return days_builder.as_markup(resize_keyboard=True)

def create_task_buttons(page) -> InlineKeyboardMarkup:
    # создаю клавиатуру с выбором курсов
    tasks_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    button_dict: InlineKeyboardButton = InlineKeyboardButton(text='Показать список слов 📃',
                                                              callback_data='dict1')
    button_esrus : InlineKeyboardButton = InlineKeyboardButton(text='Переведи слово Español-Русский 🇦🇷🇷🇺',
                                                               callback_data='esp1')
    button_ruses: InlineKeyboardButton = InlineKeyboardButton(text='Переведи слово Русский-Español 🇷🇺🇦🇷',
                                                              callback_data='rus1')
    button_estask: InlineKeyboardButton = InlineKeyboardButton(text='Выбери форму глагола 🇦🇷',
                                                              callback_data='esp1pr')
    back_button: InlineKeyboardButton = InlineKeyboardButton(text='Назад ⬅️', callback_data=f'{page}')
    tasks_builder.row(button_dict, width=1)
    tasks_builder.row(button_esrus, width=1)
    tasks_builder.row(button_ruses, width=1)
    tasks_builder.row(button_estask, width=1)
    tasks_builder.row(back_button, width=1)
    return tasks_builder.as_markup(resize_keyboard=True)

def create_answer_buttons(callback: CallbackQuery, ruwords) -> InlineKeyboardMarkup:
    # создаю клавиатуру с выбором ответа
    word = ruwords[users_db[callback.from_user.id]['word']]
    days_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    l = get_random_word(word, ruwords)
    days_builder.row(*[InlineKeyboardButton(text=f'{key}', callback_data=f'{value}') for key, value in l.items()], width=1)
    return days_builder.as_markup(resize_keyboard=True)

def create_ru_answer_buttons(callback: CallbackQuery, eswords) -> InlineKeyboardMarkup:
    # создаю клавиатуру с выбором ответа
    word = eswords[users_db[callback.from_user.id]['word']]
    ru_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    l = get_random_word_ru(word, eswords)
    ru_builder.row(*[InlineKeyboardButton(text=f'{key}', callback_data=f'{value}') for key, value in l.items()], width=1)
    return ru_builder.as_markup(resize_keyboard=True)

def create_back_button(page) -> InlineKeyboardMarkup:
    # создаю кнопку назад
    days_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    back_button: InlineKeyboardButton = InlineKeyboardButton(text='Назад ⬅️', callback_data=f'{page}')
    days_builder.row(back_button, width=1)
    return days_builder.as_markup(resize_keyboard=True)





