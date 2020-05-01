#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:52:54 2020

@author: anant
"""

import pandas as pd

class CaseForm:
    def __init__(self, excelfile, cols):
        self.excel_path = excelfile
        self.cols = cols
        self.df = pd.read_excel(self.excel_path, usecols=self.cols, na_values=['---'])
        self.results = pd.DataFrame()

    def rename_columns(self, col_mapping):
        self.col_mapping = col_mapping
        self.df.rename(columns=col_mapping, inplace = True)

    def strip_str(self, str):
        self.df[str].str.replace(" ","")
        
    def count_by_chw(self, agg_col_nm, count_col, condition=None):
        if condition == None:
            grouped = self.df.groupby(['chw_name']).agg(count_col=(count_col,'count'))
        else:
            grouped = self.df[self.df[condition[0]].isin(condition[1])].groupby(['chw_name']).agg(count_col=(count_col,'count'))
        self.results = pd.concat([self.results, grouped], axis=1, sort=False)
        self.results.rename(columns={self.results.columns[-1]:agg_col_nm}, inplace = True)
        
    def sum_by_chw(self, agg_col_nm, sum_col, condition=None):
        if condition == None:
            grouped = self.df.groupby(['chw_name']).agg(sum_col=(sum_col,'sum'))
        else:
            grouped = self.df[self.df[condition[0]].isin(condition[1])].groupby(['chw_name']).agg(sum_col=(sum_col,'sum'))
        self.results = pd.concat([self.results, grouped], axis=1, sort=False)
        self.results.rename(columns={self.results.columns[-1]:agg_col_nm}, inplace = True)
        
    def remove_duplicates(self, sort_by, dupl_subset):
        self.df = self.df.sort_values(sort_by, ascending = True).drop_duplicates(
                        subset=dupl_subset, keep='last')
        
    def convert_to_Int64(self, cols):
        """Takes a dataframe, and a list of its columns, then converts the columns
        to numeric, then to dtype Int64 before returning the dataframe"""
        
        for col in cols:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            self.df = self.df.astype({col:'Int64'})
    
    def add_columns(self, new_col, to_add_cols):
        self.results[new_col] = 0
        for col in to_add_cols:
            print(col)
            self.results[new_col] = self.results[new_col] + self.results[col].fillna(0)
        self.results.drop(to_add_cols, axis=1, inplace=True)
        
    def drop_closed_cases(self):
        self.df = self.df[self.df['closed']==False]

    def filter_at_home(self):
        self.df = self.df[self.df['person_at_home']=='yes']

    def filter_by_date(self, filter_col, dates):
        self.df = self.df[(self.df[filter_col]>=dates[0]) & (self.df[filter_col]<=dates[1])]

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
