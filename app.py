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
    password = 'WhatTheFUCKIsMySQL420',
    database = 'login_info'
)
mycursor = db.cursor(buffered = True)

app.config['SECRET_KEY'] = 'secret_key'

class Clock(FlaskForm):
    Hours = IntegerField('Hours', validators=[DataRequired(), NumberRange(min = 0,max = 24)])
    minutes = IntegerField('minuts', validators=[DataRequired(), NumberRange(min = 0,max = 60)])
    Submit = SubmitField('Submit')
@app.route('/', methods=['GET','POST'])
def Index():
    Timer_info = Clock()
    if Timer_info.validate_on_submit():
        session["Hours"] = Timer_info.Hours.data
        session["minutes"] = Timer_info.minutes.data
        print(session["Hours"])
        print(session["minutes"])
        return render_template('/Index.html', form = Timer_info)
    return render_template('/Index.html', form = Timer_info)
@app.route('/Table')
def Table():
    return render_template('/Table.html')
@app.route('/Home')
def Home():
    return render_template('/Home.html')