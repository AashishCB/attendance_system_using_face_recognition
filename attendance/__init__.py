from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
import cv2

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/')
def index():
        student = None
        try:
                with open('attendance/username.txt', 'r') as f:
                        student = f.read()
        except:
                pass
        with open('attendance/students.txt', 'r') as k:
                students = k.read().split()
        return render_template('index.html', students=students)

@app.route('/collect_samples', methods = ['GET', 'POST'])
def collect_samples():
        if request.method == 'POST':
                username = request.form['Name']
                with open('attendance/students.txt', 'a') as j:
                        j.write(username+'\n')
        cmd = 'python attendance/image_collector.py ' + username
        os.system(cmd)
        flash('samples collected')
        return redirect(url_for('index'))

@app.route('/recognize_face')
def recognize():
        cmd = 'python attendance/recognize_face.py'
        flash('recognized')
        os.system(cmd)
        return redirect(url_for('index'))