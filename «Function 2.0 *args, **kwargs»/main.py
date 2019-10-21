class PhoneBook:
    contact_list = []

    def __init__(self, name):
        self.name = name

    def all_contacts(self):
        if len(self.contact_list) > 0:
            for contact in self.contact_list:
                print(contact)
        else:
            print ('Телефонная книга пуста')

    def add_contact(self, contact):
        self.contact_list.append(contact)

    def del_by_number(self, tel_number):
        for contact in self.contact_list:
            if contact.tel_number == tel_number:
                self.contact_list.remove(contact)
            else:
                return None

    def all_chosen(self):
        for contact in self.contact_list:
            if contact.chosen_contact:
                print(contact)

    def search_by_name(self, first_name, last_name):
        for contact in self.contact_list:
            if first_name == contact.first_name and last_name == contact.last_name:
                print(contact)


class Contact:

    def __init__(self, first_name, last_name, tel_number, chosen_contact=False, *args, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.tel_number = tel_number
        self.chosen_contact = chosen_contact
        self.additional_info = {}
        # for item in args:
        self.additional_info.setdefault('Дополнительные номера', args)
        for key, value in kwargs.items():
            self.additional_info.update({key: value})

    def __str__(self):
        numbers = ' '
        all_string = 'Имя: {}\nФамилия: {}\nТелефон: {}\n'.format(self.first_name, self.last_name, self.tel_number)
        if not self.chosen_contact:
            all_string += 'В избранных: нет\nДополнительная информация:\n'
        else:
            all_string += 'В избранных: да\nДополнительная информация:\n'
        if self.additional_info:
            for key, value in self.additional_info.items():
                if key == 'Дополнительные номера' and value[0] != '':
                    for item in value:
                        numbers += item + '; '
                    all_string += '\t{}: {}\n'.format(key, numbers)
                elif value[0] == '':
                    continue
                else:
                    all_string += '\t{}: {}\n'.format(key, value)
        return all_string


def list_to_dict(any_list):
    new = {}
    if any_list[0] != '':
        for item in any_list:
            i = item.split('=')
            new[i[0]] = i[1]
    return new


if __name__ == '__main__':
    # chosen_con = False
    book_name = input('Как назовем записеую книжку?: ')
    new_phone_book = PhoneBook(book_name)
    print(f'Для работы с |{book_name}| используйте следующие команды: \n'
          f'Add - добавить контакт\nPrint - вывести все контакты')
    print('Del - удалить по номеру телефона\nVIP - вывести все избранные контакты\n'
          'Search - поиск по имени и фамилии\nExit - для выхода')
    while True:
        command = input('\nВведите вашу команду: ')
        print()
        if command == 'Add':
            f_name = input('Введите имя: ')
            if not f_name:
                print('Данное поле обязательно')
            l_name = input('Введите фамилию: ')
            if not l_name:
                print('Данное поле обязательно')
            t_number = input('Введите номер телефона: ')
            if not t_number:
                print('Данное поле обязательно')
            chosen = input('Добавить контакт в избраннное? (да/нет): ').lower()
            if chosen == 'да':
                chosen_con = True
            else:
                chosen_con = False
            additional_number = input('Дополнительные номера контакта через запятую (необязательное поле): ')\
                .replace(' ', '').split(',')
            additional_info_list = input('Дополнительная информация через запятую (пример email=a@a.ru): ')\
                .replace(' ', '').split(',')
            additional_info = list_to_dict(additional_info_list)
            new_contact = Contact(f_name, l_name, t_number, chosen_con, *additional_number, **additional_info)
            new_phone_book.add_contact(new_contact)

        elif command == 'Print':
            new_phone_book.all_contacts()

        elif command == 'Del':
            contact_for_del = input('Введите номер телефона контакта для удаления: ')
            new_phone_book.del_by_number(contact_for_del)
            print(f'Контакт с номером теелфона {contact_for_del} удален')

        elif command == 'VIP':
            new_phone_book.all_chosen()

        elif command == 'Search':
            f_name = input('Введите имя: ')
            l_name = input('Введите фамилию: ')
            print()
            new_phone_book.search_by_name(f_name, l_name)

        elif command == 'Exit':
            break

        else:
            print('Неверная команда')
