# -*- coding: utf-8 -*-
"""
Created on Fri May 27 15:21:24 2022

@author: zarub
"""


import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
import logging
rootLogger = logging.getLogger(__name__)




def kgf_interpolated(CndData,lng_tuple):
    
    Cnd = CndData.copy(deep=True)
   
    i = 0
    for i in range(len(Cnd)):
        if  Cnd.loc[i,'Pres'] >0:
          strokxy = i
      
    xy = pd.DataFrame(columns = ['x','y','h']) 

    for i in range(strokxy+1):      
        xy.loc[i,'x']= Cnd.loc[i,'Pres']
        xy.loc[i,'y']= Cnd.loc[i,'kgf']

    xy = xy.sort_values(by='x',ascending=True)   
    
    "Удаление <ложных> точек"
    for k in range(1,len(xy)):
        xy.loc[k,'h']= xy.loc[k,'x']-xy.loc[k-1,'x']
    xy=xy.drop(xy[xy.h==0].index) 
    xy=xy.reset_index()
    xy=xy.drop(['index'],axis=1) 
    
    
    
    
    xpr_min= min(xy['x'])
    xpr_max= max(xy['x'])
    
   # Точка начала конденсации
    xn_cond = Cnd.loc[0,'Pres']
    yn_cond = Cnd.loc[0,'kgf']
    
    # yn_cond = max(xy['y'])
    j = 0
    while Cnd.loc[j,'kgf'] >= yn_cond:
            xn_cond = Cnd.loc[j,'Pres']
            j=j+1
    
  
    for i in range(len(Cnd['P_mid'])):
        
        if Cnd.loc[i,'P_mid']>xpr_max:
            Cnd.loc[i,'P_mid']=xpr_max
        if Cnd.loc[i,'P_mid']<xpr_min:
            Cnd.loc[i,'P_mid']=xpr_min
    if len(xy['x'])>1:
        spline = CubicSpline(xy['x'], xy['y'])
        CndData['KGF'] = spline(Cnd['P_mid'])
        j = 0
        while CndData.loc[j,'P_mid'] >= xn_cond:
              CndData.loc[j,'KGF'] =  yn_cond 
              j=j+1
    if len(xy['x'])==1:
        CndData['KGF'] = xy.loc[0,'y']
   
    return CndData


#  exempl 

# LogFilePath="D:\Phyton_MBE_exe\Project_Shablons\Out_files\Shablon_Kobz_3_grwell_out-7.xlsx"
# CndData = CalcData = pd.read_excel(LogFilePath,'CondFactor')
# CndData = dr.dimRowdrop(CndData,'Pres' )
# print(CndData)
# print(kgf_interpolated(CndData,0))