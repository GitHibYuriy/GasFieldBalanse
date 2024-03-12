# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 11:10:04 2022

@author: zarub
"""
import pandas as pd
import numpy as np


def dimen_row(List_xls):
    colms = List_xls.columns
    # Dimd = pd.DataFrame([],columns = colms)
    Dimd = pd.DataFrame([],dtype=pd.StringDtype(),columns = colms)
    cols = tuple(colms)
    # Dimd = Dimd.append({}, ignore_index=True)
    # for j in range(Dimd.shape[1]):
    dd = pd.DataFrame([],dtype=pd.StringDtype(),columns = colms)    
    Dimd = pd.concat([Dimd,dd], ignore_index=True)
    for j in range(0,len(cols)):
        ident = cols[j] 
        try:
            idin = ['SumQ_inputed', 'Q model', 'Q_all', 'QgasSum', 'QwaterSum',
                    'QgasDif_C','QgasSum_C', 'Reserver_C','Influx_C',
                    'pore_Volume_C', 'Intepolated','old_X1','is_M1',
                    'is_M1','next_X1','Sig_X1', 'old_X3','is_M3','next_X3','Sig_X3']
            for i in range(0,len(idin)):                
                id=idin[i]                
                if ident == id:
                    Dimd.at[0,ident]="mln.cub.m"                
        except:
            pass

        try:        
            if ident == 'DateCalc':
                    Dimd.at[0,'DateCalc']="date"                   
        except:
            pass

        try:        
            if ident == 'dateTest':
                    Dimd.at[0,'dateTest']="date"                   
        except:
            pass

        try:
            idin = ['QcondSum', 'QcondDif', 'QcondSum_C', 'QcondDif_C', 'QcondDif_C']
            for i in range(0,len(idin)):                
                id=idin[i]    
                if ident == id :
                    Dimd.at[0,ident]="thnd.tonn"
        except:
            pass 
        
        try:
            idin = ['kgf', 'KGF', 'c']
            for i in range(0,len(idin)):                
                id=idin[i]    
                if ident == id :
                    Dimd.at[0,ident]="g/cub.m"
        except:
            pass 
            
        try: 
            if ident ==  'a':
                Dimd.at[0,'a']="(g/cub.m)/MPa^2"
        except:
            pass 
            
        try: 
            if ident ==  'b':
                Dimd.at[0,'b']="(g/cub.m)/MPa"
        except:
            pass   
            
        
        try: 
            if ident ==  'Wells':
                Dimd.at[0,'Wells']="pcs"
        except:
            pass

        try: 
            if ident =='Days':
                Dimd.at[0,'Days']="day" 
        except:
            pass
        try: 
            if ident =='Regim':
                Dimd.at[0,'Regim']="regime name"
        except:
            pass

        try: 
            idin = ['pHead' , 'dpRob' , 'pBottom' , 'pPl_C', 'p-z_C' , 
                    'pHead_C', 'dpRob_C', 'pBottom_C', 'ppl','P_prognz',
                    'p/z','ppl/z', 'p/z fact','P_mid','p/z model','Pres',
                    'is err1','min err1','old_X2','is_M2','Next_X2', 'Sig_X2',
                    'is err2','min err2','is err3','min err3',
                    'is err4','min err4','err_min']
            for i in range(0,len(idin)):                
                id=idin[i]
                if ident ==id:
                    Dimd.at[0,ident]="MPa"
        except:
            pass

        try:            
            if ident == 'pB_pPl_fraction':
                Dimd.at[0,ident]="fraction"
        except:
            pass   
          
        try: 
            if  ident =='qGas_C':
                Dimd.at[0,'qGas_C']="thnd cub.m/day"
           
        except:
            pass
       
        try: 
            if ident =='A':
                Dimd.at[0,'A']="MPa^2/(thnd cub.m/day)"
        except:
            pass

        try: 
            if ident =='B':
                Dimd.at[0,'B']="MPa^2/(thnd cub.m/day)^2" 
        except:
            pass 
        try: 
            if ident =='Method':
                Dimd.at[0,'Method']="2-nd name" 
        except:
            pass 

        try: 
            if ident =='Weight':
                Dimd.at[0,'Weight']="coefficient" 
        except:
            pass
         
        try:            
            if ident == 'RyadName' or ident =='Wellname':
                Dimd.at[0,ident]="name"
        except:
            pass

        try:            
            idin = ['old_X4','is_M4','next_M4',	'Sig_X4']
            for i in range(0,len(idin)):                
                id=idin[i]
                if ident ==id:
                    Dimd.at[0,ident]="mln.m.cub/(MPa*day)"    
        except:
            pass


    return Dimd
    
    
