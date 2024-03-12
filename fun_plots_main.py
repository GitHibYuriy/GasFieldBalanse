# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 08:22:20 2020

@author: zarub
"""


import tkinter as tk
from tkinter import ttk
from tkinter import *

import logging
rootLogger = logging.getLogger(__name__)

import datetime
import pylab
import matplotlib.pyplot as plt

import fun_plot_kgf as pt0
import fun_plot_pt as pt1
import fun_plot_pzQ as pt2
import fun_plot_qt as pt3



def plots_main(LogFilePath,CD,values,lng_tuple):
    now = datetime.datetime.now()
    time = now.strftime("%d-%m-%Y %H:%M")
    
    CC, WellTestData, pzData, RegimeGroups, GroupList, CGF = CD       
        
    fig, axs = plt.subplots(2,2,figsize=(8,6), dpi=100)
    
    try:                   
        pylab.subplot (2, 2, 1)
        pt1.plot_PT(WellTestData,CC,lng_tuple)
    except:
        pylab.subplot (2, 2, 1)
        pylab.text(0.5, 0.5, lng_tuple['ls_plot_mistake'], 
            fontsize=8, color='blue', alpha=0.5,
            ha='center', va='center', rotation='30')
        rootLogger.warning(lng_tuple['ls_plot_mistake'])
    
    try:
        pylab.subplot (2, 2, 3)
        pt2.plot_pzQ(CC, WellTestData, lng_tuple)
    except:
        pylab.subplot (2, 2, 3)
        pylab.text(0.5, 0.5, lng_tuple['ls_plot_mistake'], 
            fontsize=8, color='blue', alpha=0.5,
            ha='center', va='center', rotation='30')
        rootLogger.warning(lng_tuple['ls_plot_mistake'])
        
    pylab.subplot (2, 2, 2)
    pt3.plot_qt(CD,values,lng_tuple)    
        
    # try: 
    #     pylab.subplot (2, 2, 2)
    #     pt3.plot_qt(CD,values,lng_tuple)
    # except:
    #     pylab.subplot (2, 2, 2)
    #     pylab.text(0.5, 0.5, lng_tuple['ls_plot_mistake'], 
    #         fontsize=8, color='blue', alpha=0.5,
    #         ha='center', va='center', rotation='30')
    #     rootLogger.warning(lng_tuple['ls_plot_mistake'])
        
    try:
        pylab.subplot (2, 2, 4)
        pt0.plot_kgf(CGF,lng_tuple)
    except:
        pylab.subplot (2, 2, 4)
        # pylab.title("Нет данных для прогнозирования добычи конденсата", fontsize=8)
        pylab.text(0.5, 0.5, lng_tuple['ls_ncnd_plt'], 
            fontsize=8, color='blue', alpha=0.5,
            ha='center', va='center', rotation='30')
        # rootLogger.warning(lng_tuple['ls_ncnd_plt'])
            
    rootLogger.info("")  
       
    info=str( "{:.3f}".format(values.loc[2]))
    info = (" reserv_ini = "+ info +" mln.м3" )
    info1=str( "{:.2f}".format(values.loc[3]))
    info = str(info +" p_ini =" + info1 +" MPa")
    info1=str( "{:.3f}".format(values.loc[7]))
    info =  (info +" W-Poten ="+ info1 +" mln.м3")
    info1=str( "{:.4e}".format(values.loc[8]))
    info = (info +" W_Index="+ info1 +" mln.м3/MPa/day") 
    fig.suptitle(t=(lng_tuple['ls_log_file']+LogFilePath+" "+time+" \n " + info+"  ."),fontsize=8)
    
    plt.tight_layout()
    return fig

