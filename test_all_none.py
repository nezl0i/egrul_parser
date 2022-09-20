result = {'Наименование': None,
          'Адрес регистрации': None,
          'ИНН': None,
          'КПП': None,
          'ОГРН/ОГРНИП': 4,
          'Дата присвоения ОГРН': None,
          'Директор': None
          }

values = set(result.values())
print(values)

if len(values) == 1:
    print('OK')
