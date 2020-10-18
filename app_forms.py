from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, RadioField, SubmitField
from wtforms.validators import InputRequired, Length, DataRequired


class BookingForm(FlaskForm):
    day_id = HiddenField()
    time_id = HiddenField()
    teacher_id = HiddenField()

    name = StringField('Вас зовут',
                       [InputRequired(), Length(message="Имя из одной буквы?? Хм...", min=2)],
                       render_kw={"placeholder": "Иван"}
                       )
    phone = StringField('Ваш телефон',
                        [InputRequired(), Length(message="Неверная длина номера телефона", min=6, max=12)],
                        render_kw={"placeholder": "+79812756987"}
                        )

    submit = SubmitField('Записаться на пробный урок')


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

    name = StringField('Вас зовут',
                       [InputRequired(), Length(message="Имя из одной буквы?? Хм...", min=2)],
                       render_kw={"placeholder": "Иван"}
                       )

    phone = StringField('Ваш телефон',
                        [InputRequired(), Length(message="Неверная длина номера телефона", min=6, max=12)],
                        render_kw={"placeholder": "+79812756987"}
                        )

    submit = SubmitField('Найдите мне преподавателя')
