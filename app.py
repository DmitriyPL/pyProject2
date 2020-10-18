import random

from flask import render_template, request
from sqlalchemy.sql import text

import db_set

from app_setup import app
from db_tables import *
from app_forms import BookingForm, RequestForm


@app.route('/')
def index():

    teachers = db.session.query(Teacher).all()
    random.shuffle(teachers)

    return render_template("index.html", teachers=teachers)


@app.route('/goals/<goal>/')
def goals(goal):

    t = text("""SELECT * FROM public.teachers
                    JOIN (
                        SELECT teacher_id FROM public.goals_relations
                            JOIN public.goals
                            ON goal_id = id
                                WHERE public.goals.goal = :param
                        ) AS Goal                        
                    ON id = Goal.teacher_id
                ORDER BY rating DESC """
             )

    teachers_for_goal = db.session.execute(t, {"param": goal}).fetchall()

    goal_view = db.session.query(Goal).filter(Goal.goal == goal).first().view

    return render_template("goal.html", teachers_for_goal=teachers_for_goal, goal=goal_view)


@app.route('/profiles/<int:teacher_id>/')
def profiles(teacher_id):

    teacher = db.session.query(Teacher).get_or_404(teacher_id)

    teacher_goals = [goal.view for goal in teacher.goals]

    return render_template("profile.html", teacher=teacher, teacher_goals=teacher_goals)


@app.route('/request/', methods=['GET', 'POST'])
def render_request():

    form = RequestForm()

    if request.method == 'GET':

        return render_template("request.html", form=form)

    elif request.method == 'POST':

        if form.validate_on_submit():

            goal = db.session.query(Goal).filter(Goal.goal == form.goal.data).first()

            request_data = {'goal': goal,
                            'time': form.time.data,
                            'name': form.name.data,
                            'phone': form.phone.data,
                            }

            db_set.request_record(db, request_data)
            db.session.commit()

            return render_template("request_done.html", request_data=request_data)

        else:

            return render_template("request.html", form=form)


@app.route('/booking/<int:teacher_id>/<int:day_id>/<int:time_id>/', methods=['GET', 'POST'])
def booking(teacher_id, day_id, time_id):

    teacher = db.session.query(Teacher).get(teacher_id)
    day = db.session.query(Day).get(day_id)
    time = db.session.query(Time).get(time_id)

    form = BookingForm(teacher_id=teacher_id, day_id=day_id, time_id=time_id)

    if request.method == 'GET':

        return render_template("booking.html", form=form, teacher=teacher, day=day.view, time=time.time)

    elif request.method == 'POST':

        if form.validate_on_submit():

            client_data = {'day': day,
                           'time': time,
                           'name': form.name.data,
                           'phone': form.phone.data,
                           }

            db_set.booking_record(db, teacher, client_data)
            db.session.commit()

            return render_template("booking_done.html", client_data=client_data)

        return render_template("booking.html", form=form, teacher=teacher, day=day.view, time=time.time)


if __name__ == '__main__':
    app.run()
