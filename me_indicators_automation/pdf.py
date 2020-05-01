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
    col_mapping = {"woman_ID":"person_id"}
    form.rename_columns(col_mapping)
    form.strip_id()

## Post Delivery Form
def pdf_metrics(file, dt1, dt2):
    #file = './Data/post_delivery_form.csv'
    #dt1 = '2020-01-01'
    #dt2 = '2020-03-31'
    cols = ['chw_name','woman_ID','last_visit','delivery_date_pdf','delivery_location',
            'child_one.birth_outcome1','child_two.birth_outcome2','child_three.birth_outcome3',
            'child_one.baby_weight1','child_two.baby_weight2','child_three.baby_weight3',
            'pregnancy_outcome']
    #woman_at_home does not exist

    pdf = Form(file, cols)
    clean(pdf)

    df2 = pdf.df #df2 is created only to calculate ppw_visited (post partum women visited based on last_visit in date range)
    df2 = df2.sort_values(['person_id','last_visit'],ascending = True).drop_duplicates('person_id', keep='last')
    pdf.count_by_chw_with_df(df2[(df2['last_visit']>=dt1) & (df2['last_visit']<=dt2)], 'ppw_visited','person_id')

    #filter for data with delivery date in the given date range, all indicators after this are based on this filtered data
    pdf.filter_by_date('delivery_date_pdf', [dt1,dt2])
    pdf.remove_duplicates()

    pdf.count_by_chw('num_of_deliv','person_id')
    pdf.count_by_chw('inst_deliv','person_id',['delivery_location',['private_clinic_hospital', 'primary_health_center',
           'nyaya_health_hospital', 'district_hospital', 'health_post',
           'non-nhn_health_facility', 'govt_facility_outside_nepal',
           'private_clinic-hospital_outside_nepal']])

    pdf.count_by_chw('live_births1','person_id',['child_one.birth_outcome1',['live_birth']])
    pdf.count_by_chw('live_births2','person_id',['child_two.birth_outcome2',['live_birth']])
    pdf.count_by_chw('live_births3','person_id',['child_three.birth_outcome3',['live_birth']])
    pdf.add_columns('live_births',['live_births1', 'live_births2', 'live_births3'])

    pdf.count_by_chw('still_births1','person_id',['child_one.birth_outcome1',['still_birth']])
    pdf.count_by_chw('still_births2','person_id',['child_two.birth_outcome2',['still_birth']])
    pdf.count_by_chw('still_births3','person_id',['child_three.birth_outcome3',['still_birth']])
    pdf.add_columns('still_births',['still_births1', 'still_births2', 'still_births3'])

    pdf.count_by_chw_num_condition('low_birth_wt1','person_id',['child_one.baby_weight1','<',2.5])
    pdf.count_by_chw_num_condition('low_birth_wt2','person_id',['child_two.baby_weight2','<',2.5])
    pdf.count_by_chw_num_condition('low_birth_wt3','person_id',['child_three.baby_weight3','<',2.5])
    pdf.add_columns('low_birth_wt',['low_birth_wt1', 'low_birth_wt2', 'low_birth_wt3'])

    pdf.count_by_chw_with_df(pdf.df[pdf.df['pregnancy_outcome']=='intended_abortion'], 'safe_abortions','person_id',['delivery_location',['primary_health_center',
           'nyaya_health_hospital', 'district_hospital']])

    return pdf.results
