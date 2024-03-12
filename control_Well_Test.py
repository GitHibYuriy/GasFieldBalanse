# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 06:59:30 2022

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

def Mbox( hwnd, text, caption, utype):
    return _MessageBoxW(hwnd, text, caption, utype)
   
def restart():
        import sys
        print("argv was",sys.argv)
        print("sys.executable was", sys.executable)
        print("restart now")

        import os
        os.execv(sys.executable, ['python'] + sys.argv)
        
def control_WellTestDatas(LogFilePath,lng_tuple):
   
    # Формальная проверка листа 'WellTestData'
    import fun_dimRowdrop as dr
    try:
        WellTestDataSheet='WellTestData'
        WellTestData = pd.read_excel(LogFilePath,WellTestDataSheet)
        
        flag=1
        while flag>0:
            flag=0
            
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
    except:
        
        #  txt =  LogFilePath+' '+lng_tuple['ls_does not contain WTD'].format('<WellTestData>') 
        
        #  caption = lng_tuple['ls_warning']
        #  Mbox(None, txt, caption , 0)
         flag=1
         
    return flag