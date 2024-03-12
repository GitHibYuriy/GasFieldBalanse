# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 08:47:45 2022

@author: zarub
"""


import pandas as pd
import time
import ctypes
from ctypes.wintypes import HWND, LPWSTR, UINT

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


def MessageBoxW(hwnd, text, caption, utype):
    result = _MessageBoxW(hwnd, text, caption, utype)
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    return result


def ask_mbox_save(lng_tuple):
    caption = lng_tuple['ls_answer']
    text = lng_tuple['ls_asked']
    try:
        result = MessageBoxW(None, text, caption, MB_YESNO)
      
        if result == IDYES:
            print("user pressed ok")
            answer = 1
        elif result == IDNO:
            print("user pressed no")
            answer = 0
        # elif result == IDCANCEL:
        #     print("user pressed cancel")
        #     answer = 0
        
        else:
            print("unknown return code")
            answer = 1
        # MessageBoxW.wait_variable(result)
    except:
        
        answer = 1
    return answer

def ask_mbox_interrupt(lng_tuple):
    caption = lng_tuple['ls_answer']
    text = lng_tuple['ls_asked_interrupt']
    result = MessageBoxW(None, text, caption, MB_YESNO)
    
    try:
        result = MessageBoxW(None, text, caption, MB_YESNO)
        if result == IDYES:
            print("ls_iter_interrupt")
            answer = 1
        elif result == IDNO:
            print("user pressed no")
            answer = 0
        elif result == IDCANCEL:
            print("user pressed cancel")
            answer = 0
        else:
            print("unknown return code")
        # MessageBoxW.wait_variable(result)
    except WindowsError as win_err:
        print("An error occurred:\n{}".format(win_err))
        answer = 0
    return answer


def save_new(LogFilePath,GlobalData,lng_tuple):
    answer = ask_mbox_save(lng_tuple)
    if answer==1:
        writer = pd.ExcelWriter( LogFilePath, engine='xlsxwriter')        
        GlobalData.to_excel(writer,'Globals')

    