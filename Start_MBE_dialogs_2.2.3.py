# -*- coding: utf-8 -*-
"""
Created on framei Mar  4 15:20:45 2022

@author: zarub
"""



import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import Button, Label, Frame, Entry, Checkbutton,  Text
from tkinter import Toplevel
from tkinter import messagebox as mb
import locale
import sqlite3 
import numpy as np
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import  NavigationToolbar2Tk

import logging
from logging import Handler, getLogger
logger = logging.getLogger(__name__)

# Импорт собственных модулей
import fileopen_box as fo
import control_globals as glc
import control_Well_Test as gwt
import styles_to_excel as stl

import fun_dimRowdrop as dr
import dimensions  as dm
import Simpl_prgnz as sprg
import minimizator as mnm
import file_out_name as fln
import groupsFinder  as gf

import fun_plots_main as plm
import fun_plots_main_well as plw

W = tk.W
E = tk.E
END = tk.END
DISABLED = tk.DISABLED
NORMAL = tk.NORMAL

def make_textmenu(root): # """ Всплывающее меню """
	global the_menu
	the_menu = tk.Menu(root, tearoff=0)
	the_menu.add_command(label="Cut")
	the_menu.add_command(label="Copy")
	the_menu.add_command(label="Paste")
	the_menu.add_separator()
	the_menu.add_command(label="Select all")

def callback_select_all(event):
	# select text after 50ms
	root.after(50, lambda:event.widget.select_range(0, 'end'))

def show_textmenu(event): # """ Всплывающее меню for Entry"""
	e_widget = event.widget
	the_menu.entryconfigure("Cut",command=lambda: e_widget.event_generate("<<Cut>>"))
	the_menu.entryconfigure("Copy",command=lambda: e_widget.event_generate("<<Copy>>"))
	the_menu.entryconfigure("Paste",command=lambda: e_widget.event_generate("<<Paste>>"))
	the_menu.entryconfigure("Select all",command=lambda: e_widget.select_range(0, 'end'))
	the_menu.tk.call("tk_popup", the_menu, event.x_root, event.y_root)

def show_textmenu_Consol(event): # """ Всплывающее меню for Text"""
	
	e_widget = event.widget
	the_menu.entryconfigure("Cut",command=lambda: e_widget.event_generate("<<Cut>>"))
	the_menu.entryconfigure("Copy",command=lambda: e_widget.event_generate("<<Copy>>"))
	the_menu.entryconfigure("Paste",command=lambda: e_widget.event_generate("<<Paste>>"))
	the_menu.entryconfigure("Select all",command=lambda: e_widget.tag_add("sel","1.0","end"))
	the_menu.tk.call("tk_popup", the_menu, event.x_root, event.y_root)

class ScrolledText(Text):
    def __init__(self, master=None, **kw):
        self.frame = Frame(master)
        self.vbar = tk.Scrollbar(self.frame)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)

        kw.update({'yscrollcommand': self.vbar.set})
        Text.__init__(self, self.frame, **kw)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vbar['command'] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(Text).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frameame)
    
class ListboxHandler(Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted frameom Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.insert(END, msg + '\n')
            # Editable
            self.text.configure(state='normal')
            # Autoscroll to the bottom
            self.text.yview(END)
        # This is necessary because we can't modify the Text frameom other threads
        self.text.after(0, append) 

 
            
        
def get_values (LogFilePath):

    GlblData = pd.read_excel(LogFilePath,'Globals')
    values=GlblData['values']

        
    if values.loc[2]<=0:
        values.loc[2] =  0.1
    if values.loc[3]<=0:
        values.loc[3] =  0.101325
    if values.loc[7]<=0:
        values.loc[7] =  0.1
    values.loc[32] = 1
    values.loc[33] = 1.2
    for i in range(0,4): 
        values.loc[34+i] =1
    return values

def get_Rezult(LogFilePath):
    LogFilePath = log_entry.get()
    
    """
    Основной рассчетный блок после считывания исходных данных
    и формирования  диалогового окна    
    """
    # "Get values frameom data file"
    values =  get_values(LogFilePath) 
    
    # "Get changed values  entry"
    while True:
        try:
            values.loc[2]=np.float64(Resv_entry.get())
            break
        except ValueError:
            # Resv_entry.delete(0,END)
            print(lng_tuple['ls_no_res'])
            rootLogger.info(lng_tuple['ls_no_res'])
            Start_Calc_BT(LogFilePath)
            
    while True:
        try:
            values.loc[3]=np.float64(p_entry.get())
            break
        except ValueError:
            # p_entry.delete(0,END)
            print(lng_tuple['ls_no_pres'])
            rootLogger.info(lng_tuple['ls_no_pres'])
            Start_Calc_BT(LogFilePath)
    while True:
        try:
            values.loc[7]=np.float64(Wpot_entry.get())
            break
        except ValueError:
            # Wpot_entry.delete(0,END)
            print(lng_tuple['ls_no_poten'])
            rootLogger.info(lng_tuple['ls_no_poten'])
            Start_Calc_BT(LogFilePath)
    while True:
        try:
            values.loc[8]=np.float64(Wind_entry.get())
            break
        except ValueError:
            # Wind_entry.delete(0,END)
            print(lng_tuple['ls_no_ind'])
            rootLogger.info(lng_tuple['ls_no_ind'])
            Start_Calc_BT(LogFilePath)
    while True:
        try:
            values.loc[32]=int(Iter_entry.get())
            break
        except ValueError:
            # Iter_entry.delete(0,END)
            print(lng_tuple['ls_no_iter'])
            rootLogger.info(lng_tuple['ls_no_iter'])
            Start_Calc_BT(LogFilePath)
    while True:
        try:
            values.loc[33]=np.float64(Relax_entry.get())
            break
        except ValueError:
            # Relax_entry.delete(0,END)
            print(lng_tuple['ls_no_relax'])
            rootLogger.info(lng_tuple['ls_no_relax'])            
            Start_Calc_BT(LogFilePath)
    
    values.loc[5]= values.loc[2] - values.loc[4] 
    values.loc[34]=np.float64(cbRes.get()) 
    values.loc[35]=np.float64(cbPres.get()) 
    values.loc[36]=np.float64(cbWpot.get()) 
    values.loc[37]=np.float64(cbWind.get()) 
    rootLogger.warning("********* " +lng_tuple['ls_Start New Modeling'] +  " ********")
    rootLogger.warning(lng_tuple['ls_log_file']+'  ' + LogFilePath)
    rootLogger.warning(lng_tuple['ls_reserv_ini']+'  '+ str(values.loc[2]) + lng_tuple['ls_vol'])
    rootLogger.warning(lng_tuple['ls_p_ini']  +str(values.loc[3])+ " MPa")
    rootLogger.warning(lng_tuple['ls_Water_Poten']+'  '+str(values.loc[7])+" mln.m.cub. ")       
    rootLogger.warning(lng_tuple['ls_Water_Index']+'  '+str(values.loc[8])+ " mln.m.cub./MPa/day")
    
    fact = pd.read_excel(LogFilePath,"Calculated")
    
    # Удаление строки размерностей
    fact = dr.dimRowdrop(fact,'QgasSum' )

    # Проверка наличия и содержания листа WellTestData
    flag = gwt.control_WellTestDatas(LogFilePath,lng_tuple)
    
    if flag != 0:
        txt =  LogFilePath+' '+lng_tuple['ls_does not contain WTD'].format('<WellTestData>')
        caption = lng_tuple['ls_warning']
        gwt.Mbox(None, txt, caption , 0)
        
    # Контроль  имен и данных для групп скважин
    iniName = gf.group_find(LogFilePath, lng_tuple )[0]
    nr = len(iniName)
    values.loc[30] = nr
    if nr==0:
        txt =  LogFilePath+' '+lng_tuple['ls_no_forecast'].format(' any <Group')+'.\n '  
        caption = lng_tuple['ls_warning']
        glc.Mbox(None, txt, caption , 0)
    
    flagQ = pd.isna(fact.loc[0,'QgasSum'])
    "Предварительный контроль листа  Globals"
    values = glc.control_globals(LogFilePath, values, lng_tuple) 

    if flagQ==False and flag==0:
        # 'Если период фактических данных существует'
        rootLogger.warning(lng_tuple['ls_adp'])
        GlobalData,CC,WellTestData, pzData,CGF,ERR,GroupList,RegimeGroups,ERR = mnm.minimizator(LogFilePath,values, root,lng_tuple)
       
      
    else:
        # 'Если период фактических данных отсутствует или отсутствует лист WellTestData'
        rootLogger.warning(lng_tuple['ls_adp'])
        
        GlobalData,CC,WellTestData, pzData,CGF,ERR,GroupList,RegimeGroups = sprg.simpl_prgnz(LogFilePath,values, lng_tuple)
    
    
    # entris.entris_delete(0,END)
    
    log_entry.delete(0,END)
    Resv_entry.delete(0,END)
    p_entry.delete(0,END)
    Wpot_entry.delete(0,END)
    Wind_entry.delete(0,END)
    
    Resv_entry.insert(0,"{:.3f}".format(values.loc[2]) )
    p_entry.insert(0,"{:.2f}".format(values.loc[3]))    
    Wpot_entry.insert(0,"{:.3f}".format(values.loc[7]))
    Wind_entry.insert(0,"{:.4e}".format(values.loc[8]))
   
    CDd = CC, WellTestData, pzData, RegimeGroups, GroupList, CGF
    
    fig = plm.plots_main(LogFilePath, CDd,values, lng_tuple)
    figw = plw.plots_main_well(LogFilePath, CDd, values, lng_tuple)
    
    top1.deiconify()
    canvas = FigureCanvasTkAgg(figw, master = top1)         
    canvas.draw()  
    canvas.get_tk_widget().place(x=0, y=5)
    frame = tk.Frame(top1)
    frame.place(x=0, y=590)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.config(background='white')
    
    top.deiconify()
    canvas = FigureCanvasTkAgg(fig, master = top)         
    canvas.draw()  
    canvas.get_tk_widget().place(x=0, y=5)
    frame = Frame(top)
    frame.place(x=0, y=590)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.config(background='white')
    root.update()
    
    # Запрос на сохраненние нового файла данных 
    try:
        # answer=ans.ask_mbox_save(lng_tuple)
        answer = mb.askyesno(
        title=lng_tuple['ls_answer'], 
        message=lng_tuple['ls_asked'])
      
    except:
        answer==1    
    
    if answer==1:
        
        # Вставка строки размерностей в результирующие фреймы
        try:            
            WellTestData = pd.concat([dm.dimen_row(WellTestData),WellTestData], axis=0)            
            CC = pd.concat([dm.dimen_row(CC),CC], axis=0)            
            CGF = pd.concat([dm.dimen_row(CGF),CGF], axis=0)
            pzData = pd.concat([dm.dimen_row(pzData),pzData], axis=0)
            ERR = pd.concat([dm.dimen_row(ERR),ERR], axis=0)
        except:
            CC = pd.concat([dm.dimen_row(CC),CC], axis=0)
            CGF = pd.concat([dm.dimen_row(CGF),CGF], axis=0)
            
        outFile = fln.out_file(LogFilePath)    
        print("The unique file name with results created ", outFile)
        
        # Передача  результирующих фреймов в excel
        writer = pd.ExcelWriter( outFile, engine='xlsxwriter' , date_format = 'dd-mm-yyyy', datetime_format = 'dd-mm-yyyy')
        try:
            GlobalData.to_excel(writer,'Globals',index=False)
            
            CC.to_excel(writer,'Calculated',float_format="%.3f",index=False)
            WellTestData.to_excel(writer,'WellTestData',float_format="%.2f",index=False)
            pzData.to_excel(writer,'pz_Data',float_format="%.2f",index=False)
            CGF.to_excel(writer,'CondFactor',float_format="%.2f",index=False)
        except:
            GlobalData.to_excel(writer,'Globals',index=False)
            CC.to_excel(writer,'Calculated',float_format="%.2f",index=False)
            CGF.to_excel(writer,'CondFactor',float_format="%.2f",index=False)
        i=0    
        while i<len(GroupList):
            RegimeGroups[i] = pd.concat([dm.dimen_row(RegimeGroups[i]),RegimeGroups[i]], axis=0)
            RegimeGroups[i].to_excel(writer,GroupList[i],float_format="%.2f",index=False)            
            i=i+1
        try:    
            ERR.to_excel(writer,'Shots',index=False)
        except:
            pass
            
        writer.save()
        
        path = outFile
        path = stl.excel_style(path,root)
    
        rootLogger.warning(lng_tuple['saved in the file'] +"  " + outFile)
        rootLogger.info("")
        
    StartCalc_BT.configure(bg ='limegreen', fg= 'black')  
    
    
    
    return values
        

def entry_insert(LogFilePath,values):
    delete_all()    
    
    log_entry.insert(0,LogFilePath)
    Resv_entry.insert(0,"{:.3f}".format(values.loc[2]) )
    p_entry.insert(0,"{:.2f}".format(values.loc[3]))    
    Wpot_entry.insert(0,"{:.3f}".format(values.loc[7]))
    Wind_entry.insert(0,"{:.4e}".format(values.loc[8]))
    Iter_entry.insert(0, int(values.loc[32]))
    Relax_entry.insert(0,"{:.2f}".format(values.loc[33]))
    
def isChecked():
    global btnRes, btnPres, btnWpot,  btnWind 
    
    textRes=lng_tuple['ls_opt']
    textPres=lng_tuple['ls_n_opt']
    textWpot=lng_tuple['ls_opt']
    textWind=lng_tuple['ls_opt']
    
    frame = Frame(root, padx = 1, pady =1)
    frame.grid(row=9, column=4, rowspan = 4)

    argsCb ={'text':"", 'onvalue':1, 'offvalue':0, 'command':isChecked} 
    argsB = {'relief':"flat", 'font':("Arial Bold", 10), "width":18}
    # relief="flat"
    # font=("Arial Bold", 10)
    # width=18


    argsE = {'column':0, 'sticky':(E), 'pady' : 1, 'padx' :1}  
    argsW = {'column':1, 'sticky':(W), 'pady' : 1, 'padx' :1}      

    chb1 = Checkbutton(frame,  variable=cbRes, **argsCb).grid(row=0, **argsE)
    chb2 = Checkbutton(frame,  variable=cbPres, **argsCb).grid(row=1, **argsE)
    chb3 = Checkbutton(frame,  variable=cbWpot, **argsCb).grid(row=2, **argsE)
    chb4 = Checkbutton(frame,  variable=cbWind, **argsCb).grid(row=3, **argsE)
    
    btnRes = Button(frame, text=textRes, state=DISABLED, relief="flat", font=("Arial Bold", 10), width=18)
    btnRes.grid(row=0, **argsW)
    
    btnPres = Button(frame, text=textPres, state=DISABLED, relief="flat",font=("Arial Bold", 10), width=18)
    btnPres.grid(row=1, **argsW)

    btnWpot = Button(frame, text=textWpot, state=DISABLED, relief="flat",font=("Arial Bold", 10), width=18)
    btnWpot.grid(row=2, **argsW)

    btnWind = Button(frame, text=textWind, state=DISABLED, relief="flat",font=("Arial Bold", 10), width=18)
    btnWind.grid(row=3, **argsW)



    
    
    if cbRes.get() == 1:
        btnRes['state'] = NORMAL
        btnRes.configure(text=lng_tuple['ls_opt'],fg = 'blue')
    else: 
        if cbRes.get() == 0:
            btnRes['state'] = DISABLED
            btnRes.configure(text=lng_tuple['ls_n_opt'],fg = 'grey50' )
    if cbPres.get() == 1:
        btnPres['state'] = NORMAL
        btnPres.configure(text=lng_tuple['ls_opt'],fg = 'blue')
    else: 
        if cbPres.get() == 0:
            btnPres['state'] = DISABLED
            btnPres.configure(text=lng_tuple['ls_n_opt'],fg = 'grey50')
    if cbWpot.get() == 1:
        btnWpot['state'] = NORMAL
        btnWpot.configure(text=lng_tuple['ls_opt'],fg = 'blue')
    else: 
        if cbWpot.get() == 0:
            btnWpot['state'] = DISABLED
            btnWpot.configure(text=lng_tuple['ls_n_opt'],fg = 'grey50')    
    if cbWind.get() == 1:
        btnWind['state'] = NORMAL
        btnWind.configure(text=lng_tuple['ls_opt'],fg = 'blue')
    else: 
        if cbWind.get() == 0:
            btnWind['state'] = DISABLED
            btnWind.configure(text=lng_tuple['ls_n_opt'],fg = 'grey50')   
       

            
def delete_all():    
    log_entry.delete(0,END)
    Resv_entry.delete(0,END)
    p_entry.delete(0,END)
    Wpot_entry.delete(0,END)
    Wind_entry.delete(0,END)
    Iter_entry.delete(0,END)
    Relax_entry.delete(0,END)

def delete_text():
    Text_Consol.delete('1.0',END)

def Choise_File_BT(shablon_dir):
    global ChoiseFile_Button
    # var = tk.IntVar()
    text = tk.StringVar()
    text.set("Specify the location of the data file    →")
    lbl_f = Label(root,  height=2, font=("Arial", 10), anchor='w', 
                          fg='black', bg = 'white', textvariable=text)
    lbl_f.grid(row=4, column=0, columnspan=4,rowspan=1,sticky=(E+W),pady = 1, padx =1)
    ChoiseFile_Button = Button(root,text=lng_tuple['ls_choise_data'],
                           height=1, command=lambda: var.set(1) )
    ChoiseFile_Button.config(bg = 'royalblue', fg = 'white')
    ChoiseFile_Button.grid(row=4, column=4, columnspan=1,rowspan=1,sticky=(E+W),pady = 1, padx =1)
    
    while True:
        global LogFilePath
        try:
            ChoiseFile_Button.wait_variable(var)
            
            try:
                LogFilePath = fo.fileopenbox(title=lng_tuple['ls_choise_data'], default=shablon_dir,filetypes= ["*.xls", "*.xlsm"])
                text.set(LogFilePath)
                
            except:
                LogFilePath = fo.fileopenbox(title=lng_tuple['ls_choise_data'], default='*',filetypes= ["*.xls", "*.xlsm"])
                text.set(LogFilePath)
                shablon_dir = os.path.dirname(LogFilePath)
                print('2 480',shablon_dir)    
            try:
                CalcData = pd.read_excel(LogFilePath,'Calculated')
            except:
               
                txt =  LogFilePath+' '+lng_tuple['ls_does not contain'].format('<Calculated>') 
               
                caption = lng_tuple['ls_warning']
                glc.Mbox(None, txt, caption , 0)
                glc.restart()
            try:
                CalcData = pd.read_excel(LogFilePath,'Globals')
            except:
                txt =  LogFilePath+' '+lng_tuple['ls_does not contain'].format('<Globals') 
                caption = lng_tuple['ls_warning']
                glc.Mbox(None, txt, caption , 0)
                glc.restart()
                
            values =  get_values(LogFilePath)
            break
        except ValueError:
            # Resv_entry.delete(0,END)
            text.set("No valid file with input data. Correct it...")
            print(" No valid file with input data. Correct it...")
            rootLogger.info(" No valid file with input data. Correct it...")
    
    values =  get_values (LogFilePath)
    
    entry_insert(LogFilePath,values)
    ChoiseFile_Button.configure(bg ='azure', fg= 'gray')
    
    # ChoiseFile_Button.wait_variable(var)
    return LogFilePath


def Start_Calc_BT(LogFilePath):
    
    LogFilePath = log_entry.get()
   
   
    StartCalc_BT.wait_variable(var_ini)
    StartCalc_BT.configure(bg ='azure', fg= 'gray')
    
    "Call main <get rezult> modul, values may be new  after optimization"
    values = get_Rezult(LogFilePath)
    
    entry_insert(LogFilePath,values)
    
    values.loc[34]=np.float64(cbRes.get()) 
    values.loc[35]=np.float64(cbPres.get()) 
    values.loc[36]=np.float64(cbWpot.get()) 
    values.loc[37]=np.float64(cbWind.get())
    
    Q_button = Button( root, text="Quit", height=1, relief=tk.RAISED,
                              command =  lambda: root.destroy(),  bg = 'orchid', fg ='white' )
    Q_button.grid(row=28, column=4, columnspan=1,rowspan=1,sticky=(E+W),pady = 2, padx =1)    
    Cl_button = Button( root, text=lng_tuple['ls_clear'],  relief=tk.RAISED,
                              command = delete_text,  bg = 'lightsteelblue', fg ='white' )
    Cl_button.grid(row=28, column= 0, columnspan=(1),rowspan=(1),sticky=(E+W),pady = 2, padx =1)
    
    """ Текущая директория файлов исходных данных """
    shablon_dir = str(os.path.dirname(LogFilePath))+str('/')
    
    newobj = DirCalc_BT(shablon_dir)
    StartCalc_BT.configure(bg ='limegreen', fg= 'black')
    return values

def DirCalc_BT(shablon_dir):
    NewDir_Button = Button( root, text=lng_tuple['ls_new'],  height=1, 
                         command =  lambda: Dir_Start(shablon_dir),  bg = 'royalblue',fg ='white'  )
    NewDir_Button.grid(row=28, column=1, columnspan=3,rowspan=1,sticky=(E+W),pady = 1, padx =1)
    Start_Calc_BT(LogFilePath)
   
def Dir_Start(shablon_dir):
    txt = '\n'+lng_tuple['ls_iter_interrupt']+'\n'
    
    rootLogger.info(txt)
    print(txt)
    StartCalc_BT.configure(bg ='limegreen', fg= 'black') 
    log_entry.delete(0,END)
    delete_all()
    ChoiseFile_Button.config(bg = 'royalblue', fg = 'white')
    LogFilePath = Choise_File_BT( shablon_dir)
    values =  get_values (LogFilePath)
    entry_insert(LogFilePath,values)
    print('Dir_Start',LogFilePath)
    
    Start_Calc_BT(LogFilePath)
    StartCalc_BT.configure(bg ='limegreen', fg= 'black') 
    return LogFilePath

''' Блок функций переключения языка диалога '''
def get_lang_lng_tuple(lang):
    result = {}
    with sqlite3.connect('db/lang_schema_new.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        query = """ SELECT ls_name, ls_{} FROM lang_scheme_3""".format(lang)
        cursor.execute(query)
        result = dict(cursor)
    return result 
   
def lang_check(lang):
    global lng_tuple
    lng_tuple = get_lang_lng_tuple(lang)  
    return lng_tuple

def ls_choice(event):
   global lng_tuple
   
   lang = combo_lang.get()
   lng=lang
   
   if lng =='Русский':
       lang = 'ru'
   if lng =='Українська':
       lang = 'uk' 
   if lng =='English':
       lang = 'en'   
   lng_tuple = lang_check(lang)
  
   draw_labels()
   draw_buttons()
   draw_radio(lang)
   isChecked()
   return lang


def draw_radio(lang):
    global  combo_lang
    
    frame = Frame(root, padx = 1, pady =1)
    frame.grid(row=5,column=0)
    lbl = Label(frame, text=lng_tuple['ls_language'], height=1, width = 22, anchor='e',
                bg='white', font=("Arial Bold", 10)) 
    
    lbl.grid(row=0, column=0, sticky=(E+W),pady = 0, padx =1)
    s_var = tk.StringVar()
    Langs = ["English", "Українська", "Русский"]
    
    if lang == 'en': 
       s_var = 0 
    if lang == 'ru': 
       s_var = 2 
    if lang == 'uk': 
       s_var = 1 
       
    combo_lang = ttk.Combobox(frame, values=Langs, textvariable = s_var, state="readonly")
    combo_lang.grid(row=0,column=1, sticky=(E+W), pady = 1, padx =1)
    combo_lang.current(s_var)
    combo_lang.bind('<<ComboboxSelected>>', ls_choice)
    
def draw_labels():
    argsL = {'height':1, 'width':40, 'anchor':'e', 'bg':'white', 'font':("Arial Bold", 10)}
    argLgr0 = {'column':0, 'sticky':(W+E), 'pady':1, 'padx':1}
    argLgr0 = {'column':0, 'sticky':(W+E), 'pady':1, 'padx':1}

    lbl_b = Label( text=lng_tuple['ls_titul'],  height=4,
                      anchor="c", font=("Arial Bold", 14), bg = 'blue', fg='white')
    lbl_b.grid(row=0, column= 0, columnspan=5,rowspan=3,sticky=(N+S+W+E),pady = 3, padx =1)

    lbl = Label( text=lng_tuple['ls_log_file'], **argsL).grid(row=8, **argLgr0)
    lbl = Label( text=lng_tuple['ls_reserv_ini'], **argsL).grid(row=9, **argLgr0)
    lbl = Label( text=lng_tuple['ls_p_ini'], **argsL).grid(row=10, **argLgr0)
    lbl = Label( text=lng_tuple['ls_Water_Poten'],**argsL).grid(row=11, **argLgr0)
    lbl = Label( text=lng_tuple['ls_Water_Index'], **argsL).grid(row=12, **argLgr0)
    lbl = Label( text=lng_tuple['ls_iter'], **argsL).grid(row=13, **argLgr0)
    lbl = Label( text=lng_tuple['ls_relax'], **argsL).grid(row=14, **argLgr0)

    lbl = Label( text=lng_tuple['ls_vol'], height=1, width=22, anchor='w', 
            font=("Arial Bold", 10))
    lbl.grid(row=9, column= 3, sticky=('w'),pady = 1, padx =1)
    lbl = Label( text="  MPa", height=1,  width=22, anchor='w', 
                font=("Arial Bold", 10))
    lbl.grid(row=10, column= 3, sticky=('w'),pady = 1, padx =1)
    lbl = Label( text=lng_tuple['ls_vol'], height=1,  width=22, anchor='w', 
                font=("Arial Bold", 10))
    lbl.grid(row=11, column= 3, sticky=(W),pady = 1, padx =1)
    lbl = Label( text=lng_tuple['ls_q'], height=1, width=22,anchor='w', 
                font=("Arial Bold", 10))
    lbl.grid(row=12, column= 3, sticky=('w'),pady = 1, padx =1)
    lbl = Label( text=lng_tuple['ls_>1'],
                height=1,  anchor='w', 
                font=("Arial Bold", 10), fg = 'blue')
    lbl.grid(row=13, column= 3, columnspan=2,rowspan=(1),sticky='w',pady = 1, padx =1)
    lbl = Label( text=">=1", height=1, width = 14, anchor='w', 
                font=("Arial Bold", 10),fg = 'blue')
    lbl.grid(row=14, column= 3, columnspan=(1),rowspan=(1),sticky='w',pady = 1, padx =1)
    txt =  lng_tuple['ls_comment_1']
    lbl = Label(root, text=txt, anchor='center', height=1, width=66,
                font=("Arial Bold", 12), fg = 'mediumblue' )
    lbl.grid(row=5, column=1, columnspan=4,sticky=(E+W),pady = 1, padx =1)

def draw_buttons():
    global ChoiseFile_Button, StartCalc_BT, Q_button, Cl_button,   NewDir_Button
    ChoiseFile_Button = Button(root,text=lng_tuple['ls_file_loc'],
                          height=1, command=lambda: var.set(1),
                          bg = 'royalblue', fg = 'white')
    
    ChoiseFile_Button.grid(row=4, column=4, columnspan=(1),rowspan=(1),sticky=(E+W),pady = 1, padx =1) 

    StartCalc_BT = Button( root, text=lng_tuple['ls_start'], height=1,
                          command=lambda: var_ini.set(1),
                          bg = 'limegreen', fg = 'white')   
    
    StartCalc_BT.grid(row=15, column= 4, columnspan=(1),rowspan=(1),sticky=(E+W),pady = 1, padx =1)

    Q_button = Button( root, text="Quit",  height=1, relief=tk.RAISED,
                              command =  lambda: sys_exit(),  bg = 'orchid', fg ='white' )
    Q_button.grid(row=28, column= 4, columnspan=(1),rowspan=(1),sticky=(E+W),pady = 2, padx =1)
    Cl_button = Button( root, text=lng_tuple['ls_clear'],  height=1, relief=tk.RAISED,
                              command = delete_text,  bg = 'lightsteelblue', fg ='white' )
    Cl_button.grid(row=28, column= 0, columnspan=(1),rowspan=(1),sticky=(E+W),pady = 2, padx =1)
                              
    NewDir_Button = Button( root, text=lng_tuple['ls_new'], height=1, 
                          command =  lambda: Dir_Start(),  bg = 'royalblue',fg ='white'  )
    NewDir_Button.grid(row=28, column= 1, columnspan=3, rowspan=1,sticky=(E+W),pady = 2, padx =1)

root = tk.Tk()
root.title("Gas field material balance. Version: " + '2.2.3 '+ '01.04.2023')

root.wm_iconbitmap("db/BH256.ico")
root.geometry('940x824+20+20')

top = Toplevel()
top.wm_iconbitmap("db/BH256.ico")
top.geometry('800x630+980+210')
top.withdraw()

top1 = Toplevel()
top1.wm_iconbitmap("db/BH256.ico")
top1.geometry('800x630+1000+20')
top1.withdraw()

locale.setlocale(locale.LC_ALL, "")
""" Всплывающее меню"""
make_textmenu(root)
""" Переключение языка """
global lang, lng_tuple, LogFilePath,values
cbRes = tk.IntVar()
cbPres = tk.IntVar()
cbWpot = tk.IntVar()
cbWind = tk.IntVar()
var = tk.IntVar()
var_ini = tk.IntVar()

lang = locale.getdefaultlocale()[0][:2]
lng_tuple = lang_check(lang)
# print("Current interface language",lang)
s_var = tk.StringVar()
s_var.set(lang)
draw_radio(lang)
lang = ls_choice('<<ComboboxSelected>>')
lng_tuple = lang_check(lang)



draw_labels()
draw_buttons()

root.update()

Text_Consol = ScrolledText(root, font=("Arial", 8), state='normal', height=26)
Text_Consol.grid(row=16, column= 0, columnspan=5,rowspan=12,sticky=(E+W+N+S),pady = 2, padx =1)

target = Text_Consol
rootLogger = getLogger()
rootLogger.setLevel(logging.INFO)
rootLogger.addHandler(ListboxHandler(target))

clmn={'values':[]}
values=pd.DataFrame(clmn)
values.loc[2] =  0.1
values.loc[3] =  0.101325
values.loc[7] =  0.1
values.loc[8] =  0
values.loc[32] = 1
values.loc[33] = 1.2

LogFilePath='no file '

font = ("Arial", 8 )
justify = tk.RIGHT

args = {'column':2, 'sticky':(W+E), 'pady' : 1, 'padx' :1}
log_entry = Entry(root, textvariable=LogFilePath)
log_entry.grid(row=8,  columnspan=3 ,**args)

Resv_entry = Entry(root,textvariable=values.loc[2] )
Resv_entry.grid(row=9, **args)

p_entry = Entry(root,textvariable=values.loc[3])
p_entry.grid(row=10, **args)

Wpot_entry = Entry(root,textvariable=values.loc[7])
Wpot_entry.grid(row=11, **args)

Wind_entry = Entry(root,textvariable=values.loc[8])
Wind_entry.grid(row=12,  **args)

Iter_entry = Entry(root,textvariable=values.loc[32])
Iter_entry.grid(row=13,  **args)

Relax_entry = Entry(root,textvariable=values.loc[33])
Relax_entry.grid(row=14,  **args)

root.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_textmenu)
root.bind_class("Entry", "<Control-a>", callback_select_all)
root.bind_class("Text", "<Button-3><ButtonRelease-3>", show_textmenu_Consol)
root.bind_class("Text", "<Control-a>", callback_select_all)

LogFilePath = Choise_File_BT( '*') # Первый выбор файла данных в дирректории исполняемого файла

values =  get_values(LogFilePath)

# entris() 

cbRes.set(1)
cbPres.set(0)
cbWpot.set(1)
cbWind.set(1)
isChecked()

# "Для прекращения ожидания Choise_File_BT вызываем Start_Calc_BT"
Start_Calc_BT(LogFilePath)

root.mainloop()



