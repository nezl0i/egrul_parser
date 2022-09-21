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
consumers_file = 'consumers.csv'  # Файл с результатом парсинга

s = requests.Session()
s.get(url + '/index.html')


def set_invalid(invalid_inn):
    with open(invalid_file, "a", encoding='utf-8') as f:
        f.write(f'{invalid_inn}\n')


# Файл со списком ИНН
with open(inn_file, encoding='utf8') as file:
    inn_list = file.readlines()

with open(consumers_file, 'a', newline='') as csvfile:
    fieldnames = ['Наименование', 'Адрес регистрации', 'ИНН', 'КПП',
                  'ОГРН/ОГРНИП', 'Дата присвоения ОГРН', 'Директор']

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    # writer.writeheader()  # Заголовок csv файла. Для первого запуска скрипта, раскомментировать.
    count = 1

    # Основной цикл поиска данных по ИНН
    for inn in inn_list:

        inn = inn.strip()
        r = s.post(url, data={'query': inn}, cookies=s.cookies)

        '''Здесь можно нарваться на KeyError. Вероятно ошибка на стороне
        сервера. Обрабатывать исключение не нужно, просто повторно запустить
        скрипт.
        '''
        r1 = s.get(url_1 + r.json()['t'], cookies=s.cookies)

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
                writer.writerow(result)
            else:
                set_invalid(inn)

            print(f'{count}. {inn} - Done.')
            count += 1
            sleep(2)  # Таймаут между запросами

        except (IndexError, KeyError):
            # Невалидные ИНН пишем в файл
            set_invalid(inn)

print('Write .csv file is done.')
