from application.db.people import employers
from application import salary
from pprint import pprint
from datetime import datetime


def time_now():
    time = datetime.strftime(datetime.now(), '%Y.%m.%d')
    return time


def main():
    while True:
        command = input('1 - Вывести базу работников\n2 - Начислить работнику зарплату\n')
        if command == '1':
            print(time_now())
            pprint(employers)
            print()
        elif command == '2':
            name = salary.Employer(input('Введите имя сотрудника: '))
            print()
            print(time_now())
            return name.give_salary()


if __name__ == '__main__':
    main()