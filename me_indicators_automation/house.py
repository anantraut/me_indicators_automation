#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 16:01:07 2019

@author: anant
"""

#import modules
from me_indicators_automation.case_form import CaseForm

## House data
def house_metrics(file):
    #file = './Data/5. House Data Summary Report_upto Kartik.xlsx'
    cols = ['chw_name','houseID','house_name','has_plate','last_modified_date','closed']
    house = CaseForm(file, cols)
    
    house.strip_str('houseID')
    
    house.drop_closed_cases()
    house.remove_duplicates(sort_by=['houseID', 'house_name', 'last_modified_date'],dupl_subset=['houseID', 'house_name'])
    
    house.count_by_chw('has_plate','houseID',['has_plate',['yes']])
    house.count_by_chw('no_plate','houseID',['has_plate',['no']])
    
    return house.results