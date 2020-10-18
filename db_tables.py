from app_setup import db


goals_relations_association = db.Table(
    'goals_relations',
    db.Column('teacher_id', db.Integer(), db.ForeignKey('teachers.id')),
    db.Column('goal_id', db.Integer(), db.ForeignKey('goals.id'))
)


days_relations_association = db.Table(
    'days_relations',
    db.Column('teacher_id', db.Integer(), db.ForeignKey('teachers.id')),
    db.Column('day_id', db.Integer(), db.ForeignKey('days.id'))
)


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,  nullable=False)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    bookings = db.relationship("Booking")

    goals = db.relationship("Goal", secondary=goals_relations_association, back_populates='teachers')

    days = db.relationship("Day", secondary=days_relations_association, back_populates='teachers')


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String,  nullable=False)
    time = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher = db.relationship("Teacher")


class Request(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)


class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    view = db.Column(db.String, nullable=False)

    teachers = db.relationship("Teacher", secondary=goals_relations_association, back_populates="goals")


class Day(db.Model):
    __tablename__ = "days"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    view = db.Column(db.String, nullable=False)

    times = db.relationship("Time")

    teachers = db.relationship("Teacher", secondary=days_relations_association, back_populates="days")


class Time(db.Model):
    __tablename__ = "times"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=False)
    is_free = db.Column(db.Boolean, nullable=False)

    day_id = db.Column(db.Integer, db.ForeignKey("days.id"))
    day = db.relationship("Day")
