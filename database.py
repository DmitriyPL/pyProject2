import pprint
import json
from dataclasses import dataclass


@dataclass
class Teacher:
    id: int
    name: str
    about: str
    rating: float
    picture: str
    price: float
    goals: list
    free: dict

    def __lt__(self, other):
        return self.rating > other.rating


def create(data, file):
    data_for_write = {'goals': data.goals, 'weekdays': data.weekdays, 'teachers': data.teachers}

    with open(file, "w") as databaseJSON:
        json.dump(data_for_write, databaseJSON)


def get_teachers(file):
    with open(file) as databaseJSON:
        data = json.load(databaseJSON)

    teachers = {}

    for teacher in data['teachers']:

        teachers[teacher['id']] = Teacher(teacher['id'], teacher['name'], teacher['about'],
                                          teacher['rating'], teacher['picture'], teacher['price'],
                                          teacher['goals'], teacher['free'])

    return teachers


def get_teacher(file, teacher_id):
    teachers = get_teachers(file)

    return teachers.get(teacher_id)


def get_goals(file):
    with open(file) as databaseJSON:
        data = json.load(databaseJSON)

    return data['goals']


def get_weekdays(file):
    with open(file) as databaseJSON:
        data = json.load(databaseJSON)

    return data['weekdays']

# Проверка записи!
#
# with open(file, "r") as databaseJSON:
#     contents = json.load(databaseJSON)
#
# pprint.pprint(contents)