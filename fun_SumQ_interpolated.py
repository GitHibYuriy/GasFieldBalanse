# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 10:25:19 2020

@author: zarub
"""


import datetime
from datetime import datetime, timedelta
from datetime import date
import pandas as pd
import numpy as np
import logging
rootLogger = logging.getLogger(__name__)


# Импорт собственных модулей
import fun_dimRowdrop as dr
import fun_spline_interp  as spl


def SumQ_interpolated(LogFilePath, WellTestData, values,lng_tuple):
    
     # Удаление строки размерностей
    WellTestData = dr.dimRowdrop(WellTestData,'ppl')

    WTD=WellTestData.sort_values(by=['dateTest'])
    WTD=WTD.reset_index()
    WTD=WTD.drop(['index'],axis=1)
    a0=np.datetime64('1899-12-30')
    
    # Формирование таблицы известных х и у 
    
    factData = pd.read_excel(LogFilePath,'Calculated')
    factData = dr.dimRowdrop(factData,'QgasSum')
    
    QgasSum = factData['QgasSum']
    factData= factData.sort_values(by=['DateCalc'])
    factData=factData.reset_index()
    factData=factData.drop(['index'],axis=1)
   
    strokAll=len(factData.index) 
    QgasSum=factData['QgasSum']
    for i in range(strokAll):
        Qg=QgasSum.loc[i]
        if  Qg >=0:
          strokFact =i
    m=strokFact
    
    clmn={'DateCalc':[],'QgasSum':[]}
    fact_xy=pd.DataFrame(clmn)
    
    for i in range(strokFact+1):
            fact_xy.loc[i,'DateCalc']=factData.loc[i, 'DateCalc']
            fact_xy.loc[i,'QgasSum']=factData.loc[i,'QgasSum']
    
    bd=values.loc[29]
    Bdate = bd
    if fact_xy.loc[0,'QgasSum'] > 0: 
        fact_xy.loc[strokFact]=[Bdate,0]
   
    fact_xy=fact_xy.sort_values(by=['DateCalc'])
    datas_Fact =np.array(fact_xy['DateCalc'], dtype='datetime64[D]')
    SumQ_Fact = np.array(fact_xy['QgasSum'])
    
    x = np.array(datas_Fact-a0,'float64')
    y = SumQ_Fact
    # Даты интерполяции проверка конечных и начальных дат
    
    datasTest = np.array(WTD['dateTest'], dtype='datetime64[D]')
    a0=np.datetime64('1899-12-30')
    
    bgn=datasTest[0]
    lst=datas_Fact[strokFact]
    
   
    for i in range(0, len(WTD)): 
        
        if datasTest[i] < bgn:
                datasTest[i] = bgn
                WTD.loc[i,'Weight'] = 0
        if datasTest[i] > lst:
                datasTest[i] = lst
    
    xprognos = np.array(datasTest-a0,dtype='float64')
    
   
  
    if strokFact==1:
        print(lng_tuple['ls_2poin_int'])
        rootLogger.info(lng_tuple['ls_2poin_int'])
        for i in range(0,len(xprognos)):
            if xprognos[i]<x[0]:
                
                WTD.loc[i,'Intepolated']= y[0]
            else:
                
                dydx = (y[1]-y[0])/(x[1]-x[0])
                WTD.loc[i,'Intepolated'] =  dydx *(xprognos[i]-x[0]) 
               
    else:
        print(lng_tuple['ls_spline_int'])
        rootLogger.info(lng_tuple['ls_spline_int'])
        WTD['Intepolated'] = spl.splineMykub(x,y,xprognos)
    
    
    
    return WTD


