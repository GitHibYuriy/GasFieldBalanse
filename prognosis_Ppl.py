# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:15:14 2020

@author: zarub
"""
import datetime
import pandas as pd
import numpy as np
import math


# Импорт собственных модулей
import func_zRC as Z
import fun_pZab_Phead as pz
import fun_Phead_pZab as pH
import fun_ppl as ppl
import fun_q_pHead  as qpH
import fun_q_Dp  as qDp
import fun_q_pZab  as qpZ
import fun_dimRowdrop as dr

def prognosis_ppl(LogFilePath,values):

         # Расчет изменеия пластового давления соответственно фактической добычи
         # в Calculated и values задаваемыми вызывающим модулем, например Minimizator
    СalcDataSheet='Calculated'
    CD = pd.read_excel(LogFilePath,СalcDataSheet)
      
     # Удаление строки размерностей      
    CD = dr.dimRowdrop(CD,'QgasSum')
       
    strokAll=len(CD.index)
    
    if  pd.isna(CD.loc[0,'QwaterSum']):
               if pd.isna(values[6]):
                   CD.loc[0,'QwaterSum'] = 0
               else:
                   CD.loc[0,'QwaterSum'] = values[6]
    for i in range(1,strokAll):
        if  pd.isna(CD.loc[i,'QwaterSum']):
            CD.loc[i,'QwaterSum'] = CD.loc[i-1,'QwaterSum'] 

    QgasSum=CD['QgasSum']  
    
    for i in range(strokAll):
        Qg=QgasSum.loc[i]        
        if  Qg >=0:
          strokFact =i
    
          
    Ppl=values.loc[3]
    Reserver=values.loc[2]
    Q_ini=values.loc[4]
    Water_ini=values.loc[6]
    Influx_ini=values.loc[27]
    Days=0    
    clmn=({'DateCalc':[],'QgasSum_C':[],'QwaterSum':[],'Days':[],
           'Reserver_C':[],'Influx_C':[],'pPl_C':[]})
    res=pd.DataFrame(clmn)
        
    res['DateCalc']=CD.loc[0:strokFact,'DateCalc']
   
    res['QgasSum_C']=CD.loc[0:strokFact,'QgasSum']
    res['QwaterSum']=CD.loc[0:strokFact,'QwaterSum']
    res.loc[0,'Days']=None
    res.loc[0,'pPl_C']=ppl.GDW_p_plast(Ppl, Reserver, Q_ini, 
                            Water_ini, Influx_ini, Days,  values)[0] 
    res.loc[0,"QgasSum_C"]=0
    res.loc[0,"Reserver_C"]=values.loc[2]
    res.loc[0,"Influx_C"]=Influx_ini

    for i in range(0,strokFact+1):
        if i==0:
            res.loc[i,'Days']=0
            
        else:            
            res.loc[i,'Days']=((res.loc[i,'DateCalc']-res.loc[i-1,'DateCalc']).days) 
            
            
    for i in range(1,strokFact+1):   
        res.loc[i,'Reserver_C']=(res.loc[0,'Reserver_C']-
                                      res.loc[i,'QgasSum_C'])
        
        Reserver=res.loc[0,'Reserver_C']
        QgasSum=res.loc[i,'QgasSum_C']
        QwaterSum=res.loc[i,'QwaterSum']
        Influx=res.loc[i-1,"Influx_C"]
        Days=res.loc[i,'Days']
        ppp=ppl.GDW_p_plast(Ppl, Reserver, QgasSum, 
                        QwaterSum, Influx, Days,  values)
        res.loc[i,'pPl_C']=ppp[0]
        res.loc[i,'Influx_C']=ppp[1]
    
    return res    

 