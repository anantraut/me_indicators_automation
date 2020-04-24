#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 19:56:07 2020

@author: anant
"""

from flask import Flask

app = Flask(__name__)

import me_indicators_automation.views

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)
