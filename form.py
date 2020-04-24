#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:52:54 2020

@author: anant
"""

import pandas as pd

class Form:
    def __init__(self, csv_path, cols):
        self.csv_path = csv_path
        self.cols = cols
        self.df = pd.read_csv(self.csv_path, index_col=None, usecols=self.cols,
                              na_values=['---'])
        self.results = pd.DataFrame()
        
    def rename_columns(self, col_mapping):
        self.col_mapping = col_mapping
        self.df.rename(columns=col_mapping, inplace = True)
    
    def strip_id(self):    
        self.df['person_id'].str.replace(" ","")
        
    def only_at_home(self):
        self.df = self.df[self.df['person_at_home']=='yes']
    
    def remove_duplicates(self):
        self.df = self.df.sort_values(['person_id','last_visit'],ascending = True
                            ).drop_duplicates('person_id', keep='last')
        
    def count_by_chw(self, agg_col_nm, filter_col, condition=None):
        if condition == None:
            grouped = self.df.groupby(['chw_name']).agg(filter_col=(filter_col,'count'))
        else:
            grouped = self.df[self.df[condition[0]].isin(condition[1])].groupby(['chw_name']).agg(filter_col=(filter_col,'count'))
        self.results = pd.concat([self.results, grouped], axis=1)
        self.results.rename(columns={self.results.columns[-1]:agg_col_nm}, inplace = True)