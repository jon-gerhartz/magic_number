import pandas as pd
import numpy as np

def clean_data(raw):

    #create list of non data rows
    non_data = [1,7,13,19,20,21,27,33]

    #drop non data rows
    raw_rows = raw.drop(non_data, axis=0)

    #create list of non data cols
    drop_cols = ["Unnamed: 0"]

    #drop non data cols
    data = raw_rows.drop(drop_cols,axis=1)

    
    data.columns = data.iloc[0]

    #remove extra header
    data = data.iloc[1:len(data)]

    #fill first col with DR
    data = data.rename({'Unnamed: 0_level_1':'DR'}, axis=1)

    #create list of cols for magic df
    magic_cols = [0,1,2,3,7,8]

    #create df with condensed cols
    magic = data.iloc[:,magic_cols]
    
    #set data type of Lg, D, W, L cols
    magic = magic.astype({'DR':'int32','Lg': str,'D':str,'W':'int32','L':'int32'})

    #add Div column to magic
    magic['Div'] = magic['Lg'] + magic['D']

    #add col games remaining as GR
    magic['GR'] = 162 - (magic['W'] + magic['L'])

    
    return magic


def wildcard(data,league):   
    #create bool for non first place teams
    bool = data["DR"] != 1

    #create bool for league
    league_bool = data['Lg'] == league

    #create combo bool
    combo = bool & league_bool

    #create df of non first place teams
    wild = data[combo]

    #sort potential wildcard teams by wins and reset index
    wild_sorted = wild.sort_values("W", ascending = False).reset_index()

    #create new column league + "_wildcard_rank"
    wild_sorted[league + " Wildcard Rank"] = (wild_sorted.index + 1)

    #drop extra columns  
    wild_final = wild_sorted.drop(['DR','Lg', 'D', 'W','L','Div', 'GR','index'], axis=1)

    return wild_final


def div_magic(data,div):
    #create div bool
    div_bool = data['Div'] == div

    #create first bool
    first_bool = data['DR'] == 1

    #create second bool
    second_bool = data['DR'] == 2
     
    #create bool for first and second place in division
    first_second_bool = first_bool | second_bool

    #create combo bool
    combo = div_bool & first_second_bool

    #create combo df
    div_data = data[combo]

    #create MN col 
    div_data['MN'] = (div_data['GR'] + 1) - (div_data.iloc[1,5] - div_data.iloc[0,5])
    div_data.reset_index()

    #drop 2nd place team
    div_data.drop([div_data.index[1]], inplace = True)

    #remove unessasary cols
    cols = ['Tm','MN']
    mn = div_data[cols]


    return mn
 

def wildcard_magic (data, Lg):
    #create bool for Lg
    Lg_bool = data['Lg'] == Lg
    
    #create df for lg
    lg_df = data[Lg_bool]
    
    #create bool for #1 wildcard rank
    first_wc_bool = data[Lg+" Wildcard Rank"] == 1
    
    #create bool for #2 wildcard rank
    second_wc_bool = data[Lg+" Wildcard Rank"] == 2
    
    #create combo bool
    combo = first_wc_bool | second_wc_bool
    
    #create df for wildcard mns
    lg_wc_mns = lg_df[combo]
    
    #create MN col 
    lg_wc_mns['MN WC'] = (lg_wc_mns['GR'] + 1) - (lg_wc_mns.iloc[1,5] - lg_wc_mns.iloc[0,5])
    sorted1 = lg_wc_mns.sort_values(Lg+" Wildcard Rank",axis=0,ascending = True)
        
    #drop 2nd place team
    reset = sorted1.reset_index()
    dropped = reset.drop(reset.index[1])
    
    #remove unessasary cols
    cols = ['Tm','MN WC']
    mn = dropped[cols]

    
    return mn

