# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 16:15:06 2022

@author: zarub
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import fun_dimRowdrop as dr

def markerStyle(m):
    markers=('o', 'v', 's','d','^','H', '<', '>', '8',  'p', '*', 'h', 'H', 'D', 
                                  'P', 'X' )
    clrs=('Blue','Red', 'Green', 'Yellow', 'Cyan', 'Magenta')
    
    mm=m//len(markers)
    mc=m//len(clrs)
   
    for i in range(mc):
        clrs=clrs+clrs
    for i in range(mm):
          markers= markers + markers
    for i in range(mm):
        marks= random.choice(markers)
    marks =  [markers[i] for i in range(m)]
    colors = [clrs[i] for i in range(m)]
    return [marks, colors]

def plot_PT(WellTestData,CC,lng_tuple):
    
    # Удаление строки размерностей    
    CalcData = CC
    CalcData = dr.dimRowdrop(CalcData,'QgasSum' )
    
    XC_ryad=np.array(CalcData['DateCalc'],dtype='datetime64[D]')
    YC_ryad=np.array(CalcData['pPl_C'])
    x_minC=np.min(XC_ryad)
    x_maxC=np.max(XC_ryad)
    try:
        LogDataNs = WellTestData
        LogDataNs = dr.dimRowdrop(LogDataNs,'ppl')
        X_ryad=np.array(WellTestData['dateTest'],dtype='datetime64[D]')
        # tests = len(X_ryad)
        
        x_min=np.min(X_ryad)
        x_max=np.max(X_ryad)
        if x_minC<x_min:
            x_min=x_minC
        if x_maxC>x_max:
           x_max=x_maxC   
           
        x_min=x_min-300
        x_max=x_max+300
          
        Y_ryad=np.array(WellTestData['ppl'])
        # y_min=np.min(X_ryad)
        y_max=1.1*np.max(Y_ryad)
        
        RyadName = WellTestData['RyadName']
        categories=np.unique(RyadName)
        plt.grid(True, linestyle='-', color='0.75')
        
        plt.plot(XC_ryad,YC_ryad,label='Forecast', color='blue') 
                        
        marks, colors=markerStyle(len(categories))    
            
        for i, RyadName in enumerate(categories):    
            plt.scatter('dateTest', 'ppl', 
                        data=WellTestData.loc[WellTestData.RyadName==RyadName, :], 
                        color=colors[i], edgecolors = 'Black',
                        marker=marks[i],   label=str(categories[i]))
        plt.gca().set(xlim=(x_min, x_max), ylim=(0, y_max))    
    except:
        # Если нет фактических данных по замеру пластового давления
        y_max=1.1*np.max(YC_ryad)
        plt.grid(True, linestyle='-', color='0.75')
        plt.plot(XC_ryad,YC_ryad,label='Forecast', color='blue')
        plt.gca().set(xlim=(x_minC, x_maxC), ylim=(0, y_max))
    
    plt.xlabel(lng_tuple['ls_date'], fontsize=8) 
    plt.ylabel(lng_tuple['ls_p_plt'], fontsize=8)

    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.title(lng_tuple['ls_dp_plt'], fontsize=8)
    plt.legend(fontsize=8) 
    
        
        
        