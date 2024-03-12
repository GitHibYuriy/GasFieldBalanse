# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 12:33:23 2022

@author: zarub
"""
import pandas as pd
import ctypes
from ctypes.wintypes import HWND, LPWSTR, UINT  
import datetime
_user32 = ctypes.WinDLL('user32', use_last_error=True)

_MessageBoxW = _user32.MessageBoxW
_MessageBoxW.restype = UINT  # default return type is c_int, this is not required
_MessageBoxW.argtypes = (HWND, LPWSTR, LPWSTR, UINT)

MB_OK = 0
MB_OKCANCEL = 1
MB_YESNOCANCEL = 3
MB_YESNO = 4

IDOK = 1
IDCANCEL = 2
IDABORT = 3
IDYES = 6
IDNO = 7

# Формальная проверка содержания листов 'Globals' и  'Calculated'

def restart():
        import sys
        print("argv was",sys.argv)
        print("sys.executable was", sys.executable)
        print("restart now")

        import os
        os.execv(sys.executable, ['python'] + sys.argv)

def Mbox( hwnd, text, caption, utype):
    return _MessageBoxW(hwnd, text, caption, utype)
    # return  easygui.msgbox( text,  title)

def control_globals(LogFilePath,values,lng_tuple):
   
    # Формальная проверка листа 'Globals'
    
    flag=1
    while flag>0:
       

        i = 0
        if pd.isna(values.loc[i]) or values.loc[i]<= 0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_Depth'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=3000
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 
             
        i = 1      
        if pd.isna(values.loc[i]) or values.loc[i]<= 213:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_Tpplast'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=values.loc[0]*0.03+273
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 
        i = 2
        if pd.isna(values.loc[2]) or values.loc[2]<= 0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_reserv_ini'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=values.loc[0]*100
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 
        i = 3
        if pd.isna(values.loc[3]) or values.loc[3]<= 0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_p_ini'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=values.loc[0]/100
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 
        i = 4
        if pd.isna(values.loc[4]) or values.loc[4] < 0 or values.loc[4] > values.loc[2]:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_Q_ini'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[4]=0
                values.loc[5]=values.loc[2]
            else:
                flag=1
                
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[4]=GlobalData['values'].loc[4]
                continue
        else:
            flag = 0 

               
        i = 6
        if pd.isna(values.loc[6]) or values.loc[6]< 0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_Water'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 7   
        if pd.isna(values.loc[7]) or values.loc[7] <0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_Water_Poten'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=values.loc[2]/values.loc[3]/10
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 8
        if pd.isna(values.loc[8]) or values.loc[8] <0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_Water_Index'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 9
        if pd.isna(values.loc[9]) or values.loc[9] <0.56:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_ro'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0.56
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 10
        if pd.isna(values.loc[10]) or values.loc[9] <0:
            flag=1
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_H2S'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 11
        if pd.isna(values.loc[11]) or values.loc[11] <0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_CO2'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 12
        if pd.isna(values.loc[i]) or values.loc[i] <0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_N2'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 16
        if pd.isna(values.loc[16]) or values.loc[16] <213:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_T_Head'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=288
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 17
        if pd.isna(values.loc[17]) or values.loc[17] <=0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_d'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=7.3
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 18
        if pd.isna(values.loc[18]) or values.loc[18] <0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_Lmbd'] + ' In Globals values row '+ str(i+2) 
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0.0025
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 
        i = 19    
        if pd.isna(values.loc[19]) or values.loc[19] <=0 or values.loc[19]>1 :
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_K_expl'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=1
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 20
        if pd.isna(values.loc[20]) or values.loc[20] <0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_porisity'] + ' In Globals values row '+ str(i+2) 
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0.18
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 21    
        if pd.isna(values.loc[21]) or values.loc[21] <0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_sat_water'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0.30
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 22
        if pd.isna(values.loc[22]) or values.loc[22] <0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_bet_rock'] + ' In Globals values row '+ str(i+2) 
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0.0004
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 


        i = 23
        if pd.isna(values.loc[23]) or values.loc[23] <0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_bet_water'] + ' In Globals values row '+ str(i+2) 
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0.0006
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 
        values.loc[24] = values.loc[22]+values.loc[20]*values.loc[21]*values.loc[23]
            
        i = 25
        if pd.isna(values.loc[i]) or values.loc[i] <0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_pst'] + ' In Globals values row '+ str(i+2) 
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0.101325
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 26
        if pd.isna(values.loc[i]) or values.loc[i] <0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_Tst'] + ' In Globals values row '+ str(i+2) 
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=293.15
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 
            
        i = 27    
        if pd.isna(values.loc[27]) or values.loc[27] <0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_Influx'] + ' In Globals values row '+ str(i+2)
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0

        i = 28
        if pd.isna(values.loc[28]) or values.loc[28] <0:
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_Condensat'] + ' In Globals values row '+ str(i+2) 
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:                   
                values.loc[i]=0
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 

        i = 29
        data_start_V = values.loc[i]
        CalcData = pd.read_excel(LogFilePath,'Calculated')
        cdate = CalcData['DateCalc']
        data_start_C = CalcData.loc[1,'DateCalc'] 
         
        
        if pd.isna(data_start_V) or not isinstance(data_start_V,datetime.date) or  data_start_V > data_start_C :
            txt = LogFilePath+'n\ DataFile list <Gloobals> Incorrect - ' + lng_tuple['ls_BeginDate'] + ' In Globals values row '+ str(i+2) 
            caption = lng_tuple['ls_warning']
            rez =  Mbox(None, txt, caption , MB_OKCANCEL)
            if rez == IDCANCEL:
                values.loc[i]=data_start_C 
            else:
                flag=1
                GlobalData = pd.read_excel(LogFilePath,'Globals')
                values.loc[i]=GlobalData['values'].loc[i]
                continue
        else:
            flag = 0 
            
        # Формальна проверка date листа Calculated
            
        
            
        for i in range(2, len(cdate)):
            if (cdate[i]<=cdate[i-1]):
                txt =  LogFilePath+'n\ DataFile list <Calculated> Incorrect - '+ lng_tuple['ls_date'] + ' Cell A'+ str(i+2) 
                caption = lng_tuple['ls_warning']
                rez =  Mbox(None, txt, caption , MB_OK)
            #     if rez == IDCANCEL:
            #         values.loc[i]=cdate[i-1]+ datetime.timedelta(days=1)
            #     else:
            #         flag=1
            #         CalcData = pd.read_excel(LogFilePath,'Calculated')
            #         cdate[i] = CalcData.loc[i,'DateCalc']
            #         continue
            # else:
            #     flag = 0 
        
        
        
        return values
                
def control_WellTestDatas(LogFilePath,lng_tuple):
   
    # Формальная проверка листа 'WellTestData'
    import fun_dimRowdrop as dr
    
    
    
    flag=1
    while flag>0:
        # flag=0
        WellTestDataSheet='WellTestData'
        WellTestData = pd.read_excel(LogFilePath,WellTestDataSheet)
        ppl = WellTestData['ppl']
        date = WellTestData['dateTest']
        # print(WellTestData)
        
        for i in range(1, len(ppl)):
            # print('ppl[i]', i, ppl[i] )
            if pd.isna(ppl[i]) or ppl[i]<= 0:
                  txt = LogFilePath+' '+lng_tuple['ls_error WTD'] + ' - ppl' + '\n' +lng_tuple['ls_in row']+' '+ str(i+2)+'.\n'
                  txt = txt +  lng_tuple['ls_Fix_Save'] 
                  caption = lng_tuple['ls_warning']
                  rez =  Mbox(None, txt, caption , MB_OKCANCEL)
                  if rez == IDCANCEL:                   
                      restart()
                  else: 
                      flag=1
            if pd.isna(date[i]) or not isinstance(date[i], datetime.date):
                  txt = LogFilePath+' '+lng_tuple['ls_error WTD'] +  ' - dateTest' + '\n'+lng_tuple['ls_in row']+' '+ str(i+1)+'.\n'
                  txt = txt +  lng_tuple['ls_Fix_Save'] 
                  caption = lng_tuple['ls_warning']
                  rez =  Mbox(None, txt, caption , MB_OKCANCEL)
                  if rez == IDCANCEL:                   
                      restart()
                  else: 
                      flag=1
    
        
