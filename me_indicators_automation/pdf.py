#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:22:07 2020

@author: anant
"""

from me_indicators_automation.case_form import CaseForm

def clean(form):
    col_mapping = {"woman_ID":"person_id"}
    form.rename_columns(col_mapping)
    form.strip_str('person_id')

## Post Delivery Form
def pdf_metrics(file, dt1='2015-01-01', dt2='2050-01-01', content_type='text/csv'):
    #file = './Data/post_delivery_form.csv'
    #dt1 = '2020-01-01'
    #dt2 = '2020-03-31'
    cols = ['chw_name','woman_ID','last_visit','delivery_date_pdf','delivery_location',
            'child_one.birth_outcome1','child_two.birth_outcome2','child_three.birth_outcome3',
            'child_one.baby_weight1','child_two.baby_weight2','child_three.baby_weight3',
            'pregnancy_outcome']
    #woman_at_home does not exist

    pdf = CaseForm(filepath=file, cols=cols, filetype=content_type)
    clean(pdf)

    pdf_ppw_visited = CaseForm() #pdf_ppw_vis is created only to calculate ppw_visited (post partum women visited based on last_visit in date range)
    pdf_ppw_visited.df = pdf.df
    pdf_ppw_visited.filter_by_date('last_visit', [dt1,dt2])
    pdf_ppw_visited.remove_duplicates(sort_by=['person_id', 'last_visit'],dupl_subset=['person_id'])
    pdf_ppw_visited.count_by_chw('ppw_visited','person_id')

    #filter for data with delivery date in the given date range, all indicators after this are based on this filtered data
    pdf.filter_by_date('delivery_date_pdf', [dt1,dt2])
    pdf.remove_duplicates(sort_by=['person_id', 'last_visit'],dupl_subset=['person_id'])

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

    pdf.filter_for_condition('pregnancy_outcome','intended_abortion')
    
    pdf.count_by_chw('safe_abortions','person_id',['delivery_location',['primary_health_center',
           'nyaya_health_hospital', 'district_hospital']])

    return pdf.concat_dataframes([pdf.results, pdf_ppw_visited.results])