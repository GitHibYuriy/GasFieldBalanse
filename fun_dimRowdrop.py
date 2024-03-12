# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 12:01:35 2022

@author: zarub
"""

import numpy as np
import pandas as pd
# Модуль удаления строки размерностей

def dimRowdrop(df,indicator):
    # print('Enter dimRowdrop(df,indicator)')    
    # print('type', df.loc[0,indicator] ,type(df.loc[0,indicator]))
    
    if len(df[indicator]) > 0 and type(df.loc[0,indicator] )==str:
        df.drop(labels = [0],  axis=0, inplace=True)
        df.index =  df.index - 1          
   
    return  df   
    
# # # exempl 
# LogFilePath="D:\pyhton_try\Plots\Shablon_Kobz_3_grwell_out-1.xlsx"
# LogFilePath="D:\Phyton_MBE_exe\Project_Shablons\Out_files\Shablon_Kobz_3_grwell_out-21.xlsx"
# LogDataSheet='WellTestData'
# СalcDataSheet='Calculated'
# WellTest = pd.read_excel(LogFilePath,LogDataSheet)
# CalcData = pd.read_excel(LogFilePath,СalcDataSheet)
# print(CalcData)

# dimRowdrop(CalcData,'QgasSum')     
# print(CalcData)     
    
    
    
    
    
    
    
    


