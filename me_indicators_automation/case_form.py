#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:52:54 2020

@author: anant
"""

import pandas as pd

class CaseForm:
    def __init__(self, filepath=None, cols=None, filetype=None):
        self.filepath = filepath
        self.cols = cols
        if self.filepath is not None:
            if filetype == 'text/csv':
                self.df = pd.read_csv(self.filepath, usecols=self.cols, na_values=['---'])
            else:
                self.df = pd.read_excel(self.filepath, usecols=self.cols, na_values=['---'], sheet_name=0)
        else:
            self.df = pd.DataFrame()
        self.results = pd.DataFrame()

    def rename_columns(self, col_mapping):
        self.col_mapping = col_mapping
        self.df.rename(columns=col_mapping, inplace = True)
        
    def create_duplicate_df2(self):
        self.df2 = self.df.copy(deep=True)

    def strip_str(self, str):
        self.df[str].str.replace(" ","")
        
    def count_by_chw(self, agg_col_nm, count_col, condition=None):
        if condition == None:
            grouped = self.df.groupby(['chw_name']).agg({count_col:'count'})
        else:
            grouped = self.df[self.df[condition[0]].isin(condition[1])].groupby(['chw_name']).agg({count_col:'count'})
        self.results = pd.concat([self.results, grouped], axis=1, sort=False)
        self.results[count_col].fillna(0, inplace = True)
        self.results.rename(columns={self.results.columns[-1]:agg_col_nm}, inplace = True)
        
    def countifs_by_chw(self, agg_col_nm, conditions):
        countifs_df = pd.DataFrame()
        for condition in conditions:
            countifs_df[condition[0]] = self.df[condition[0]].isin(condition[1])
        self.df['countifs_sum'] = countifs_df.sum(axis=1)
        self.df.loc[self.df['countifs_sum']>0, 'countifs_sum'] = 1
        grouped = self.df[self.df['countifs_sum']>0].groupby(['chw_name']).agg({'countifs_sum':'count'})
        self.results = pd.concat([self.results, grouped], axis=1, sort=False)
        self.results['countifs_sum'].fillna(0, inplace = True)
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
            self.results[new_col] = self.results[new_col] + self.results[col].fillna(0)
        self.results.drop(to_add_cols, axis=1, inplace=True)
        
    def filter_for_condition(self, filter_col, value):
        self.df = self.df[self.df[filter_col]==value]
        
    def filter_out_condition(self, filter_col, value):
        self.df = self.df[self.df[filter_col]!=value]

    def filter_by_date(self, filter_col, dates):
        self.df = self.df[(self.df[filter_col]>=dates[0]) & (self.df[filter_col]<=dates[1])]

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
        
    def concat_dataframes(self, dataframes):
        return pd.concat(dataframes, axis=1, sort=False)
