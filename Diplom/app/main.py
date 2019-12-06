# -*- coding: utf-8 -*-
from app.user import User, take_config
from app.sort_couple import Criteria
from app.create_data import DataMaker
from app.database import Database
from pprint import pprint
import vk_api
import psycopg2 as pg
from sys import exit


def main():
    try:
        try:
            user_id = take_config('../config.json')['id'] if take_config('config.json')['id'] else input('Input id: ')
            user = User(user_id)
            user.create_session()
            user.get_main_user_data()
        except ValueError:
            print('Не верно возраст')
            exit()
        try:
            db = Database()
            if not db.check_tables():
                db.create_db()
            users_ids = db.take_user()
            if not users_ids:
                db.create_user(user.id)
            else:
                users_ids_in_table = []
                for row in users_ids:
                    users_ids_in_table += row
                if str(user.id) not in users_ids_in_table:
                    db.create_user(user.id)
            writen_users = db.get_couple()
        except pg.Error as e:
            print(f'Проблема с базой данных: {e}.\nПроверьте конфигурацию в config.json')
            exit()

        print('==== Получили достаточную информацию о пользователе')

        user.take_groups()
        print('==== Получили группы пользователя')

        couple_list = user.search_all()
        writen_users_in_table = []
        new_couple_list = []
        if writen_users:
            for row in writen_users:
                writen_users_in_table += row
            for item in couple_list:
                if str(item['id']) not in writen_users_in_table:
                    new_couple_list.append(item)
            print('==== Получили список возможных пар\nОбрабатываем...')
            list_for_criteria = Criteria(user, new_couple_list)
        else:
            print('==== Получили список возможных пар\nОбрабатываем...')
            list_for_criteria = Criteria(user, couple_list)

        list_for_criteria.users_with_common_groups()
        print('==== Добавили вес пользователям с общими группами')

        list_for_criteria.user_weight_all()
        print('==== Добавили вес пользователям с общими интересами и возрастом')

        list_for_criteria.create_list_with_weight()
        list_for_criteria.sort_list()
        sorted_list = list_for_criteria.user_list
        print('==== Отсортировали по весу')

        list_to_json = DataMaker(user, sorted_list)
        print('==== Собираем фото и формируем json')

        json_f = list_to_json.take_ten_json()
        print('=== Полученная информация')
        pprint(json_f)
        try:
            db.insert_json(json_f, user.id)
            print('Информация добавлена в базу данных')
        except pg.Error as e:
            print('Не удалось записать информацию')

    except KeyboardInterrupt:
        print('Выполнение программы прервано')

if __name__ == '__main__':
    pass













