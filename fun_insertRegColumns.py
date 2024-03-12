# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 13:35:33 2022

@author: zarub
"""
import pandas as pd
import numpy as np

# Упорядоченное добавление в результитрующий фрайм недостающих столбцов
def addRegColumns(df):
    allColumns = ['Days','qGas_C', 'QgasDif_C', 'pHead_C','pBottom_C','dpRob_C',' ','Remark']
    cols = list(df.columns)
    added=[]
    m = len(df.columns)
    for j in range(len(allColumns)):
        if allColumns[j] not in cols:            
               added.append(allColumns[j])
               
    added = pd.array(added)       
    for i in range(0,len(added)):
     
        df.insert(loc=m+i,column=added[i],value = np.nan )
    
    return df     
