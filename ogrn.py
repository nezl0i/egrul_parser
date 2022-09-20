from time import sleep

import requests

url = 'https://egrul.nalog.ru'
url_1 = 'https://egrul.nalog.ru/search-result/'
url_2 = 'https://egrul.nalog.ru/vyp-download/'
# inn = 7777777778

s = requests.Session()
s.get(url + '/index.html')
# print(s.cookies)

with open('inn.txt', encoding='utf8') as file:
    inn_list = file.readlines()


for inn in inn_list:
    inn = inn.strip()
    r = s.post(url, data={'query': inn}, cookies=s.cookies)
    # print(r.json()['t'])

    r1 = s.get(url_1 + r.json()['t'], cookies=s.cookies)
    # print(type(r1.json()['rows'][0]))
    try:
        result = f"{'='*30} {inn} {'='*30}\n" \
                 f"Наименование: {r1.json()['rows'][0].get('n')}\n" \
                 f"Адрес регистрации: {r1.json()['rows'][0].get('a', None)}\n" \
                 f"ИНН: {r1.json()['rows'][0].get('i')}\n" \
                 f"КПП: {r1.json()['rows'][0].get('p')}\n" \
                 f"ОГРН/ОГРНИП: {r1.json()['rows'][0].get('o')}\n" \
                 f"Дата присвоения ОГРН: {r1.json()['rows'][0].get('r')}\n" \
                 f"Директор: {r1.json()['rows'][0].get('g')}\n"

        with open("result_3.txt", "a", encoding='utf-8') as f:
            f.write(result)

        # print(r1.json()['rows'][0].get('n'))    # Полное наименование
        # print(r1.json()['rows'][0].get('a'))    # Адрес регистрации
        # print(f"ИНН: {r1.json()['rows'][0].get('i')}")  # ИНН
        # print(f"КПП: {r1.json()['rows'][0].get('p')}")  # КПП
        # print(f"ОГРН: {r1.json()['rows'][0].get('o')}")     # ОГРН
        # print(f"Дата присвоения ОГРН: {r1.json()['rows'][0].get('r')}")     # Дата регистрации
        # print(r1.json()['rows'][0].get('g'))    # Руководитель
        print(f'{inn} - Done.')
        sleep(2)
    except (IndexError, KeyError):
        # Невалидные ИНН пишем в файл
        with open("invalid.txt", "a", encoding='utf-8') as f:
            f.write(f'{inn}\n')


# print(r1.json()['rows'][0]['t'])

# r2 = s.get(url_2 + r1.json()['rows'][0]['t'], cookies=s.cookies)
# print(r2.content)
# sleep(2)
# with open(f'{r1.json()["rows"][0]["n"]}_{str(inn)}.pdf', 'wb') as f:
#     f.write(r2.content)
