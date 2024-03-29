# -*- coding: utf-8 -*-
import vk_api
from urllib.parse import urlencode
from datetime import date, datetime
import re
import json
from sys import exit
import os
import pathlib


class User:

    def __init__(self, user_id):
        self.id = user_id
        self.vk_api = None
        self.groups = None
        self.age = int()
        self.interest_list = None
        self.city = None
        self.sex = None
        self.token = None
        self.music = []
        self.interests = []
        self.books = []

    def get_main_user_data(self):
        try:
            data = self.vk_api.users.get(user_ids=self.id, fields='interests, music, books, sex, bdate, has_photo,'
                                                                  'city, groups')
            self.id = data[0].get('id')
        except vk_api.exceptions.ApiError as e:
            print('Что то пошло не так', e)
            exit()
        except IndexError:
            print('Неверно введен ID')
            exit()
        try:
            day, month, year = data[0].get('bdate').split('.')
            self.age = calculate_age(datetime(year=int(year), month=int(month), day=int(day)))
        except ValueError:
            self.age = int(input('Мы не знаем сколько вам лет для поиска пары. Введите ваш возраст: '))
        except TypeError:
            self.age = int(input('Мы не знаем сколько вам лет для поиска пары. Введите ваш возраст: '))
        except AttributeError:
            self.age = int(input('Мы не знаем сколько вам лет для поиска пары. Введите ваш возраст: '))

        self.sex = data[0]['sex']
        if self.sex == 0:
            self.sex = input('Введите ваш пол для корректного поиска(1-м, 2-ж): ')

        try:
            self.city = data[0].get('city')['id']
        except TypeError:
            look = str(input('В каком городе ищем пару?: '))
            self.take_city_id(look)

        interests = data[0].get('interests')
        if interests:
            self.interests = interests_search(interests)
        else:
            self.interests = input('У вас отсутвуют интересы, если хотите ввести, то введите через пробел: ') \
                .split(' ')

        books = data[0].get('books')
        if interests:
            self.books = interests_search(books)
        else:
            self.books = []

        music = data[0].get('music')
        if interests:
            self.music = interests_search(music)
        else:
            self.music = []

    def take_groups(self):
        self.groups = self.vk_api.groups.get(user_id=self.id).get('items')

    def take_city_id(self, city):
        params = {
            'country_id': 1,
            'q': city,
            'count': 1,
            'v': '5.103'
        }
        cities = self.vk_api.database.getCities(**params)
        try:
            self.city = cities['items'][0]['id']
        except IndexError:
            print('Город не найден')
            exit()

    def get_user_access(self):
        url = 'https://oauth.vk.com/authorize'
        params = {
            'client_id': '7148260',
            'response_type': 'token',
            'display': 'page',
            'scope': ['groups', 'friends', 'photos'],
            'v': '5.103',
        }
        print('?'.join((url, urlencode(params))))
        self.token = input('Введите токен из ссылки редиректа: ')
        write_token('config.json', self.token)

    def create_session(self):
        try:
            configuration = take_config('config.json')
            if configuration['access_token']:
                session = vk_api.VkApi(token=configuration['access_token'])
                check = session.get_api()
                check.users.get(user_ids='1')
                self.vk_api = check
            else:
                self.get_user_access()
                session = vk_api.VkApi(token=self.token)
                self.vk_api = session.get_api()
        except vk_api.exceptions.ApiError:
            self.get_user_access()
            session = vk_api.VkApi(token=self.token)
            check = session.get_api()
            self.vk_api = check

    def is_member(self, groups, users):

        try:
            common_groups = self.vk_api.groups.isMember(group_id=groups, user_ids=users)
            common_groups += common_groups
            return common_groups
        except vk_api.exceptions.ApiError:
            common_groups = []
            return common_groups

    def search_all(self, count=1000):
        """
        Благодаря циклу обходим запрет в 1000 пользователей
        Проверяем на дубли и закрыт ли профиль
        """
        search_all = []
        search_all_dirt = []
        search_without_dubl = []
        if self.sex == 1:
            sex = 2
            age_from = self.age
            age_to = self.age + 10
        else:
            sex = 1
            age_from = self.age - 10
            age_to = self.age
        param = {
            'count': count,
            'sex': sex,
            'age_to': age_to,
            'has_photo': 1,
            'city': self.city,
            'fields': 'interests, music, movies, books, city, bdate, common_count'
        }
        for j in range(0, 1):
            search = self.vk_api.users.search(age_from=age_from + j, **param)['items']
            search_all_dirt += search
        for people in search_all_dirt:
            if people not in search_without_dubl:
                search_without_dubl.append(people)
        for people in search_without_dubl:
            if not people['is_closed']:
                people.update({'weight': 0})
                search_all.append(people)
        return search_all


def take_config(path_a):
    with open(path_a, 'r') as config:
        configuration = json.load(config)
        return configuration


def interests_search(interest):
    interest = re.sub(r'[?|$.!,:;]', r'', interest)
    match = re.findall(r'\w+', interest)
    return [item.lower() for item in match]


def write_token(path, token):
    config = take_config(path)
    config.update({'access_token': token})
    with open (path, 'w') as con:
        json.dump(config, con)


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


if __name__ == '__main__':
    pass
