from application.db.people import employers as employers


class Employer:
    position = ''
    name = ''

    def __init__(self, name):
        for workers in employers:
            if name in workers['name']:
                self.position = workers['position']
                self.name = name
                self.salary = workers['salary']

    def give_salary(self):
        print('Зарплата начислена сотруднику {} в размере {} руб.'.format(self.name, self.salary))

