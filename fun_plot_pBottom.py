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

def plot_pBottom(CD,values,lng_tuple):
    
    markers=('o', 'v', 's','d','^','H', '<', '>', '8',  'p', '*', 'h', 'H', 'D', 
                                      'P', 'X' )
    clrs = ('Blue','Red', 'Purple',  'Cyan', 'Magenta', 'Orange','Black')
    styls = ("solid","dotted","dashed","dashdot")
    
    CC, WellTestData, pzData, RegimeGroups, GroupList, CGF = CD
    CalcData = CC
    
    CalcData = dr.dimRowdrop(CalcData,'QgasSum' )
    
    X_ryad=np.array(CalcData['DateCalc'],dtype='datetime64[D]') 
    x_min=np.min(X_ryad)
    x_max=np.max(X_ryad)
    
    FactData=pd.DataFrame()
   
    for i in range(1, len(CalcData)) :
        
        if CalcData.loc[i,'QgasSum']>=0:
            FactData.loc[i,'DateCalc']=CalcData.loc[i,'DateCalc']
            FactData.loc[i,'pBottom_C']=CalcData.loc[i,'pBottom_C']
        FactData = FactData.dropna(axis=0, how='any')    

    y_max = 0
    nr = len(GroupList)
    if nr > 0: 
        for j in range (0,nr):
            
            name=GroupList[j]  
            
            # Удаление строки размерностей
            # RegimeGroups[j] = dr.dimRowdrop(RegimeGroups[j],'Wells' )
            Rg=pd.DataFrame()
            Rg['DateCalc']=RegimeGroups[j]['DateCalc']
            Rg['pBottom_C']=RegimeGroups[j]['pBottom_C']
            
            # print('pBottom_C',Rg)
            # Rg = Rg[np.logical_not(np.isnan(Rg.pBottom_C))]
            Rg = Rg.dropna(axis=0, how='any')
            # print('pBottom_C',Rg['pBottom_C'])
            y_maxRg = np.max(Rg['pBottom_C'])
            if y_maxRg > y_max:
                y_max = y_maxRg
            
            mark= random.choice(markers)
            clr = random.choice(clrs)
            stl = random.choice(styls)
            plt.step(Rg['DateCalc'], Rg['pBottom_C'],  
                        where='mid',color=clr, linestyle=stl,
                             marker =mark, markersize=3, label=name)   

    x_min=x_min-300
    x_max=x_max+300

    try: 
        YF_ryad=np.array(FactData['pBottom_C'])
        XF_ryad=np.array(FactData['DateCalc'])

        y_maxF = 1.1*np.max(YF_ryad) 
        if y_max < y_maxF:
            y_max = y_maxF     
        
        plt.grid(True, linestyle='-', color='0.75')    
        plt.step(XF_ryad, YF_ryad,  color="g", 
                    marker ='o', where='mid',  label="Fact")
    except:
        y_max = y_max 
        x_min=x_min-300
        x_max=x_max+300
        
    plt.gca().set(xlim=(x_min, x_max), ylim=(0, y_max))
    plt.xlabel(lng_tuple['ls_date'], fontsize=8) 
    plt.ylabel(lng_tuple['ls_pBottom'], fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.title(lng_tuple['ls_pBottom_titul'], fontsize=8)
    plt.legend(fontsize=8) 
    
        
