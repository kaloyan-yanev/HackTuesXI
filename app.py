from flask import Flask, render_template, request, url_for, redirect,session
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import mysql.connector  
from string_manipulation import remove_obstacles
#from flask_session import Session

app = Flask(__name__)  
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'gogo112008',
    database = 'login_info'
)
mycursor = db.cursor(buffered = True)

app.config['SECRET_KEY'] = 'secret_key'

class Clock(FlaskForm):
    minutes = IntegerField('minuts', validators=[DataRequired(), NumberRange(min = 0,max = 600)])
    Submit = SubmitField('Submit')

class Clock2(FlaskForm):
    minutes = IntegerField('minuts', validators=[DataRequired(), NumberRange(min = 0,max = 600)])
@app.route('/default')
def default():
    session["minutes_to_shift"] = 20
    session["minutes_to_move_around"] = 30
    return redirect(url_for("Index"))

@app.route('/', methods = ['GET', 'POST'])
def Index():
    Timer_info2 = Clock2() 
    Timer_info = Clock()
    if Timer_info.validate_on_submit():
        session["minutes_to_shift"] = Timer_info.minutes.data
        session["minutes_to_move_around"] = Timer_info2.minutes.data
        print(session["minutes_to_shift"])
        print(session["minutes_to_move_around"])
        return render_template('/Home.html', form = Timer_info, secondform = Timer_info2)
    else:
        print("TOO BAD")
    return render_template('/Index.html', form = Timer_info, secondform = Timer_info2)

@app.route('/Table')
def Table():
    return render_template('/Table.html')

@app.route('/Home')
def Home():
    print(session["minutes_to_shift"])
    print(session["minutes_to_move_around"])
    return render_template('/Home.html', minutes_to_shift_posture = session["minutes_to_shift"], minutes_to_move_around = session["minutes_to_move_around"])