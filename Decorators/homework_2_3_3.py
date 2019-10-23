from decorators.decorator import log_decorator

documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
    {"type": "insurance", "number": "1", 'name': 'Кто-то'}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}


# проверка на наличие полки
def doc_search(change_shelf, shelf):
    if change_shelf not in shelf.keys():
        return False
    return True


# p – people – команда, которая спросит номер документа и выведет имя человека, которому он принадлежит
def find_people(doc):
    document_number = input("Введите номер документа: ")
    for document in doc:
        if document_number == document['number']:
            return print('Владелец документа: {}'.format(document['name']))
    return print('Такого документа не существует. Повторите команду')


# l– list – команда, которая выведет список всех документов в формате passport "2207 876234" "Василий Гупкин"
@log_decorator('/Users/antongrutsin/Desktop/Python/advanced_python/Decorators/logs/log2.txt')
def info_list(doc):
    for document in doc:
        print('{} "{}" "{}"'.format(document['type'], document['number'], document['name']))


# s – shelf – команда, которая спросит номер документа и выведет номер полки, на которой он находится
def find_shelf(shelf):
    document_number = input("Введите номер документа: ")
    for direct_key, direct_value in shelf.items():
        if document_number in direct_value:
            return print('Номер полки: {}'.format(direct_key))
    return print('Такого документа не существует. Повторите команду')


# a – add – команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип, имя владельца и номер полки, на котором он будет храниться.
def add(doc, shelf):
    people_number_doc = input('Введите номер документа: ')
    for direct_key, direct_value in shelf.items():
        if people_number_doc in direct_value:
            return print('Такой номер документа уже существует в базе')

    people_type_doc = input('Введите тип документа: ')
    people_name = input('Введите имя владельца: ')
    shelf_number = input('Введите номер полки для хранения: ')
    if doc_search(shelf_number, shelf) == False:
        return print('\nТакой полки не существует.\nНеобходима существующая полка для этой команды')

    shelf[shelf_number].append(people_number_doc)
    doc.append(dict(type=people_type_doc, number=people_number_doc, name=people_name))

    print('\nДанные добавлены в каталог.\nПолка зарезервирована.')


# d – delete – команда, которая спросит номер документа и удалит его из каталога и из перечня полок
def delete(doc, shelf):
    doc_num = input('Введите номер документа для удаления: ')

    for count, document in enumerate(doc):
        if doc_num == document['number']:
            doc.pop(count)
            print('\nЗапись удалена из каталога.')

    for direct_key, direct_value in shelf.items():
        if doc_num in direct_value:
            direct_value.remove(doc_num)
            print('Документ убран с полки.')
    return print('\nТакого документа не существует.')


# m – move – команда, которая спросит номер документа и целевую полку и переместит его с текущей полки на целевую
def move(shelf):
    doc_number = input('Введите номер документа: ')
    change_shelf = input('Введите целевую полку: ')
    if doc_search(change_shelf, shelf) == False:
        return print('\nТакой полки не существует.\nНеобходима существующая полка для этой команды')
    for direct_key, direct_value in shelf.items():
        for inter, document in enumerate(direct_value):
            if document == doc_number:
                if direct_key == change_shelf:
                    return print('Документ уже в этой папке.\nВведите другую команду:')
                else:
                    shelf[change_shelf].append(direct_value.pop(inter))
                    return print('Документ {} перемещен на полку {}'.format(doc_number, change_shelf))
        return print('Такого документа не существует')

    # as – add shelf – команда, которая спросит номер новой полки и добавит ее в перечень


def add_shelf(shelf):
    new_shelf = input('Введите номер новой полки: ')
    if doc_search(new_shelf, shelf) == False:
        shelf.setdefault(new_shelf, [])
        return print('Полка под номером {} добавлена'.format(new_shelf))
    return print('\nТакая полка уже сущетсвует.\nВведите новую команду')

# n– name – вывод имен всех владельцев документов и обработка исключения KeyError
def name(doc):
    try:
        for document in doc:
            print('Документ {} принадлежит {}'.format(document['number'], document['name']))
    except KeyError:
        print()
        print('Документ {} не имеет владельца'.format(document['number']))


def main():
    print('Список комманд:')
    print('p – people – команда, которая спросит номер документа и выведет имя человека, которому он принадлежит.')
    print(
        'l– list – команда, которая выведет список всех документов в формате passport "2207 876234" "Василий Гупкин".')
    print('s – shelf – команда, которая спросит номер документа и выведет номер полки, на которой он находится.')
    print(
        'a – add – команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип, имя владельца и номер полки, на котором он будет храниться.')
    print('d – delete – команда, которая спросит номер документа и удалит его из каталога и из перечня полок.')
    print(
        'm – move – команда, которая спросит номер документа и целевую полку и переместит его с текущей полки на целевую')
    print('as – add shelf – команда, которая спросит номер новой полки и добавит ее в перечень.')
    print('n - name -вывод имен всех владельцев документов и обработка исключения KeyError')
    print()
    command = input('Введите команду: ')
    print()
    if command == 'p':
        find_people(documents)
    elif command == 'l':
        info_list(documents)
    elif command == 's':
        find_shelf(directories)
    elif command == 'a':
        add(documents, directories)
    elif command == 'd':
        delete(documents, directories)
    elif command == 'm':
        move(directories)
    elif command == 'as':
        add_shelf(directories)
    elif command == 'n':
        name(documents)
    else:
        print('Неверная команда.\nПока !')
        return


if __name__ == '__main__':
    main()
