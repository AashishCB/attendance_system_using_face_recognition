from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
import cv2
from openpyxl import load_workbook
from datetime import date
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
        workbook = load_workbook(filename='attendance/attendance_register.xlsx')
        sheet = workbook.active
        return render_template('index.html', students=students, sheet=sheet)

@app.route('/collect_samples', methods = ['GET', 'POST'])
def collect_samples():
        if request.method == 'POST':
                username = request.form['Name']
                with open('attendance/students.txt', 'a') as j:
                        j.write(username+'\n')
        cmd = 'python attendance/image_collector.py ' + username
        os.system(cmd)
        workbook = load_workbook(filename='attendance/attendance_register.xlsx')
        sheet = workbook.active
        rc = 'A'+str(sheet.max_row+1)
        sheet[rc] = username
        workbook.save('attendance/attendance_register.xlsx')
        flash('samples collected')
        return redirect(url_for('index'))

@app.route('/recognize_face')
def recognize():
        cmd = 'python attendance/recognize_face.py'
        flash('recognized')
        os.system(cmd)
        student = None
        try:
                with open('attendance/username.txt', 'r') as f:
                        student = f.read()
        except:
                pass
        add_column()
        mark_present(student)
        return redirect(url_for('index'))

def add_column():
        workbook = load_workbook(filename='attendance/attendance_register.xlsx')
        sheet = workbook.active
        rc = str(sheet.cell(row=1,column=sheet.max_column))[-3:-1]
        print(rc,' rc',  sheet[rc].value, ' sheet[rc]', int(str(date.today()).split('-')[-1]), ' date.today')
        if sheet[rc].value == int(str(date.today()).split('-')[-1]):
                print(True)
                pass
        else:
                rc = str(sheet.cell(row=1,column=sheet.max_column+1))[-3:-1]
                sheet[rc] = int(str(date.today()).split('-')[-1])
        workbook.save('attendance/attendance_register.xlsx')
        print('later ', rc,' rc',  sheet[rc], ' sheet[rc]')

def mark_present(student):
        workbook = load_workbook(filename='attendance/attendance_register.xlsx')
        sheet = workbook.active
        column_no = str(sheet.cell(row=1,column=sheet.max_column))[-3:-2]
        for cell_no in sheet.iter_cols(min_row=2,max_row=sheet.max_row,min_col=1,max_col=1):
                names_row_cell_tuple=cell_no
        for row_cell_no in names_row_cell_tuple:
                if row_cell_no.value == student:
                        row_no = str(row_cell_no)[-2:-1]
        rc = column_no + row_no
        if sheet[rc].value != 'present':
                sheet[rc] = 'present'
        workbook.save('attendance/attendance_register.xlsx')