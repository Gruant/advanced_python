from pprint import pprint
import re
import csv


def take_info():
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contact_list = list(rows)
    return contact_list


def write_info(final_list):
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(final_list)


def new_list(contacts_list):
    new_contacts_list = []
    for index, contact in enumerate(contacts_list):
        if index == 0:
            new_contacts_list.append(contact)
        else:
            work_string = ' '.join(contact)

            match_fio = re.findall(r'(?:\b\w+\b)', work_string)
            new_contacts_list.append([match_fio[i] for i in range(3)])

            new_contacts_list[index].append(contact[3])

            new_contacts_list[index].append(contact[4])

            match_tel = re.findall(r'(\+7|8)\s*?\(?(\d{3})\s*?\)?\s*?\-?(\d{3})\s*?\-?(\d{2})\s*?\-?(\d{2})'
                                   r'|(\d{4})', work_string)
            if contact[5]:
                if len(match_tel) > 1:
                    new_contacts_list[index].append(f'{match_tel[0][0]}({match_tel[0][1]}){match_tel[0][2]}-'
                                                    f'{match_tel[0][3]}-{match_tel[0][4]} доб. {match_tel[1][-1]}')
                else:
                    new_contacts_list[index].append(f'{match_tel[0][0]}({match_tel[0][1]}){match_tel[0][2]}-'
                                                    f'{match_tel[0][3]}-{match_tel[0][4]}')
            else:
                new_contacts_list[index].append(contact[5])

            new_contacts_list[index].append(contact[6])

    return new_contacts_list


def del_dublicate(list_format):
    new_list = []
    for item_first in list_format:
        for item_second in list_format:
            if item_first[0] == item_second[0]:
                for i in range(len(item_first)):
                    if not item_first[i]:
                        item_first[i] = item_second[i]
                    else:
                        item_second[i] = item_first[i]
            if item_first not in new_list:
                new_list.append(item_first)
    return new_list


def main():
    contacts_list = take_info()
    format_list = new_list(contacts_list)
    write_info(del_dublicate(format_list))


if __name__ == '__main__':
    main()

