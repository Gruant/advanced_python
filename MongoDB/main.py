import csv
import re
import pprint
from datetime import datetime
from pymongo import MongoClient


def connection(database):
    client = MongoClient()
    db = client[database]
    collection = db['concert']
    return collection


def read_data(csv_file, db):
    collection = connection(db)
    """
    Загрузить данные в бд из CSV-файла
    """
    with open(csv_file, encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {}
            for key, value in row.items():
                if key == 'Дата':
                    day, month = value.split('.')
                    value = datetime(year=2019, month=int(month), day=int(day))
                data.update({key: value})
            collection.insert_one(data)


def find_cheapest(db):
    collection = connection(db)
    for item in collection.find().sort('Цена'):
        print(item)


def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке, например "Seconds to"),
    и вернуть их по возрастанию цены
    """

    collection = connection(db)
    name = re.escape(name)
    regex = re.compile('{}'.format(name))
    match = collection.find({'Исполнитель': regex})
    if not match.count():
        print('Нет такого исполнителя')
    for item in match:
        print(item)


def date_sort(dates, db):
    collection = connection(db)
    for index, item in enumerate(dates):
        day, month, year = item.split('.')
        dates[index] = datetime(year=int(year), month=int(month), day=int(day))
    if len(dates) == 1:
        for item in collection.find({"Дата": {"$gte": dates[0]}}).sort("Дата"):
            print(item)
    if len(dates) == 2:
        for item in collection.find({"Дата": {"$gte": dates[0], "$lte": dates[1]}}).sort("Дата"):
            print(item)


if __name__ == '__main__':
    # read_data('artists.csv', 'concert_db5')
    # find_cheapest('concert_db5')
    # find_by_name('Ариkя', 'concert_db5')
    date_sort(['1.07.2019', '30.07.2019'], 'concert_db5')
