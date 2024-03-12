# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 08:22:20 2020

@author: zarub
"""


import numpy as np

from matplotlib.figure import Figure
from tkinter import *
from pandas import DataFrame
import tkinter as tk

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import fun_dimRowdrop as dr
import groupsFinder  as gf
import fun_insertRegColumns  as insR

def plot_qt(LogFilePath,CD,values,lng_tuple):
    
    markers=('o', 'v', 's','d','^','H', '<', '>', '8',  'p', '*', 'h', 'H', 'D', 
                                      'P', 'X' )
    clrs = ('Blue','Red', 'Purple',  'Cyan', 'Magenta', 'Orange','Black')
    styls = ("solid","dotted","dashed","dashdot")
    
    CC, WellTestData, pzData, RegimeGroups, GroupList, CGF = CD
    CalcData = CC
    CalcData = dr.dimRowdrop(CalcData,'QgasSum' )
  
    
    FactData=pd.DataFrame()
    SumData=pd.DataFrame()
    for i in range(1, len(CalcData)) :
        
        if CalcData.loc[i,'QgasSum']>=0:
            FactData.loc[i,'DateCalc']=CalcData.loc[i,'DateCalc']
            FactData.loc[i,'qGas_C']=CalcData.loc[i,'qGas_C']
        else:
            SumData.loc[i,'DateCalc']=CalcData.loc[i,'DateCalc']
            SumData.loc[i,'qGas_C']=CalcData.loc[i,'qGas_C']
        FactData = FactData.dropna(axis=0, how='any')
        SumData = SumData.dropna(axis=0, how='any')  
        
  
    
    x_min=np.min(SumData['DateCalc'])
    x_max=np.max(SumData['DateCalc']) 
    
    Xsum_ryad=np.array(SumData['DateCalc'],dtype='datetime64[D]')
    Ysum_ryad = np.array(SumData['qGas_C'])

    y_max = 1.1*np.max(Ysum_ryad)
    try: 
        YF_ryad=np.array(FactData['qGas_C'])
        XF_ryad=np.array(FactData['DateCalc'])
        
        x_min=np.min(XF_ryad)
        y_maxF = 1.1*np.max(YF_ryad) 
        if y_max < y_maxF:
            y_max = y_maxF     
        
        plt.grid(True, linestyle='-', color='0.75')    
        plt.step(XF_ryad, YF_ryad,  color="g", 
                    marker ='o', where='mid',  label="Fact")
    except:
        y_max = y_max 
    
    nr = len(GroupList)
    if nr > 0: 
        for j in range (0,nr):
            
            name=GroupList[j]  
            
            # Удаление строки размерностей
            # RegimeGroups[j] = dr.dimRowdrop(RegimeGroups[j],'qGas_C' )
            Rg=pd.DataFrame()
            Rg['DateCalc']=RegimeGroups[j]['DateCalc']
            Rg['qGas_C']=RegimeGroups[j]['qGas_C']
            Rg = Rg.dropna(axis=0, how='any')
            y_maxRg = np.max(Rg['qGas_C'])
            if y_maxRg > y_max:
                y_max = y_maxRg
            
            mark= random.choice(markers)
            clr = random.choice(clrs)
            stl = random.choice(styls)
            plt.step(Rg['DateCalc'], Rg['qGas_C'],  
                        where='mid',color=clr, linestyle=stl,
                             marker =mark, markersize=3, label=name)
        
    plt.step(Xsum_ryad, Ysum_ryad, color="g", where='mid', label="Total") 
 
    plt.gca().set(xlim=(x_min, x_max), ylim=(0, y_max))
    plt.xlabel(lng_tuple['ls_date'], fontsize=8) 
    plt.ylabel(lng_tuple['ls_q_plt'], fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.title(lng_tuple['ls_dq_plt'], fontsize=8)
    plt.legend(fontsize=8) 
    
    
    
        
