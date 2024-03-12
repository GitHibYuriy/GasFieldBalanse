# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 11:27:29 2020

@author: zarub
"""
import pandas as pd
import math
import numpy as np
from statistics import mean, median
import logging
rootLogger = logging.getLogger(__name__)

"""Импорт собственных модулей"""

import fun_spline_interp  as spl
import fun_Condensat_chrt  as chrt
import fun_Condensat_fact  as fct

def condensat(CndData,lng_tuple):
    # print('condensat main row 21')
    # print(CndData)
    
   

    try:
        CndData = chrt.kgf_interpolated(CndData,lng_tuple)
        inf =lng_tuple['ls_table_use_cnd']
       
    except:
        try:            
            print(lng_tuple['ls_fit_cnd'])  
            CndData = fct.condensat(CndData,lng_tuple)
            
            inf =lng_tuple['ls_history_use_cnd']
            
        except:
            CndData.loc[0,'a'] = 0
            CndData.loc[0,'b'] = 0
            CndData.loc[0,'c'] = 0
            inf = lng_tuple['ls_n_data_cnd']
            
            print(inf) 
        
    else:
        print(inf)
        rootLogger.warning(inf)
     
    return CndData

