import pprint
import json
from dataclasses import dataclass

import data

FILE_FOR_DATA = "database.json"
FILE_FOR_BOOKING = "booking.json"
FILE_FOR_REQUEST = "request.json"


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


def change_teacher_time(teacher_id, day, time):
    with open(FILE_FOR_DATA) as databaseJSON:
        info = json.load(databaseJSON)

    for teacher in info['teachers']:
        if teacher['id'] == teacher_id:
            teacher['free'][day][time] = False

            with open(FILE_FOR_DATA, "w") as databaseJSON:
                json.dump(info, databaseJSON)


def create():
    data_for_write = {'goals': data.goals, 'weekdays': data.weekdays, 'teachers': data.teachers}

    with open(FILE_FOR_DATA, "w") as databaseJSON:
        json.dump(data_for_write, databaseJSON)


def get_teachers():
    with open(FILE_FOR_DATA) as databaseJSON:
        info = json.load(databaseJSON)

    teachers = {}

    for teacher in info['teachers']:

        teachers[teacher['id']] = Teacher(teacher['id'], teacher['name'], teacher['about'],
                                          teacher['rating'], teacher['picture'], teacher['price'],
                                          teacher['goals'], teacher['free'])

    return teachers


def get_teacher(teacher_id):
    teachers = get_teachers()

    return teachers.get(teacher_id)


def get_goals():
    with open(FILE_FOR_DATA) as databaseJSON:
        info = json.load(databaseJSON)

    return info['goals']


def get_weekdays():
    with open(FILE_FOR_DATA) as databaseJSON:
        info = json.load(databaseJSON)

    return info['weekdays']


create()


# Проверка записи!
#
# with open(file, "r") as databaseJSON:
#     contents = json.load(databaseJSON)
#
# pprint.pprint(contents)