#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 19:56:07 2020

@author: anant
"""

from me_indicators_automation import app
from flask import Flask, render_template, request, make_response
import pandas
import os
from me_indicators_automation import pss

UPLOAD_FOLDER = './uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET','POST'])
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/pss', methods=['GET','POST'])
def data():
    if request.method == "POST":
        f = request.files['csvfile']
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'csvfile.csv'))
        data = pss.pss_metrics(f)
        resp = make_response(data.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
    return resp

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)
