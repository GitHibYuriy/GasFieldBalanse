# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 11:27:29 2020

@author: zarub
"""
import pandas as pd
import numpy as np


"""Импорт собственных модулей"""
import parabola_fit  as prf

def condensat(CndData,lng_tuple):
    # print('Inputed to Condenszt.fact CndData')
    # print(CndData)
    Cnd = CndData.copy(deep=True)
    # Удаление строк, несодержащих добычу конденсата
    Cnd=Cnd[Cnd["QcondSum"]>0] 
    Cnd.reset_index(drop=True, inplace=True)
    for row in Cnd.index:
        row=np.int64(row)
    # print('Cnd in Condenszt.fact CndData')
    # print(Cnd)    
        
        
    # pPl=Cnd['P_mid']
    # Cnd=pd.DataFrame(columns =["P_mid", "sQcond",  "sQgas", "QcondDif", "QgasDif","KGF"])
    Cnd["QcondSum"] = Cnd['QcondSum']*1000
    # Cnd["sQgas"] = Cnd['QgasSum'] 
    # Cnd["P_mid"] = Cnd['P_mid'] 
    # Cnds = Cnd
    
    # print('Cnd in Condenszt.fact CndData')
    # print(Cnd) 
    # print(len( Cnd["P_mid"])) 
    
    # Cnd = Cnd.sort_values(by="QgasSum", ignore_index=True)
    # Cnd.reset_index(drop=True, inplace=True)
    # print(Cnd.columns)
    for i in range(0,len( Cnd["P_mid"]-1)):
        Cnd.loc[i,"Pres"] = Cnd.loc[i,"P_mid"]
        
        if i==0:
            c=Cnd.loc[0,"QcondSum"]
            Cnd.loc[0,"QgasDif"]=Cnd.loc[0,"QgasSum"]
            g=Cnd.loc[0,"QgasSum"]
            Cnd.loc[0,"kgf"] = c/ g
        else:
            x2=Cnd.loc[i,"QcondSum"]
            x1=Cnd.loc[i-1,"QcondSum"]
            Cnd.loc[i,"QcondDif"]=x2-x1
            y2=Cnd.loc[i,"QgasSum"]
            y1=Cnd.loc[i-1,"QgasSum"]
            Cnd.loc[i,"QgasDif"]=y2-y1
            Cnd.loc[i,"kgf"] = Cnd.loc[i,"QcondDif"]/ Cnd.loc[i,"QgasDif"]

    
    # print('Cnd in Condenszt.fact to fitting')
    # print(Cnd)
    
    if len(Cnd["kgf"]) < 3:
        a = 0
        b = 0 
        c = np.mean(Cnd["kgf"])
    else:
        a, b, c =  prf.fitting(Cnd,lng_tuple)
    
    CndData.loc[0,'a'] = a
    CndData.loc[0,'b'] = b
    CndData.loc[0,'c'] = c
    
    # print('CndData in Condenszt.fact after fitting')
    # print(CndData)
    
    
    CndData['Pres'] = Cnd['Pres']
    CndData['kgf'] = Cnd['kgf']

    for i in range(len(CndData)):
        p =  CndData.loc[i,'P_mid'] 
        CndData.loc[i,'KGF'] = a*p*p + b*p +c
        
    for i in range(0,len( CndData["P_mid"]-1)):
      
        
        if i==0:
            CndData.loc[i,'QcondSum'] = 0 
            CndData.loc[i,'QcondDif'] = 0
            
        else:
            CndData.loc[i,'QcondDif'] = (CndData.loc[i,'QgasSum']-CndData.loc[i-1,'QgasSum'])*CndData.loc[i,'KGF']
            CndData.loc[i,'QcondSum'] = CndData.loc[i-1,'QcondSum'] + CndData.loc[i,'QcondDif']
            
    # print('CndData rez  Condenszt.fact to fitting')
    # print(CndData)        

    return CndData
