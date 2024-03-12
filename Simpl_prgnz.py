# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 10:57:08 2020

@author: zarub
"""



import datetime
import pandas as pd

import logging
rootLogger = logging.getLogger(__name__)
# Импорт собственных модулей
import file_out_name as fln
import prognosis_simpl as prs
import prognosis_Grups as prg
import func_zRC as Z
import global_lng as gln
import fun_dimRowdrop as dr

def simpl_prgnz(LogFilePath,values,lng_tuple):
    t_begin = datetime.datetime.now()
    print(lng_tuple['ls_lst_mnm'])
    rootLogger.warning(lng_tuple['ls_lst_mnm'])
    info = (lng_tuple['ls_mod_mnm'])
    info=str( "{:.3f}".format(values.loc[2]))
    print(lng_tuple['ls_reserv_ini']+ info +" mln.m.cub" )
    info=str( "{:.2f}".format(values.loc[3]))
    print(lng_tuple['ls_p_ini'] + info +" MPa")
    info=str( "{:.3f}".format(values.loc[7]))
    print (lng_tuple['ls_Water_Poten']+ info +" mln.m.cub")
    info=str( "{:.5e}".format(values.loc[8]))
    print(lng_tuple['ls_Water_Index']+ info +" mln.m.cub(MPa*day)\n\a")
    print(lng_tuple['ls_call_smp'])

    fact = pd.read_excel(LogFilePath,"Calculated")    
    # Удаление строки размерностей
   
    fact = dr.dimRowdrop(fact,'QgasSum' )
    
    flagQ = pd.isna(fact.loc[0,'QgasSum'])

    if flagQ :
        CD, WellTestData, pzData, RegimeGroups, GroupList, CGF = prs.prognosis(LogFilePath,values,lng_tuple)
        
    else:
        CD, WellTestData, pzData, RegimeGroups, GroupList, CGF = prg.prognosis(LogFilePath,values,lng_tuple)
        
    CC=CD
    
    # Формирование фрейма GlobalData
    GlobalDataIni = pd.read_excel(LogFilePath,'Globals')
    
    GlobalData = pd.DataFrame(columns = ['Parametr','Dimensions',
    	'values'])
    name =  gln.global_parametr_name(lng_tuple)
    GlobalData['Parametr'] = name['Name']
    GlobalData['Dimensions'] = name['Dim']
    GlobalData['values'] = GlobalDataIni['values']
    
    Tp = values.loc[1]
    ro=values.loc[9]
    H2S=values.loc[10]
    Co2=values.loc[11]
    N2=values.loc[12]
    
    GlobalData.loc[13,'values'] = Z.zNew(values.loc[3], Tp, ro, H2S, Co2, N2)[1]
    GlobalData.loc[14,'values'] = Z.zNew(values.loc[3], Tp, ro, H2S, Co2, N2)[2]
    GlobalData.loc[15,'values'] = Z.zNew(values.loc[3], Tp, ro, H2S, Co2, N2)[3]
    rootLogger.warning(lng_tuple['ls_cr_fl_mnm'])
    print(lng_tuple['ls_cr_fl_mnm'])
   
    
    t_end = datetime.datetime.now()
    print(lng_tuple['ls_simDuration'] +  " = "+ "%.5s" % ((t_end-t_begin).seconds/60)," min")
    rootLogger.info(lng_tuple['ls_simDuration'] +  " = "+ "%.5s" % ((t_end-t_begin).seconds/60)+" min")
    rootLogger.info("********************************* End *********************************")  
    rootLogger.info("")
   
    ERR=pd.DataFrame(columns = ["Simpl prognos", " no iteration fo ERR"])
    return GlobalData,CC,WellTestData, pzData,CGF,ERR,GroupList,RegimeGroups
    # return   CC, GlobalData,  RegimeGroups, GroupList, Condens