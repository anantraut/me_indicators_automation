#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 19:56:07 2020

@author: anant
"""

from me_indicators_automation import app
from flask import Flask, render_template, request, make_response
from me_indicators_automation import pss, pdf, house, family, individual

UPLOAD_FOLDER = './uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET','POST'])
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/pss', methods=['GET','POST'])
def pss_data():
    if request.method == "POST":
        f = request.files['pss_file']
        data = pss.pss_metrics(f, request.form['from'], request.form['to'])
        resp = make_response(data.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=pss_metrics.csv"
        resp.headers["Content-Type"] = "text/csv"
    return resp

@app.route('/pdf', methods=['GET','POST'])
def pdf_data():
    if request.method == "POST":
        f = request.files['pdf_file']
        data = pdf.pdf_metrics(f, request.form['from'], request.form['to'])
        resp = make_response(data.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=pdf_metrics.csv"
        resp.headers["Content-Type"] = "text/csv"
    return resp

@app.route('/house', methods=['GET','POST'])
def house_data():
    if request.method == "POST":
        f = request.files['house_file']
        data = house.house_metrics(f)
        resp = make_response(data.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=house_metrics.csv"
        resp.headers["Content-Type"] = "text/csv"
    return resp

@app.route('/family', methods=['GET','POST'])
def family_data():
    if request.method == "POST":
        f = request.files['family_file']
        data = family.family_metrics(f)
        resp = make_response(data.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=family_metrics.csv"
        resp.headers["Content-Type"] = "text/csv"
    return resp

@app.route('/individual', methods=['GET','POST'])
def individual_data():
    if request.method == "POST":
        f = request.files['individual_file']
        data = individual.pdf_metrics(f)
        resp = make_response(data.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=individual_metrics.csv"
        resp.headers["Content-Type"] = "text/csv"
    return resp

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)
