from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import TimeField,FloatField, SubmitField
from wtforms.validators import DataRequired, Length
import mysql.connector  
from string_manipulation import remove_obstacles
from flask_session import Session

app = Flask(__name__)  
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'WhatTheFUCKIsMySQL420',
    database = 'login_info'
)
mycursor = db.cursor(buffered = True)

app.config['SECRET_KEY'] = 'secret_key'

class Clock(FlaskForm):
    Hours = FloatField('Hours', validators=[DataRequired(), Length(min = 0,max = 24)])
    minutes = FloatField('minuts', validators=[DataRequired(), Length(min = 0,max = 60)])
    Submit = SubmitField('Submit')
@app.route('/', methods=['GET','POST'])
def Index():
    Timer_info = Clock()
    if Timer_info.validate_on_submit():
        Session['hours'] = Timer_info.Hours.data
        Session['minutes'] = Timer_info.minutes.data
        print(request.form['hours'])
        print(request.form['minutes'])
        print(Timer_info.Hours.data)
        print(Timer_info.minutes.data)
        return render_template('/Index.html', form = Timer_info)
    return render_template('/Index.html', form = Timer_info)
@app.route('/Table')
def Table():
    return render_template('/Table.html')