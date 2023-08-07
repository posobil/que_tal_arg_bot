import random
from copy import deepcopy
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from keyboards.pagination_kb import create_menu_button, create_course_buttons,\
    create_weeks_buttons, create_days_buttons, create_task_buttons, create_answer_buttons, create_back_button, \
    create_ru_answer_buttons
from lexicon.lexicon import LEXICON, LEXICON_MAIN_BUTTON
from lexicon.words import WORDS_ES_RUS
from services.file_handling import listdict_es_rus, eswords, ruwords
from database.database import user_dict_template, users_db

router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    if 1 > 0:
        await message.answer(LEXICON['/start'], reply_markup=create_menu_button())
    else:
        await message.answer(LEXICON['/guest'], reply_markup=ReplyKeyboardRemove())

@router.message(F.text=='Показать меню ⭐')
async def open_menu(message: Message):
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
    users_db[message.from_user.id]['correct'] = 0
    await message.answer(LEXICON['/menu'], reply_markup=create_course_buttons())


@router.callback_query(Text(text='course_a1'))
async def process_forward_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] = 'Показать меню ⭐'
    page = users_db[callback.from_user.id]['page']
    await callback.message.edit_text(
            text=LEXICON['choise_weeks'],
            reply_markup=create_weeks_buttons(page))

@router.callback_query(Text(text='week_1'))
async def process_forward_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] = 'course_a1'
    page = users_db[callback.from_user.id]['page']
    await callback.message.edit_text(
            text=LEXICON['choise_days'],
            reply_markup=create_days_buttons(page))

@router.callback_query(Text(text='day_1'))
async def process_forward_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] = 'week_1'
    page = users_db[callback.from_user.id]['page']
    await callback.message.edit_text(
            text=LEXICON['choise_type_task'],
            reply_markup=create_task_buttons(page))

@router.callback_query(Text(text='dict1'))
async def process_forward_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] = 'day_1'
    page = users_db[callback.from_user.id]['page']
    await callback.message.edit_text(
            text=listdict_es_rus(WORDS_ES_RUS),
            reply_markup=create_back_button(page))

@router.callback_query(Text(text='esp1'))
async def start_translate_es_ru(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] = 'day_1'
    page = users_db[callback.from_user.id]['page']
    users_db[callback.from_user.id]['correct'] = 0
    users_db[callback.from_user.id]['word'] = 0
    word = eswords[users_db[callback.from_user.id]['word']]
    await callback.message.edit_text(
        text=f'{users_db[callback.from_user.id]["word"] + 1}/{len(eswords)}\n'
             f'{LEXICON["/trans"]}{word}', reply_markup=create_answer_buttons(callback, ruwords))


@router.callback_query(Text(text='correct'))
async def translate_es_ru(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] = 'day_1'
    page = users_db[callback.from_user.id]['page']
    if users_db[callback.from_user.id]['word'] + 1 < len(eswords):
        users_db[callback.from_user.id]['word'] += 1
        users_db[callback.from_user.id]['correct'] += 1
        word = eswords[users_db[callback.from_user.id]['word']]
        await callback.message.edit_text(
            text=f'{users_db[callback.from_user.id]["word"] + 1}/{len(eswords)}\n'
                 f'{LEXICON["/trans_sh"]}{word}', reply_markup=create_answer_buttons(callback, ruwords))
        await callback.answer(text='✅ Верно')
    else:
        users_db[callback.from_user.id]['word'] += 1
        users_db[callback.from_user.id]['correct'] += 1
        await callback.message.edit_text(
            text=f'{LEXICON["finish"]}{users_db[callback.from_user.id]["correct"] } из {len(ruwords)}\n',
            reply_markup=create_back_button(page))
        await callback.answer(text='✅ Верно')

@router.callback_query(Text(text='incorrect'))
async def translate_es_ru_inc(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] = 'day_1'
    page = users_db[callback.from_user.id]['page']
    if users_db[callback.from_user.id]['word'] + 1 < len(eswords):
        users_db[callback.from_user.id]['word'] += 1
        word = eswords[users_db[callback.from_user.id]['word']]
        await callback.message.edit_text(
            text=f'{users_db[callback.from_user.id]["word"] + 1}/{len(eswords)}\n'
                 f'{LEXICON["/trans_sh"]}{word}', reply_markup=create_answer_buttons(callback, ruwords))
        await callback.answer(text='❌ Не верно')
    else:
        users_db[callback.from_user.id]['word'] += 1
        await callback.message.edit_text(
            text=f'{LEXICON["finish"]}{users_db[callback.from_user.id]["correct"] } из {len(ruwords)}\n',
        reply_markup=create_back_button(page))
        await callback.answer(text='❌ Не верно')

@router.callback_query(Text(text='rus1'))
async def start_translate_ru_es(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] = 'day_1'
    users_db[callback.from_user.id]['correct'] = 0
    page = users_db[callback.from_user.id]['page']
    users_db[callback.from_user.id]['word'] = 0
    word = ruwords[users_db[callback.from_user.id]['word']]
    await callback.message.edit_text(
        text=f'{users_db[callback.from_user.id]["word"] + 1}/{len(ruwords)}\n'
             f'{LEXICON["/trans"]}{word}', reply_markup=create_answer_buttons(callback, eswords))

@router.callback_query(Text(text='correct_ru'))
async def translate_ru_es(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] = 'day_1'
    page = users_db[callback.from_user.id]['page']
    if users_db[callback.from_user.id]['word'] + 1 < len(ruwords):
        users_db[callback.from_user.id]['word'] += 1
        users_db[callback.from_user.id]['correct'] += 1
        word = ruwords[users_db[callback.from_user.id]['word']]
        await callback.message.edit_text(
            text=f'{users_db[callback.from_user.id]["word"] + 1}/{len(ruwords)}\n'
                 f'{LEXICON["/trans_sh"]}{word}', reply_markup=create_ru_answer_buttons(callback, eswords))
        await callback.answer(text='✅ Верно')
    else:
        users_db[callback.from_user.id]['word'] += 1
        users_db[callback.from_user.id]['correct'] += 1
        await callback.message.edit_text(
            text=f'{LEXICON["finish"]}{users_db[callback.from_user.id]["correct"] } из {len(eswords)}\n',
            reply_markup=create_back_button(page))
        await callback.answer(text='✅ Верно')


@router.callback_query(Text(text='incorrect_ru'))
async def translate_ru_es_inc(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] = 'day_1'
    page = users_db[callback.from_user.id]['page']
    if users_db[callback.from_user.id]['word'] + 1 < len(ruwords):
        users_db[callback.from_user.id]['word'] += 1
        word = ruwords[users_db[callback.from_user.id]['word']]
        await callback.message.edit_text(
            text=f'{users_db[callback.from_user.id]["word"] + 1}/{len(ruwords)}\n'
                 f'{LEXICON["/trans_sh"]}{word}', reply_markup=create_ru_answer_buttons(callback, eswords))
        await callback.answer(text='❌ Не верно')
    else:
        users_db[callback.from_user.id]['word'] += 1
        await callback.message.edit_text(
            text=f'{LEXICON["finish"]}{users_db[callback.from_user.id]["correct"] } из {len(eswords)}\n',
        reply_markup=create_back_button(page))
        await callback.answer(text='❌ Не верно')




# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])

