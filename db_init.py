import data

from db_tables import *

for teacher in data.teachers:

    record_teacher = Teacher(
        name=teacher['name'],
        about=teacher['about'],
        rating=teacher['rating'],
        picture=teacher['picture'],
        price=teacher['price']
    )
    db.session.add(record_teacher)

    for goal in teacher['goals']:

        record_goal = Goal(goal=goal, view=data.goals[goal])
        db.session.add(record_goal)
        record_goal.teachers.append(record_teacher)

    for day, times in teacher['free'].items():

        record_day = Day(day=day, view=data.weekdays[day])
        db.session.add(record_day)
        record_day.teachers.append(record_teacher)

        for time, is_free in times.items():

            record_time = Time(time=time, is_free=is_free, day=record_day)
            db.session.add(record_time)

db.session.commit()
