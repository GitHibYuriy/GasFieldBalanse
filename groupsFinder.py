# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 06:56:42 2022

@author: zarub
"""

import pandas as pd
import control_globals as glc

def group_find(LogFilePath, lng_tuple ):
    
    xlData = pd.ExcelFile(LogFilePath)
    sheetsName = xlData.sheet_names
    
    RegimeGroups=[]
    iniName = []
    group_namelist=[]
    m=len(sheetsName)
    nn=0
    for n in range(0,m):
        fn = sheetsName[n]
        
        if fn.count('Group' ):            
            iniName.append(fn)            
            new='gr_'+str(nn)            
            RegimeGroups.append(new)           
            name=fn
            group_namelist.append(name)
            nn=nn+1
        if fn.count('iWell'):
            iniName.append(fn)            
            new='gr_'+str(nn)            
            RegimeGroups.append(new)            
            name=fn
            group_namelist.append(name)
            nn=nn+1

    # print(group_namelist)
    
    
    return iniName, RegimeGroups, group_namelist
    
    
    
    
    
    
# LogFilePath ="D:\Phyton_MBE_exe\Project_Shablons\Shablon_Kobz_3_grwell-stts.xlsm"
# app =group_find(LogFilePath, lng_tuple )