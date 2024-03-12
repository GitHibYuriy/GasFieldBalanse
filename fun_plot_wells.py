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

def plot_wells(CD,values,lng_tuple):
    
    markers=('o', 'v', 's','d','^','H', '<', '>', '8',  'p', '*', 'h', 'H', 'D', 
                                      'P', 'X' )
    clrs = ('Blue','Red', 'Purple',  'Cyan', 'Magenta', 'Orange','Black')
    styls = ("solid","dotted","dashed","dashdot")
    
    CC, WellTestData, pzData, RegimeGroups, GroupList, CGF = CD
    CalcData = CC
    
    CalcData = dr.dimRowdrop(CalcData,'QgasSum' )
    
    
    
    FactData=pd.DataFrame()
    AllData=pd.DataFrame()
    for i in range(1, len(CalcData)) :
        
        if CalcData.loc[i,'QgasSum']>=0:
            FactData.loc[i,'DateCalc']=CalcData.loc[i,'DateCalc']
            FactData.loc[i,'Wells']=CalcData.loc[i,'Wells']
            AllData.loc[i,'DateCalc']=CalcData.loc[i,'DateCalc']
            AllData.loc[i,'Wells']=CalcData.loc[i,'Wells']
        else:
            AllData.loc[i,'DateCalc']=CalcData.loc[i,'DateCalc']
            AllData.loc[i,'Wells']=CalcData.loc[i,'Wells']
   
    x_min=np.min(AllData['DateCalc'])
    x_max=np.max(AllData['DateCalc']) 
    
    Xsum_ryad=np.array(AllData['DateCalc'],dtype='datetime64[D]')
    Ysum_ryad = np.array(AllData['Wells'])
    try:
        y_max = 1.1*np.max(FactData['Wells'])
    except:    
        y_max = 1.1*np.max(AllData['Wells'])
        
    # График фактического дебита
    try: 
        YF_ryad=np.array(FactData['Wells'])
        XF_ryad=np.array(FactData['DateCalc'])
        plt.grid(True, linestyle='-', color='0.75')    
        plt.step(XF_ryad, YF_ryad,  color="g", 
                    marker ='o', where='mid',  label="Fact")
    except:
        pass
    
    # График дебитов групп скважин
    nr = len(GroupList)
    if nr > 0: 
        for j in range (0,nr):
            
            name=GroupList[j] 
            Rg=pd.DataFrame()
            Rg['DateCalc']=RegimeGroups[j]['DateCalc']
            Rg['Wells']=RegimeGroups[j]['Wells']
            Rg = Rg.dropna(axis=0, how='any')            
            y_maxRg = np.max(Rg['Wells'])
            # x_max=np.max(Rg['DateCalc']) 
            if y_maxRg > y_max:
                y_max = y_maxRg
            mark= random.choice(markers)
            clr = random.choice(clrs)
            stl = random.choice(styls)
            plt.step(Rg['DateCalc'], Rg['Wells'],  
                        where='mid',color=clr, linestyle=stl,
                             marker =mark, markersize=3, label=name)
        
    plt.step(Xsum_ryad, Ysum_ryad, color="g", where='mid', label="Total") 
    
    plt.gca().set(xlim=(x_min, x_max), ylim=(0, y_max))
    plt.xlabel(lng_tuple['ls_date'], fontsize=8) 
    plt.ylabel(lng_tuple['ls_wells'], fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.title(lng_tuple['ls_wells_titul'], fontsize=8)
    plt.legend(fontsize=8) 
    

    
        
