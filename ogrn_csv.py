# Парсер информации о контрагентах по ИНН с сайта https://egrul.nalog.ru
# https://github.com/nezl0i/egrul_parser

import csv
import requests
from time import sleep

url = 'https://egrul.nalog.ru'  # Основной сайт
url_1 = 'https://egrul.nalog.ru/search-result/'  # URL для поиска по ИНН
url_2 = 'https://egrul.nalog.ru/vyp-download/'  # URL для выгрузки pdf (не используется)

inn_file = 'inn.txt'  # Файл со списком ИНН
invalid_file = 'invalid.txt'  # Файл для не валидных ИНН
consumers_file = 'consumers_2.csv'  # Файл с результатом парсинга

fieldnames = ['Наименование', 'Адрес регистрации', 'ИНН', 'КПП',
              'ОГРН/ОГРНИП', 'Дата присвоения ОГРН', 'Директор']

count = 1

s = requests.Session()
s.get(url + '/index.html')


# Запись в файл не валидных ИНН
def set_invalid(invalid_inn):
    with open(invalid_file, "a", encoding='utf-8') as f:
        f.write(f'{invalid_inn}\n')


# Основной запрос к сайту с установкой cookie (мы же честные ;) )
def set_cookie(valid_inn):
    r = s.post(url, data={'query': valid_inn}, cookies=s.cookies)
    return s.get(url_1 + r.json()['t'], cookies=s.cookies)


# Запись в файл информации по валидным ИНН
def write_valid(result_info: dict):
    with open(consumers_file, 'a', encoding='utf8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        # writer.writeheader()  # Заголовок csv файла.
        writer.writerow(result_info)


# Формируем список ИНН
with open(inn_file, encoding='utf8') as file:
    inn_list = file.readlines()

# Основной цикл поиска данных по ИНН
for inn in inn_list:

    inn = inn.strip()
    r1 = set_cookie(inn)

    try:
        rows = r1.json()['rows'][0]
        result = {
            fieldnames[0]: rows.get('n'),
            fieldnames[1]: rows.get('a'),
            fieldnames[2]: rows.get('i'),
            fieldnames[3]: rows.get('p'),
            fieldnames[4]: rows.get('o'),
            fieldnames[5]: rows.get('r'),
            fieldnames[6]: rows.get('g')
        }

        values = set(result.values())

        if len(values) > 1:
            write_valid(result)
            print(f'{count}. {inn} - Done.')
        else:
            set_invalid(inn)
            print(f'{count}. {inn} - Invalid.')

        count += 1

        # Таймаут между запросами
        sleep(2)

    except (IndexError, KeyError):
        # Не валидные ИНН пишем в файл
        set_invalid(inn)

print('Write .csv file is done.')
