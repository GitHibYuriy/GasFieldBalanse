# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 08:22:20 2020

@author: zarub
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import fun_dimRowdrop as dr

def plot_qt(CD,values,lng_tuple):
    markers=('o', 'v', 's','d','^','H', '<', '>', '8',  'p', '*', 'h', 'H', 'D', 
                                      'P', 'X' )
    clrs = ('Blue','Red', 'Purple',  'Cyan', 'Magenta', 'Orange','Black')
    styls = ("solid","dotted","dashed","dashdot")

    # Выбор данных
    CC, WellTestData, pzData, RegimeGroups, GroupList, CGF = CD
    CalcData = CC
    CalcData = dr.dimRowdrop(CalcData,'QgasSum' )
    FactData=pd.DataFrame()
    AllData=pd.DataFrame()
    for i in range(1, len(CalcData)) :
        if CalcData.loc[i,'QgasSum']>0:
            FactData.loc[i,'DateCalc']=CalcData.loc[i,'DateCalc']
            FactData.loc[i,'qGas_C']=CalcData.loc[i,'qGas_C']
            AllData.loc[i,'DateCalc']=CalcData.loc[i,'DateCalc']
            AllData.loc[i,'qGas_C']=CalcData.loc[i,'qGas_C']
        else:
            AllData.loc[i,'DateCalc']=CalcData.loc[i,'DateCalc']
            AllData.loc[i,'qGas_C']=CalcData.loc[i,'qGas_C']
    FactData = FactData.dropna(axis=0, how='any')
    AllData = AllData.dropna(axis=0, how='any')

    x_min=np.min(AllData['DateCalc'])
    x_max=np.max(AllData['DateCalc']) 

    try: 
        y_max = 1.1*np.max(FactData['qGas_C'])
    except:
        y_max = 1.1*np.max(AllData['qGas_C'])
    try: 
        y_min = 1.1*np.min(FactData['qGas_C'])
    except:
        y_min = 1.1*np.min(AllData['qGas_C'])    
        
    
    # График фактического дебита
    try: 
        
        YF_ryad=np.array(FactData['qGas_C'])
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
            Rg['qGas_C']=RegimeGroups[j]['qGas_C']
            Rg = Rg.dropna(axis=0, how='any')
            y_maxRg = 1.1*np.max(Rg['qGas_C'])
            
            # x_max=np.max(Rg['DateCalc']) 
            if y_maxRg > y_max:
                y_max = y_maxRg
            y_minRg = 1.1*np.min(Rg['qGas_C']) 
            if y_minRg < y_min:
                y_min = y_minRg
                
            mark= random.choice(markers)
            clr = random.choice(clrs)
            stl = random.choice(styls)
            plt.step(Rg['DateCalc'], Rg['qGas_C'],  
                        where='mid',color=clr, linestyle=stl,
                             marker =mark, markersize=3, label=name)

    # График суммарного прогнозного дебита
    Xsum_ryad=np.array(AllData['DateCalc'],dtype='datetime64[D]')
    Ysum_ryad = np.array(AllData['qGas_C'])                         

    plt.step(Xsum_ryad, Ysum_ryad, color="g", where='mid', label="Total") 
 
    plt.gca().set(xlim=(x_min, x_max), ylim=(y_min, y_max))
    plt.xlabel(lng_tuple['ls_date'], fontsize=8) 
    plt.ylabel(lng_tuple['ls_q_plt'], fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.title(lng_tuple['ls_dq_plt'], fontsize=8)
    plt.legend(fontsize=8) 



