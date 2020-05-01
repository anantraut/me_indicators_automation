#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:22:07 2020

@author: anant
"""

import pandas as pd
from me_indicators_automation.form import Form
import datetime as dt

def clean(form):
    col_mapping = {"woman_ID":"person_id", "woman_at_home":"person_at_home"}
    form.rename_columns(col_mapping)
    form.strip_id()
    form.filter_at_home()
    form.remove_duplicates()

## Pregnancy Screening
def pss_metrics(file, dt1, dt2):
    #file = './Data/pregnancy_screening.csv'
    #dt1 = '2020-01-01'
    #dt2 = '2020-03-31'
    cols = ['chw_name','woman_at_home','woman_ID','last_visit','last_visit_nepali',
            'agrees_for_service','urine_test','urine_test_positive',
            'pregnancy_status','balanced_counseling.bcs_form.method_change',
            'menopause','want_more_children', 'birth_gap', 'contraceptive_current',
            'balanced_counseling.bcs_form.counseling.method_chosen1']
    pss = Form(file, cols)
    clean(pss)

    #filter for data with last_visit date in the given date range, all indicators after this are based on this filtered data
    pss.filter_by_date('last_visit', [dt1,dt2])

    pss.count_by_chw('elig_wm','person_id')
    pss.count_by_chw('rcvd_pss','person_id',['agrees_for_service',['yes']])
    pss.count_by_chw('upt_done','person_id',['urine_test',['positive','negative','indetermined','test_malfunctioning']])
    pss.count_by_chw('upt_pos','person_id',['urine_test',['positive']])
    pss.count_by_chw('new_preg','person_id',['pregnancy_status',['pregnant']])
    pss.count_by_chw('bcs_agree','person_id',['balanced_counseling.bcs_form.method_change',['yes']])
    pss.count_by_chw('menop','person_id',['menopause',['yes']])
    pss.count_by_chw('more_child','person_id',['want_more_children',['yes']])
    pss.count_by_chw('birth_gap','person_id',['birth_gap',['two_or_more_years']])
    pss.count_by_chw('hystectomy','person_id',['contraceptive_current',['hystectomy']])
    pss.count_by_chw('sterilization','person_id',['contraceptive_current',['male_sterilization','female_sterilization']])
    pss.count_by_chw('pills','person_id',['contraceptive_current',['pills']])
    pss.count_by_chw('dipo','person_id',['contraceptive_current',['Dipo']])
    pss.count_by_chw('iud','person_id',['contraceptive_current',['iud']])
    pss.count_by_chw('implants','person_id',['contraceptive_current',['implants']])
    pss.count_by_chw('refer','person_id',['contraceptive_current',['implants']])
    #pss.results.to_csv('./uploads/'+dt.datetime.today().strftime('%m-%d-%Y %H%M%S')+'.csv', index=True)
    return pss.results
