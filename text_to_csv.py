import csv
from itertools import zip_longest

tmp = []
result = []

csv.register_dialect('myDialect', quoting=csv.QUOTE_NONNUMERIC, delimiter=';')


def chunk(lst):
    n = len(lst) // 7
    return list(x for x in zip_longest(*[iter(lst)] * n))
    # _ = iter(lst)
    # return list(zip_longest(_, _, _, _, _, _, _))


with open('result_1.txt', encoding='utf8') as file:
    inn_list = file.readlines()

for item in inn_list:
    if item.startswith('=='):
        continue

    tmp.append(item.split(':')[1].lstrip())
result = [tmp[i:i + 7] for i in range(0, len(tmp), 7)]
print(result)
fieldnames = ['Наименование', 'Адрес регистрации', 'ИНН', 'КПП',
              'ОГРН/ОГРНИП', 'Дата присвоения ОГРН', 'Директор']

with open('result_1.csv', 'w', encoding='cp1251') as f:
    write = csv.writer(f, dialect='myDialect')

    write.writerow(fieldnames)
    write.writerows(result)
print('Done')



