#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 19:56:07 2020

@author: anant
"""

from flask import Flask, render_template, request, make_response
import pandas as pd
import os
import generate


UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET','POST'])
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/data', methods=['GET','POST'])
def data():
    if request.method == "POST":
        f = request.files['csvfile']
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'csvfile.csv'))
        #data = pd.read_csv(f)
        data = generate.hello(f)
    #return render_template('data.html', data=data)
        resp = make_response(data.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
    return resp

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)
