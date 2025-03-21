from flask import Flask, render_template, request, url_for, redirect,session
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NumberRange
import mysql.connector  
from string_manipulation import remove_obstacles
import random
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
    minutes2 = IntegerField('minutes', validators=[DataRequired(), NumberRange(min = 0,max = 600)],)
class KilograMeter(FlaskForm):
    kilograms = IntegerField('KG', validators=[DataRequired(), NumberRange(min = 0,max = 200)])
class Calibrate(FlaskForm):
    bool = BooleanField('Calibrate', false_values=(False, 'false', 0, '0'))
@app.route('/default')
def default():
    session["minutes_to_shift"] = 20
    session["minutes_to_move_around"] = 30
    session["Kilograms"] = 50
    global i
    i = 0
    return redirect(url_for("Home"))

@app.route('/', methods = ['GET', 'POST'])
def Index():
    Timer_info = Clock()
    Timer_info2 = Clock2() 
    Kilogram = KilograMeter()
    calibrate = Calibrate()
    if Timer_info.validate_on_submit():
        session["minutes_to_shift"] = Timer_info.minutes.data
        session["minutes_to_move_around"] = Timer_info2.minutes2.data
        session["Kilograms"] = Kilogram.kilograms.data
        print(session["Kilograms"])
        print(session["minutes_to_shift"])
        print(session["minutes_to_move_around"])
        print(calibrate.bool)
        i = 1
        if(calibrate.bool.data == True):    
            print("YES")
           # values = [30.5,20.6]
           # mycursor.execute("CREATE TABLE IF NOT EXISTS default_data (back_sensor FLOAT, neck_sensor FLOAT)")
           # mycursor.execute("INSERT INTO default_data (back_sensor,neck_sensor) VALUES(%f,%f)", values)
        else:
            print("NO")
        return redirect(url_for("Home"))
    else:
        print("TOO BAD")
    return render_template('/Index.html', form = Timer_info, secondform = Timer_info2, Weight = Kilogram, calibrating = calibrate, session_minutes1 = session["minutes_to_shift"], session_minutes2 = session["minutes_to_move_around"], current_weight = session["Kilograms"])

@app.route('/Table')
def Table():
    return render_template('/Table.html')

@app.route('/Home')
def Home():
    random_value_for_now = random.randint(session["Kilograms"] - 10, 100)
    print(random_value_for_now)
    print(session["minutes_to_shift"])
    print(session["minutes_to_move_around"])
    return render_template('/Home.html', minutes_to_shift_posture = session["minutes_to_shift"], minutes_to_move_around = session["minutes_to_move_around"], minimum_weight = session["Kilograms"], current_weight = random_value_for_now)