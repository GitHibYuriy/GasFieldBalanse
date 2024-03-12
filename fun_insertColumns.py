# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 13:35:33 2022

@author: zarub
"""
import pandas as pd
import numpy as np

# Упорядоченное добавление в результитрующий фрайм недостающих столбцов
def addColumns(df):
    allColumns = ['Days','Regim','pHead','A','B','qGas_C',
    	'kgf','QgasDif_C','QgasSum_C','Reserver_C','QcondDif_C','QcondSum_C',
    	'Influx_C','pPl_C','p-z_C','P_mid','pHead_C','dpRob_C','pBottom_C',
        'pore_Volume_C',' ','Remark' ]
    
    cols = list(df.columns)
    added=[]
   
    for j in range(len(allColumns)):
        if allColumns[j] not in cols:            
               added.append(allColumns[j])
            
    for i in range(len(added)):
        
        df.insert(loc=len(df.columns),column=added[i],value = np.nan )
    
    return df     
