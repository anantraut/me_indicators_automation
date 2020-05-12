#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 16:01:07 2019

@author: anant
"""

#import modules
from me_indicators_automation.case_form import CaseForm

## Individual data
def individual_metrics(file, content_type):

    #file = './Data/4. Individual-Enrollment_Bhadra 2076.xlsx'
    cols = ['chw_name','name_text','individualID','last_modified_date','closed','eligible_woman',
            'anc','pdf_direct','pnc1','pnc2','child_under_2','post_delivery','imam_patient',
            'cd_patient','surgery_patient','hypertension_screening','hypertension_screening_second_visit']
    individual = CaseForm(filepath=file, cols=cols, filetype = content_type)
    
    individual.strip_str('individualID')
    
    individual.filter_for_condition('closed', False) #Drop closed cases
    individual.remove_duplicates(sort_by=['individualID', 'name_text', 'last_modified_date'],dupl_subset=['individualID', 'name_text'])
    
    individual.convert_to_Int64(['anc','pdf_direct','pnc1','pnc2','child_under_2'])
    
    # Calculate number of individuals receiving service, and convert to Int64
    individual.df['receiving_service'] = individual.df[['eligible_woman',
                   'anc','pdf_direct','pnc1','pnc2','child_under_2','post_delivery','imam_patient','cd_patient','surgery_patient','hypertension_screening','hypertension_screening_second_visit']].sum(axis=1)>0
    individual.convert_to_Int64(['receiving_service'])
    
    individual.count_by_chw('ind_regd','individualID')
    individual.sum_by_chw('elig_women','eligible_woman')
    individual.sum_by_chw('anc','anc')
    individual.sum_by_chw('pdf_direct','pdf_direct')
    individual.sum_by_chw('pnc1','pnc1')
    individual.sum_by_chw('pnc2','pnc2')
    individual.sum_by_chw('u2_child','child_under_2')
    individual.sum_by_chw('post_deliv','post_delivery')
    individual.sum_by_chw('imam','imam_patient')
    individual.sum_by_chw('cd','cd_patient')
    individual.sum_by_chw('surgery','surgery_patient')
    individual.sum_by_chw('htn_scrn','hypertension_screening')
    individual.sum_by_chw('htn_2nd_scrn','hypertension_screening_second_visit')
    individual.sum_by_chw('recv_service','receiving_service')
    
    return individual.results