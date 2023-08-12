import os
import random
from lexicon.words import WORDS_ES_RUS, Day_1_task_2
import gspread

dict_esrus = WORDS_ES_RUS
eswords: list = []
ruwords: list = []
table_link = 'https://docs.google.com/spreadsheets/d/14M-0SLkZCyyLreBE2-Ia7v4olg5LVsqWXl-F_pPtRAk/edit#gid=0'
page_name = 'day1_1'

# Метод принимает ссылку на гугл таблицу и название страницы
# возвращает 2 списка из первого и второго столбцов выбранной страницы
def get_words_lists_gtable(table_link, page_name):
    gc = gspread.service_account(filename='qta.json')
    sh = gc.open_by_url(table_link)
    worksheet = sh.worksheet(page_name)
    es_w = worksheet.col_values(1)
    ru_w = worksheet.col_values(2)
    return es_w, ru_w


# Преобразую в строку для вывода всего набора слов
def listdict_es_rus(es_list, ru_list):
    ll = ''
    for i in range(len(es_list)):
        ll = ll + (f'{es_list[i]} - {ru_list[i]}\n')
    return ll

# функция принимае массив и возвращает 2 списка слов
def get_es_rus_lists(dict):
    es_words: list = []
    ru_words: list = []
    for key, value in dict.items():
        es_words.append(key)
        ru_words.append(value)
    return es_words, ru_words

def get_ru_es(ru_list, es_list):
    dict_ru_es = {}
    for i in range(len(ru_list)):
        dict_ru_es[ru_list[i]] = es_list[i]
    return dict_ru_es


# функция принимает выбранное корректное слово и список слов
# возвращает словарь с корректным словом и 3я рандомными(с сортировкой)
def get_random_word(correct_word, words):
    words_dict: dict[str, str] = {}
    words_dict[correct_word] = 'correct'
    while True:
        number = random.randint(0, len(words) - 1)
        if correct_word != words[number]:
            words_dict[words[number]] = 'incorrect'
            if len(words_dict) == 4:
                break
    sort_words = sorted(words_dict.items())
    return dict(sort_words)

def get_random_word_ru(correct_word, words):
    words_dict: dict[str, str] = {}
    words_dict[correct_word] = 'correct'
    print(correct_word)
    while True:
        number = random.randint(0, len(words) - 1)
        if correct_word != words[number]:
            words_dict[words[number]] = 'incorrect'
            if len(words_dict) == 4:
                break
    sort_words = sorted(words_dict.items())
    return dict(sort_words)

def get_random_task_3(correct_word, words):
    words_dict: dict[str, str] = {}
    words_dict[correct_word] = 'right'
    while True:
        number = random.randint(0, len(words) - 1)
        if correct_word != words[number]:
            words_dict[words[number]] = 'wrong'
            if len(words_dict) == 4:
                break
    sort_words = sorted(words_dict.items())
    return dict(sort_words)

eswords, ruwords = get_es_rus_lists(WORDS_ES_RUS)
estask2, esansw2 = get_es_rus_lists(Day_1_task_2)
