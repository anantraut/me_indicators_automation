#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 16:01:07 2019

@author: anant
"""

#import modules
from me_indicators_automation.case_form import CaseForm

## Family data
def family_metrics(file):
    #file = './Data/3. Family Enrollment Monthly report_Bhadra 2076.xlsx'
    cols = ['chw_name','familyID','family_head','last_modified_date','closed',
            'enrollment_complete','family_female_non_residents',
            'family_male_non_residents','family_female_residents','family_male_residents','residence_type']
    family = CaseForm(file, cols)
    
    family.strip_str('familyID')
    
    family.drop_closed_cases()
    family.remove_duplicates(sort_by=['familyID', 'family_head', 'last_modified_date'],dupl_subset=['familyID', 'family_head'])
    
    family.df['residence_type'] = family.df['residence_type'].map({1:1,2:2,
               3:3,'single':1,'primary':2,'secondary':3})
    
    family.convert_to_Int64(['residence_type','family_female_non_residents','family_male_non_residents','family_female_residents','family_male_residents'])
    
    family.count_by_chw('enroll_cmplt','familyID',['enrollment_complete',['yes']])
    family.count_by_chw('enroll_not_cmplt','familyID',['enrollment_complete',['no']])
    family.count_by_chw('Single','familyID',['residence_type',[1]])
    family.count_by_chw('Primary','familyID',['residence_type',[2]])
    family.count_by_chw('Secondary','familyID',['residence_type',[3]])
    family.count_by_chw('fam_regd','familyID')
    family.sum_by_chw('male_res','family_male_residents')
    family.sum_by_chw('fem_res','family_female_residents')
    family.sum_by_chw('male_nonres','family_male_non_residents')
    family.sum_by_chw('fem_nonres','family_female_non_residents')
    family.add_columns('tot_male', ['male_res','male_nonres'])
    family.add_columns('tot_fem', ['fem_res','fem_nonres'])
    
    return family.results