#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:22:07 2020

@author: anant
"""

from me_indicators_automation.case_form import CaseForm

def clean(form):
    col_mapping = {"woman_ID":"person_id", "woman_at_home":"person_at_home"}
    form.rename_columns(col_mapping)
    form.strip_str('person_id')

## Pregnancy Screening
def anc_metrics(file, dt1='2015-01-01', dt2='2050-01-01', content_type='text/csv'):
    
    #file = './Data/6. ANC_data_Magh_2076.xlsx'
    #dt1 = '2020-01-01'
    #dt2 = '2020-04-30'
    
    cols = ['chw_name', 'woman_at_home', 'visit_type', 'woman_ID', 'followup.pregnancy_status', 
            'agrees_for_service', 'last_visit', 'labs_complete', 'record_usg_findings', 'usg_complete',
            'high_risk_vdrl', 'high_risk.high_risk_urine_sugar', 'high_risk_hcv', 'high_risk.high_risk_hiv',
            'high_risk_rh_negative', 'high_risk_hbsag', 'high_risk_anemia', 'high_risk_urine_protein',
            'high_risk_placenta_previa', 'high_risk_fetal_presentation', 'high_risk_no_of_fetus',
            'high_risk', 'anc_visit1_month', 'anc_visit2_month', 'anc_visit3_month', 'anc_visit4_month',
            'anc_visit5_month', 'anc_visit6_month', 'anc_visit7_month', 'anc_visit8_month', 'anc_visit9_month',
            'anc_visit10_month', 'lmp_group.weeks_pregnant', 'immun-meds.albendazole_taken',
            'immun-meds.daily_iron', 'immun-meds.tt_actual_first_dose']
    
    anc = CaseForm(filepath=file, cols=cols, filetype=content_type)
    clean(anc)
    anc.filter_by_date('last_visit', [dt1,dt2])
    
    anc_home = CaseForm()
    anc_home.df = anc.df.copy()
    
    '''
    CALCULATE FOR HOME VISITS
    '''
    anc_home.filter_for_condition('visit_type', 'home')
    anc_home.filter_out_condition('followup.pregnancy_status', 'No')
    anc_home.remove_duplicates(sort_by=['person_id', 'person_at_home', 'last_visit'],dupl_subset=['person_id'])
    
    anc_home.count_by_chw('home_visit_yes','person_id', ['person_at_home',['yes']])
    anc_home.count_by_chw('home_visit_no','person_id', ['person_at_home',['no']])
    #anc_home.add_columns('home_visit',['home_visit_yes', 'home_visit_no'])
    
    anc_home.count_by_chw('agrees_for_service_yes','person_id', ['agrees_for_service',['yes']])
    anc_home.count_by_chw('agrees_for_service_no','person_id', ['agrees_for_service',['no']])
    #anc_home.add_columns('agrees_for_service',['agrees_for_service_yes', 'agrees_for_service_no'])
    
    anc_home.filter_for_condition('agrees_for_service', 'yes')
    
    anc_home.count_by_chw('labs_complete','person_id', ['labs_complete',['yes']])
    anc_home.count_by_chw('record_usg_findings','person_id', ['record_usg_findings',['yes']])
    anc_home.count_by_chw('usg_complete','person_id', ['usg_complete',['yes']])
    
    anc_home.countifs_by_chw('lab_high_risk', [['high_risk_vdrl',['yes']], 
                                       ['high_risk.high_risk_urine_sugar',['yes']],
                                       ['high_risk_hcv',['yes']], 
                                       ['high_risk.high_risk_hiv',['yes']], 
                                       ['high_risk_rh_negative',['yes']], 
                                       ['high_risk_hbsag',['yes']], 
                                       ['high_risk_anemia',['yes']],
                                       ['high_risk_urine_protein',['yes']]])
    
    anc_home.countifs_by_chw('USG_high_risk', [['high_risk_placenta_previa',['yes']], 
                                       ['high_risk_fetal_presentation',['yes']],
                                       ['high_risk_no_of_fetus',['yes']]])
    
    anc_home.count_by_chw('high_risk', 'person_id', ['high_risk',[1]])
    
    
    '''
    CALCULATE FOR GROUP ANC VISITS
    '''
    anc_group = CaseForm()
    anc_group.df = anc.df.copy()
    
    '''
    GOVERNMENT PROTOCOL
    '''
    
    anc_proto = CaseForm()
    anc_proto.df = anc.df.copy()
    anc_proto.remove_duplicates(sort_by=['person_id', 'person_at_home', 'last_visit'],dupl_subset=['person_id'])
    
    anc_proto.countifs_by_chw('4th_complete', [['anc_visit1_month',[4]], 
                                       ['anc_visit2_month',[4]],
                                       ['anc_visit3_month',[4]], 
                                       ['anc_visit4_month',[4]], 
                                       ['anc_visit5_month',[4]], 
                                       ['anc_visit6_month',[4]], 
                                       ['anc_visit7_month',[4]],
                                       ['anc_visit8_month',[4]],
                                       ['anc_visit9_month',[4]],
                                       ['anc_visit10_month',[4]]])
    anc_proto.countifs_by_chw('6th_complete', [['anc_visit1_month',[6]], 
                                       ['anc_visit2_month',[6]],
                                       ['anc_visit3_month',[6]], 
                                       ['anc_visit4_month',[6]], 
                                       ['anc_visit5_month',[6]], 
                                       ['anc_visit6_month',[6]], 
                                       ['anc_visit7_month',[6]],
                                       ['anc_visit8_month',[6]],
                                       ['anc_visit9_month',[6]],
                                       ['anc_visit10_month',[6]]])
    anc_proto.countifs_by_chw('8th_complete', [['anc_visit1_month',[8]], 
                                       ['anc_visit2_month',[8]],
                                       ['anc_visit3_month',[8]], 
                                       ['anc_visit4_month',[8]], 
                                       ['anc_visit5_month',[8]], 
                                       ['anc_visit6_month',[8]], 
                                       ['anc_visit7_month',[8]],
                                       ['anc_visit8_month',[8]],
                                       ['anc_visit9_month',[8]],
                                       ['anc_visit10_month',[8]]])
    anc_proto.countifs_by_chw('9th_complete', [['anc_visit1_month',[9]], 
                                       ['anc_visit2_month',[9]],
                                       ['anc_visit3_month',[9]], 
                                       ['anc_visit4_month',[9]], 
                                       ['anc_visit5_month',[9]], 
                                       ['anc_visit6_month',[9]], 
                                       ['anc_visit7_month',[9]],
                                       ['anc_visit8_month',[9]],
                                       ['anc_visit9_month',[9]],
                                       ['anc_visit10_month',[9]]])
    anc_proto.countifs_by_chw('Proto_vis_cmplt', [['anc_visit1_month',[4, 6, 8, 9]], 
                                       ['anc_visit2_month',[4, 6, 8, 9]],
                                       ['anc_visit3_month',[4, 6, 8, 9]], 
                                       ['anc_visit4_month',[4, 6, 8, 9]], 
                                       ['anc_visit5_month',[4, 6, 8, 9]], 
                                       ['anc_visit6_month',[4, 6, 8, 9]], 
                                       ['anc_visit7_month',[4, 6, 8, 9]],
                                       ['anc_visit8_month',[4, 6, 8, 9]],
                                       ['anc_visit9_month',[4, 6, 8, 9]],
                                       ['anc_visit10_month',[4, 6, 8, 9]]])
    
    anc_proto.count_by_chw('anc_edd_mnth', 'person_id', ['lmp_group.weeks_pregnant', [36]])
    anc_proto.count_by_chw('albendazole', 'person_id', ['immun-meds.albendazole_taken', ['yes']])
    anc_proto.count_by_chw('daily_iron', 'person_id', ['immun-meds.daily_iron', ['yes']])
    anc_proto.count_by_chw('tt_first_dose', 'person_id', ['immun-meds.tt_actual_first_dose', ['yes']])
    
    anc.results = anc.concat_dataframes([anc_home.results, anc_group.results, anc_proto.results])
    print(dt1, " - ", dt2)
    return anc.results