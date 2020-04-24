M&E Indicators Automation
======

This application takes a csv file of specific format, and generates metrics for download in another csv file.


Install
-------

    # clone the repository

Create a virtualenv and activate it::

    $ python3 -m venv venv
    $ . venv/bin/activate

Install me_indicators_automation::

    $ pip install -e .

Run
---

::

    $ export FLASK_APP=me_indicators_automation
    $ export FLASK_ENV=development
    $ flask run

Open http://127.0.0.1:5000 in a browser.
