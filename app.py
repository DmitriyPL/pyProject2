from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, Length

app = Flask(__name__)
app.secret_key = "randomstring"


class MyForm(FlaskForm):

    name = StringField('name', [InputRequired()])
    mail = StringField('mail', [Email()])


@app.route('/')
def render_index():

    form = MyForm()
    return render_template("form.html", form=form)


@app.route('/send/', methods=["POST"])
def render_send():

    form = MyForm()
    if form.validate():
        return "It's OK"
    else:
        return "It's not OK"


@app.route('/form/', methods=["GET", "POST"])
def render_form():

    form = MyForm()

    if form.validate():
        return "It's OK"
    else:
        return "It's not OK"

    if request.method == "POST":

        name = form.name.data
        phone = form.phone.data

        return render_template("save.html", name=name, phone=phone)

    else:

        return render_template("form.html", form=form)


app.run(port=8060, debug=True)