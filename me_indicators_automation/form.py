#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:52:54 2020

@author: anant
"""

import pandas as pd

class Form:
    def __init__(self, csvfile, cols):
        self.csv_path = csvfile
        self.cols = cols
        self.df = pd.read_csv(self.csv_path, index_col=None, usecols=self.cols,
                              na_values=['---'])
        self.results = pd.DataFrame()

    def rename_columns(self, col_mapping):
        self.col_mapping = col_mapping
        self.df.rename(columns=col_mapping, inplace = True)

    def strip_id(self):
        self.df['person_id'].str.replace(" ","")

    def filter_at_home(self):
        self.df = self.df[self.df['person_at_home']=='yes']

    def remove_duplicates(self):
        self.df = self.df.sort_values(['person_id','last_visit'],ascending = True
                            ).drop_duplicates('person_id', keep='last')
        
    def filter_by_date(self, filter_col, dates):
        self.df = self.df[(self.df[filter_col]>=dates[0]) & (self.df[filter_col]<=dates[1])]
        
    def add_columns(self, new_col, to_add_cols):
        self.results[new_col] = 0
        for col in to_add_cols:
            print(col)
            self.results[new_col] = self.results[new_col] + self.results[col].fillna(0)
        self.results.drop(to_add_cols, axis=1, inplace=True)

    def count_by_chw(self, agg_col_nm, count_col, condition=None):
        if condition == None:
            grouped = self.df.groupby(['chw_name']).agg(count_col=(count_col,'count'))
        else:
            grouped = self.df[self.df[condition[0]].isin(condition[1])].groupby(['chw_name']).agg(count_col=(count_col,'count'))
        self.results = pd.concat([self.results, grouped], axis=1, sort=False)
        self.results.rename(columns={self.results.columns[-1]:agg_col_nm}, inplace = True)
    
    def count_by_chw_with_df(self, df, agg_col_nm, count_col, condition=None):
        if condition == None:
            grouped = df.groupby(['chw_name']).agg(count_col=(count_col,'count'))
        else:
            grouped = df[df[condition[0]].isin(condition[1])].groupby(['chw_name']).agg(count_col=(count_col,'count'))
        self.results = pd.concat([self.results, grouped], axis=1, sort=False)
        self.results.rename(columns={self.results.columns[-1]:agg_col_nm}, inplace = True)

    def count_by_chw_date_condition(self, agg_col_nm, count_col, condition=None):
        grouped = self.df[(self.df[condition[0]]>=condition[1][0]) & (self.df[condition[0]]<=condition[1][1])].groupby(['chw_name']).agg(count_col=(count_col,'count'))
        self.results = pd.concat([self.results, grouped], axis=1, sort=False)
        self.results.rename(columns={self.results.columns[-1]:agg_col_nm}, inplace = True)
        
    def count_by_chw_num_condition(self, agg_col_nm, count_col, condition=None):
        if condition[1] == '<':
            grouped = self.df[self.df[condition[0]]<condition[2]].groupby(['chw_name']).agg(count_col=(count_col,'count'))
        elif condition[1] == '>':
            grouped = self.df[self.df[condition[0]]>condition[2]].groupby(['chw_name']).agg(count_col=(count_col,'count'))
        elif condition[1] == '<=':
            grouped = self.df[self.df[condition[0]]<=condition[2]].groupby(['chw_name']).agg(count_col=(count_col,'count'))
        elif condition[1] == '>=':
            grouped = self.df[self.df[condition[0]]>=condition[2]].groupby(['chw_name']).agg(count_col=(count_col,'count'))
        elif condition[1] == '==':
            grouped = self.df[self.df[condition[0]]==condition[2]].groupby(['chw_name']).agg(count_col=(count_col,'count'))
        self.results = pd.concat([self.results, grouped], axis=1, sort=False)
        self.results.rename(columns={self.results.columns[-1]:agg_col_nm}, inplace = True)