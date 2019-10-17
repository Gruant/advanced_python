import json


class CountryIterator:

    def __init__(self, from_file, to_file):
        self.from_file = from_file
        self.to_file = to_file
        self.country_list = []
        self.new_line = ''
        self.count = 0
        with open(self.from_file, 'r') as json_file:
            data = json.load(json_file)
        for i in data:
            self.country_list.append(i['name']['common'])
        self.country = self.country_list.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        if self.count == len(self.country_list):
            raise StopIteration
        else:
            self.count += 1
            country = self.country.__next__()
            country_wiki = country.replace(' ', '_')
            country_link = f'https://en.wikipedia.org/wiki/{country_wiki}'
            self.new_line = f'{country} - {country_link}\n'
            return self.new_line

    def save(self):
        with open(self.to_file, mode='a', encoding='utf-8') as file:
            file.write(self.new_line)


if __name__ == '__main__':
    new = CountryIterator('countries.json', 'new.txt')
    for i in new:
        new.save()
    print('Страны и ссылки записаны в файл new.txt ')
