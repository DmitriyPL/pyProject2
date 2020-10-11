import json
import random

from flask import Flask, render_template, abort
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, RadioField
from wtforms.validators import InputRequired, Length, DataRequired

import database

app = Flask(__name__)
app.secret_key = "randomstring"


class BookingForm(FlaskForm):
    clientWeekday = HiddenField()
    clientTime = HiddenField()
    clientTeacher = HiddenField()
    clientName = StringField('Вас зовут', [InputRequired(message="Укажите Ваше имя!")],
                             render_kw={"placeholder": "Иван"})
    clientPhone = StringField('Ваш телефон', [InputRequired(message="Что то не так с телефоном!"),
                                              Length(min=6, max=12)], render_kw={"placeholder": "+79812756987"})


class RequestForm(FlaskForm):
    goal = RadioField('Какая цель занятий?', [DataRequired(message="Как без цели?")],
                      choices=[
                          ("travel", "Для путешествий"),
                          ("study", "Для школы"),
                          ("work", "Для работы"),
                          ("relocate", "Для переезда")
                      ]
                      )
    time = RadioField('Сколько времени есть?', [DataRequired(message="Укажите время!")],
                      choices=[
                          ("1-2 часа в неделю", "1-2 часа в неделю"),
                          ("3-5 часов в неделю", "3-5 часов в неделю"),
                          ("5-7 часов в неделю", "5-7 часов в неделю"),
                          ("7-10 часов в неделю", "7-10 часов в неделю")
                      ]
                      )
    name = StringField('Вас зовут', [InputRequired(message="Укажите Ваше имя!")], render_kw={"placeholder": "Иван"})
    phone = StringField('Ваш телефон', [InputRequired(message="Что то не так с телефоном!"), Length(min=6, max=12)],
                        render_kw={"placeholder": "+79812756987"})


@app.route('/')
def index():
    teachers = database.get_teachers()
    random_teachers = list(teachers.values())

    random.seed()
    random.shuffle(random_teachers)

    return render_template("index.html", teachers=random_teachers)


@app.route('/goals/<goal>/')
def goals(goal):
    list_goals = database.get_goals()
    teacher_for_goal = []

    for teacher in database.get_teachers().values():
        if goal in teacher.goals:
            teacher_for_goal.append(teacher)

    teacher_for_goal.sort()

    return render_template("goal.html", teacher_for_goal=teacher_for_goal, goal=list_goals[goal])


@app.route('/profiles/<int:teacher_id>/')
def profiles(teacher_id):
    teacher = database.get_teacher(teacher_id)
    weekdays = database.get_weekdays()
    goals = database.get_goals()

    teacher_goals = [goals[g] for g in teacher.goals]

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
    goals = database.get_goals()

    form = RequestForm()

    request_data = {'goal': form.goal.data,
                    'time': form.time.data,
                    'name': form.name.data,
                    'phone': form.phone.data,
                    }

    goal = goals.get(request_data['goal'])

    try:
        with open(database.FILE_FOR_REQUEST, "a") as requestJSON:
            json.dump(request_data, requestJSON)

        print(f"Данные успешно записаны в файл {database.FILE_FOR_REQUEST}")

    except OSError:

        print("Не удалось записать запрос!")

    return render_template("request_done.html", request_data=request_data, goal=goal)


@app.route('/booking/<int:teacher_id>/<day>/<time>/')
def booking(teacher_id, day, time):
    teacher = database.get_teacher(teacher_id)
    weekdays = database.get_weekdays()

    form = BookingForm(clientWeekday=day, clientTime=time, clientTeacher=teacher_id)

    return render_template("booking.html", form=form, teacher_id=teacher_id,
                           teacher=teacher, day=day, time=time, weekdays=weekdays)


@app.route('/booking_done/', methods=['POST'])
def booking_done():
    weekdays = database.get_weekdays()

    form = BookingForm()

    client_data = {'day': form.clientWeekday.data,
                   'time': form.clientTime.data,
                   'teacher': form.clientTeacher.data,
                   'name': form.clientName.data,
                   'phone': form.clientPhone.data,
                   }

    database.change_teacher_time(int(client_data['teacher']), client_data['day'], client_data['time'])

    try:
        with open(database.FILE_FOR_BOOKING, "a") as bookingJSON:
            json.dump(client_data, bookingJSON)

        print(f"Данные успешно записаны в файл {database.FILE_FOR_BOOKING}")

    except OSError:

        print("Не удалось записать данные клиента!")

    return render_template("booking_done.html", client_data=client_data, weekdays=weekdays)


if __name__ == '__main__':
    app.run()
