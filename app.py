import json
import random

from flask import Flask, render_template, request, abort
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, RadioField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, Length

import data
import database

FILE_FOR_DATA = "database.json"
FILE_FOR_BOOKING = "booking.json"
FILE_FOR_REQUEST = "request.json"

database.create(data, FILE_FOR_DATA)

app = Flask(__name__)
app.secret_key = "randomstring"


class BookingForm(FlaskForm):
    clientWeekday = HiddenField()
    clientTime = HiddenField()
    clientTeacher = HiddenField()
    clientName = StringField('Вас зовут', [InputRequired()])
    clientPhone = StringField('Ваш телефон', [InputRequired()])


class RequestForm(FlaskForm):
    goal = RadioField('Какая цель занятий?', choices=[("travel", "Для путешествий"),
                                                      ("study", "Для школы"),
                                                      ("work", "Для работы"),
                                                      ("relocate", "Для переезда")
                                                      ]
                      )
    time = RadioField('Сколько времени есть?', choices=[("1-2 часа в неделю", "1-2 часа в неделю"),
                                                        ("3-5 часов в неделю", "3-5 часов в неделю"),
                                                        ("5-7 часов в неделю", "5-7 часов в неделю"),
                                                        ("7-10 часов в неделю", "7-10 часов в неделю")
                                                        ]
                      )
    name = StringField('Вас зовут', [InputRequired()])
    phone = StringField('Ваш телефон', [InputRequired()])


@app.route('/')
def index():
    teachers = database.get_teachers(FILE_FOR_DATA)
    random_teachers = list(teachers.values())

    random.seed()
    random.shuffle(random_teachers)

    return render_template("index.html", teachers=random_teachers)


@app.route('/goals/<goal>/')
def goals(goal):
    list_goals = database.get_goals(FILE_FOR_DATA)
    teacher_for_goal = []

    for key, teacher in database.get_teachers(FILE_FOR_DATA).items():
        if goal in teacher.goals:
            teacher.id = int(key)
            teacher_for_goal.append(teacher)

    teacher_for_goal.sort()

    return render_template("goal.html", teacher_for_goal=teacher_for_goal, goal=goal, list_goals=list_goals)


@app.route('/profiles/<int:teacher_id>/')
def profiles(teacher_id):
    teacher = database.get_teacher(FILE_FOR_DATA, teacher_id)

    list_goals = database.get_goals(FILE_FOR_DATA)
    teacher_goals = [list_goals[g] for g in teacher.goals]
    weekdays = database.get_weekdays(FILE_FOR_DATA)

    if teacher is None:
        abort(404)

    return render_template("profile.html", teacher_id=teacher_id, teacher=teacher,
                           teacher_goals=teacher_goals, weekdays=weekdays
                           )


@app.route('/request/')
def request():
    form = RequestForm()

    return render_template("request.html", form=form)


@app.route('/request_done/', methods=['POST'])
def request_done():
    list_goals = database.get_goals(FILE_FOR_DATA)

    form = RequestForm()

    request_data = {'goal': form.goal.data,
                    'time': form.time.data,
                    'name': form.name.data,
                    'phone': form.phone.data,
                    }

    try:
        with open(FILE_FOR_REQUEST, "a") as requestJSON:
            json.dump(request_data, requestJSON)

        print(f"Данные успешно записаны в файл {FILE_FOR_REQUEST}")

    except OSError:

        print("Не удалось записать запрос!")

    goal = list_goals.get(request_data['goal'])

    return render_template("request_done.html", request_data=request_data, goal=goal)


@app.route('/booking/<int:teacher_id>/<day>/<time>/')
def booking(teacher_id, day, time):
    teacher = database.get_teacher(FILE_FOR_DATA, teacher_id)
    weekdays = database.get_weekdays(FILE_FOR_DATA)

    form = BookingForm(clientWeekday=day, clientTime=time, clientTeacher=teacher_id)

    return render_template("booking.html", form=form, teacher_id=teacher_id,
                           teacher=teacher, day=day, time=time, weekdays=weekdays)


@app.route('/booking_done/', methods=['POST'])
def booking_done():
    weekdays = database.get_weekdays(FILE_FOR_DATA)

    form = BookingForm()

    client_data = {'day': form.clientWeekday.data,
                   'time': form.clientTime.data,
                   'teacher': form.clientTeacher.data,
                   'name': form.clientName.data,
                   'phone': form.clientPhone.data,
                   }

    try:
        with open(FILE_FOR_BOOKING, "a") as bookingJSON:
            json.dump(client_data, bookingJSON)

        print(f"Данные успешно записаны в файл {FILE_FOR_BOOKING}")

    except OSError:

        print("Не удалось записать данные клиента!")

    return render_template("booking_done.html", client_data=client_data, weekdays=weekdays)


if __name__ == '__main__':
    app.run()
