from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import TimeField,FloatField
from wtforms.validators import DataRequired, Length
import mysql.connector  
from string_manipulation import remove_obstacles
from flask_session import Session

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
    time = TimeField('Interval', validators=[DataRequired()])
@app.route('/')
def Index():
    Timer_info = Clock()
    return render_template('/Index.html')
@app.route('/Table')
def Table():
    return render_template('/Table.html')