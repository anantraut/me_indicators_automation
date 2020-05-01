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
from me_indicators_automation import pss, pdf

UPLOAD_FOLDER = './uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET','POST'])
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/pss', methods=['GET','POST'])
def pss_data():
    if request.method == "POST":
        f = request.files['pss_csv']
        data = pss.pss_metrics(f, request.form['from'], request.form['to'])
        resp = make_response(data.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
    return resp

@app.route('/pdf', methods=['GET','POST'])
def pdf_data():
    if request.method == "POST":
        f = request.files['pdf_csv']
        data = pdf.pdf_metrics(f, request.form['from'], request.form['to'])
        resp = make_response(data.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
    return resp

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)
