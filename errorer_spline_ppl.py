# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:17:16 2020

@author: zarub
"""


import datetime
from datetime import datetime, timedelta
from datetime import date
import pandas as pd
import numpy as np
import math
import logging
rootLogger = logging.getLogger(__name__)

# Импорт собственных модулей
import prognosis_Ppl  as pprg
import fun_spline_interp  as spl
import fun_dimRowdrop as dr

def errorer(LogFilePath,values,lng_tuple):
    
     # Вызов расчет динамики пластового давления по датам в Calculated и 
     # values задаваемыми вызывающим модулем, например Minimizator
     
    CDD=pprg.prognosis_ppl(LogFilePath, values)
    y=CDD['pPl_C']
    
    # Из расчетной динамики CDD на даты в Calculated
    # Получкение расчетных давлений на даты фактического замера давления
    # в WellTestDataб используя сплайн-аппроксимацию 
   
    datasCalc=np.array(CDD['DateCalc'],dtype='datetime64[D]')
    a0=np.datetime64('1899-12-30')
    
    x= np.array(datasCalc-a0,'float64')
    WellTestData = pd.read_excel(LogFilePath,'WellTestData')
    
    # Удаление строки размерностей      
    WellTestData = dr.dimRowdrop(WellTestData,'ppl')
            
    WellTestData=WellTestData.sort_values(by=['dateTest'])
    Fact=WellTestData  
    Fact=Fact.reset_index()
    
    # Даты исследования скважин datasTest
    datasTest=np.array(Fact['dateTest'], dtype='datetime64[D]')
   
    
    # Начальная и конечные с листа  прогноза для границ интерполяции
    bgn=datasCalc[0]
    lst=datasCalc[len(datasCalc)-1]
   
    
    for i in range(0, len(Fact)): 
        
        if datasTest[i] < bgn:
                datasTest[i] = bgn
                Fact.loc[i,'Weight'] = 0
        if datasTest[i] > lst:
                
                datasTest[i] = lst
                Fact.loc[i,'Weight'] = 0
      
    xprognos = np.array(datasTest-a0,dtype='float64')
    
    if len(x) > 2:
        # используя сплайн-аппроксимацию
        
        sum_weight=0
        sum_sq_err=0
        progn = spl.splineMykub(x,y,xprognos)
        
        for i in range(0,len(xprognos)):
                WT = Fact.loc[i,'Weight'] 
                if pd.isna(Fact.loc[i,'Weight']):
                        WT = 1         
                sum_sq_err=(sum_sq_err+(Fact.loc[i,'ppl']-progn[i])**2 * WT)
                sum_weight=sum_weight+WT
        
    else:
        # используя линейную аппроксимацию
        
        dyx =(y[1]-y[0])/(x[1]-x[0])
        
        if len(x) == 2:
            sum_weight = 0
            sum_sq_err = 0
            progn = []
            print(lng_tuple['ls_add_err'])
            rootLogger.warning(lng_tuple['ls_add_err'])
            ay = y[0]
            ax = x[0]
            progn = ay + dyx *(xprognos-ax)
            for i in range(0,len(xprognos)-1):
                progn[i] = y[0] + dyx *(xprognos[i]-x[0])
                
                for i in range(0,len(xprognos)-1):  
                    WT = Fact.loc[i,'Weight'] 
                    if pd.isna(Fact.loc[i,'Weight']):
                        WT = 1    
                    sum_sq_err=(sum_sq_err+(Fact.loc[i,'ppl']-progn[i])**2 * WT)
                    sum_weight=sum_weight+WT    
                   
        else:             
            sum_weight=1
            sum_sq_err=0
            progn = 0
                      
    RMS=math.sqrt(sum_sq_err/sum_weight) 
  
    # print('from errorer',RMS, sum_sq_err,  sum_weight, progn, bgn, lst)
    return RMS, sum_sq_err,  sum_weight, progn, bgn, lst
