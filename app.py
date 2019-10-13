from flask import Flask, jsonify, request, render_template, url_for, send_from_directory, abort
import requests, json, mysql.connector
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import json, requests
import os, random
import numpy as np



app = Flask(__name__)


mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '12345678',
    database = 'creditrisk'
)
x = mydb.cursor()
x.execute('select * from users')
datauser = x.fetchall()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    deptid = int(request.form['department'])
    password = int(request.form['password'])

    if password =='<Response [404]>':
        return render_template('index.html')
    else: 
        if deptid == 0 and password == int(datauser[deptid][2]):
            return render_template('form.html')
        elif deptid == 1 and password == int(datauser[deptid][2]):
            return render_template('form.html')
        else:
            # return render_template('2ndlogin.html')
            notice ="Wrong Password!"
            return render_template('index.html', notice=notice)


@app.route('/predict', methods = ['POST', 'GET'])
def predict():
    age = int(request.form['age'])
    sex = int(request.form['sex'])
    job = int(request.form['job'])
    housing = int(request.form['housing'])
    creditamount = int(request.form['creditamount'])
    duration = int(request.form['duration'])
    purpose = int(request.form['purpose'])
    checking = int(request.form['checking'])
    saving = int(request.form['saving'])


    pred2 = modelRF.predict(scaler.transform([[
        age, sex, job, housing, saving, checking, creditamount, duration, purpose
        ]]))[0]
        
    if pred2 == 0:
        pred2 = 'He/ She has BAD credit risk'
    elif pred2 == 1:
        pred2 = 'He/ She has Good credit risk, you can approve the application!'
    else:
        notice ="Wrong Input!"
        return render_template('index.html', notice=notice)
    


    dict = {
        'age': age,
        'sex': sex,
        'job': job,
        'housing': housing,
        'creditamount': creditamount,
        'duration': duration,
        'purpose': purpose,
        'checking': checking,
        'saving': saving,
        'pred': pred2,
       
    }
    return render_template('result.html', data=dict)

@app.route('/contact', methods = ['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        message = request.form['message']
        x = mydb.cursor()
        qry ='''insert into pesan(name,email,department,message) value (%s,%s,%s,%s )'''
        val = name, email, department, message
        x.execute(qry, val)
        mydb.commit()
        notice ="Message Sent!"
        return render_template('contact.html', notice=notice)
    else:
        return render_template('contact.html')

@app.route('/statistic', methods = ['POST', 'GET'])
def statistic():
    return render_template('statistic.html')


@app.route('/file/<path:x>')
def graph(x):
    return send_from_directory('file', x)

if __name__ == "__main__":
    scaler = joblib.load('scaler')
    modelRF = joblib.load('modelRF')
    app.run(debug = True,
        host = '0.0.0.0',
        port = 1911)