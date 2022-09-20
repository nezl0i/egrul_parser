import csv
from time import sleep
import requests

url = 'https://egrul.nalog.ru'  # Основной сайт
url_1 = 'https://egrul.nalog.ru/search-result/'     # URL для поиска по ИНН
url_2 = 'https://egrul.nalog.ru/vyp-download/'     # URL для выгрузки pdf (не используется)

s = requests.Session()
s.get(url + '/index.html')

# Файл со списком ИНН
with open('inn.txt', encoding='utf8') as file:
    inn_list = file.readlines()

with open('consumers_1.csv', 'a', newline='') as csvfile:
    fieldnames = ['Наименование', 'Адрес регистрации', 'ИНН', 'КПП',
                  'ОГРН/ОГРНИП', 'Дата присвоения ОГРН', 'Директор']

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    # writer.writeheader()
    count = 1
    # Основной цикл поиска данных по ИНН
    for inn in inn_list:

        inn = inn.strip()
        r = s.post(url, data={'query': inn}, cookies=s.cookies)
        r1 = s.get(url_1 + r.json()['t'], cookies=s.cookies)

        try:
            rows = r1.json()['rows'][0]
            result = {'Наименование': rows.get('n'),
                      'Адрес регистрации': rows.get('a'),
                      'ИНН': rows.get('i'),
                      'КПП': rows.get('p'),
                      'ОГРН/ОГРНИП': rows.get('o'),
                      'Дата присвоения ОГРН': rows.get('r'),
                      'Директор': rows.get('g')
                      }
            values = set(result.values())
            if len(values) > 1:
                writer.writerow(result)
            else:
                with open("invalid.txt", "a", encoding='utf-8') as f:
                    f.write(f'{inn}\n')

            print(f'{count}. {inn} - Done.')
            count += 1
            sleep(2)    # Таймаут между запросами
        except (IndexError, KeyError):
            # Невалидные ИНН пишем в файл
            with open("invalid.txt", "a", encoding='utf-8') as f:
                f.write(f'{inn}\n')

print('Write .csv file done.')
