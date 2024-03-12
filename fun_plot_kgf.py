# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 11:24:45 2022

@author: zarub
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
rootLogger = logging.getLogger(__name__)

"""Импорт собственных модулей"""
def plot_kgf(CGF,lng_tuple):

    XYF = pd.DataFrame(columns=['Pres','kgf'])
    i=0
    while not  pd.isna(CGF.loc[i,'Pres']):
        XYF.loc[i,'Pres']=CGF.loc[i,'Pres']
        XYF.loc[i,'kgf']=CGF.loc[i,'kgf']
        i=i+1
        if i > len(CGF)-1:
          break 
    
    XYC = pd.DataFrame(columns=['P_mid','KGF'])
    i=0
    while not  pd.isna(CGF.loc[i,'P_mid']):
        XYC.loc[i,'XC']=CGF.loc[i,'P_mid']
        XYC.loc[i,'YC']=CGF.loc[i,'KGF']
        i=i+1    
        if i > len(CGF)-1:
          break
   
    xyf = XYF.sort_values(by =['Pres'],ignore_index=True)
    XF_ryad = xyf['Pres']
    YF_ryad = xyf['kgf']
    
    y_min=np.min(YF_ryad)
    y_max=np.max(YF_ryad)    
    
    
    XYC['P_mid']=CGF['P_mid']
    XYC['KGF']=CGF['KGF']   
    xyc = XYC.sort_values(by =['P_mid'],ignore_index=True)
    XC_ryad =xyc['P_mid']
    YC_ryad =  xyc['KGF']
    
    x_min=np.min(XF_ryad)
    x_max=np.max(XF_ryad)
    
    if np.min(XC_ryad)<x_min:
        x_min= np.min(XC_ryad)
    if np.max(XC_ryad)>x_max:
        x_max= np.max(XC_ryad)  
    
    if x_min > 1:
        x_min = np.round(x_min-1,decimals=0)
    else:
        x_min = 0
        
    if np.min(YC_ryad)<y_min:
        y_min= np.min(YC_ryad)
    if np.max(YC_ryad)>y_max:
        y_max= np.max(YC_ryad)        
        
    y_min=y_min*0.7
    y_max=y_max*1.1   

   

   
   

    if pd.isna(CGF.loc[0,'Pres']):
        plt.gca().set(xlim=(x_min, x_max), ylim=(y_min, y_max), 
                  xlabel=lng_tuple['ls_pg_plt'], 
                  ylabel=lng_tuple['ls_kgf_plt'])
        plt.text(0.5, 0.5, lng_tuple['ls_ncnd_plt'], 
                fontsize=8, color='blue', alpha=0.5,
                ha='center', va='center', rotation='30')
        # rootLogger.warning(lng_tuple['ls_ncnd_plt'])
    else:

        plt.grid(True, linestyle='-', color='0.75')
        
        plt.scatter(XF_ryad, YF_ryad,  color="r", edgecolor = 'b', marker ='o',   label="Fact")
        plt.plot(XC_ryad,YC_ryad, label='Approximation interval', color='blue')
        
        plt.gca().set(xlim=(x_min, x_max), ylim=(y_min, y_max))
        plt.xlabel(lng_tuple['ls_pg_plt'], fontsize=8)
        plt.ylabel(lng_tuple['ls_kgf_plt'],fontsize=8)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.title(lng_tuple['ls_cgftit_plt'], fontsize=8)
        plt.legend(fontsize=8)
        
    
    "EXEMPLE"
# import  sqlite3 


# LogFilePath = "D:\Phyton_MBE_exe\Project_Shablons\Out_files\Shablon_Soha_206_bis_out-90.xlsx"
# # LogFilePath = "D:\Phyton_MBE_exe\Project_Shablons\Out_files\Shablon_Kobz_3_grwell_out-4.xlsx"

# lang = 'ru'    

# def get_lang_lng_tuple(lang):
#     result = {}
#     with sqlite3.connect('db/lang_schema.db') as db:
#         db.row_factory = sqlite3.Row
#         cursor = db.cursor()
#         query = """ SELECT ls_name, ls_{} FROM lang_scheme """.format(lang)
#         cursor.execute(query)
#         result = dict(cursor)
#     return result 
   
# def lang_check(lang):
#     global lng_tuple
#     lng_tuple = get_lang_lng_tuple(lang)  
#     return lng_tuple

# def ls_choice():
#     global lng_tuple
   
  
#     lang = 'en'
   
#     lng_tuple = lang_check(lang)
#     # lng_tuple = get_lang_lng_tuple(lang) 

   
#     return lang 

# lng_tuple = lang_check(lang)

# plot_kgf(LogFilePath,lng_tuple)    




   