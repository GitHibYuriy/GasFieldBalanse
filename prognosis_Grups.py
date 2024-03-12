# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:15:14 2020

@author: zarub
"""
import datetime
import pandas as pd
import numpy as np
import math

import logging
rootLogger = logging.getLogger(__name__)

# Импорт собственных модулей
import prognosis_Ppl  as pprg
import func_zRC as Z
import fun_pZab_Phead as pz
import fun_Phead_pZab as pH
import fun_ppl as ppl
import fun_reserv_ppl as rs
import fun_q_pHead  as qpH
import fun_q_Dp  as qDp
import fun_q_pZab  as qpZ
import fun_Condensat_main  as cnd
import fun_SumQ_interpolated as qin
import fun_pore_Volume  as pv
import errorer_spline_ppl as err
import dimensions  as dm
import fun_dimRowdrop as dr
import fun_insertColumns as ins
import fun_insertRegColumns  as insR
import groupsFinder  as gf
import control_globals as glc
import control_Well_Test as gwt
def prognosis(LogFilePath,values,lng_tuple):
    

    СalcDataSheet='Calculated'
    CDd = pd.read_excel(LogFilePath,СalcDataSheet)
   
    # Удаление строки размерностей
    CDd = dr.dimRowdrop(CDd,'QgasSum' )

    # Сщздание датафрайм с расчетными данными
    # Добавление столбцов
    # CD = ins.addColumns(CD)
    cols = ['DateCalc','QgasSum','QcondSum','QwaterSum','Wells',
        'Days','pHead','A','B','qGas_C',
    	'kgf','QgasDif_C','QgasSum_C','Reserver_C','QcondDif_C','QcondSum_C',
    	'Influx_C','pPl_C','p-z_C','P_mid','pHead_C','dpRob_C','pBottom_C',
        'pore_Volume_C',' ','Remark' ]
    CD=pd.DataFrame(columns = cols)
    CD['DateCalc']=CDd['DateCalc']
    CD['QgasSum']=CDd['QgasSum']
    CD['QcondSum']=CDd['QcondSum']
    CD['QwaterSum']=CDd['QwaterSum']
    CD['Wells']=CDd['Wells']
    CD['pHead']=CDd['pHead']
    
    QgasSum=CD['QgasSum']
    Dat=CD['DateCalc']
    
    for i in range(len(CD)):
        Qg=QgasSum.loc[i]
       
        Dt=Dat.loc[i]
        if  Qg >=0:
          strokFact =i
        if  not pd.isna(Dt):
          strokAll =i 
          
    # Контроль есть-ли даты для прогнозирования в данных для групп скважин
    # для случая в Calculated даты для прогноза есть, а режимных групп нет
    iniName, RegimeGroups, group_namelist = gf.group_find(LogFilePath, lng_tuple )   
    nr = len(iniName)
    values.loc[30] = nr
    if nr==0:
        strokAll = strokFact 
    strokFact = strokFact + 1
    strokAll = strokAll + 1 
    Ppl=values.loc[3]
    
    # Проверка корректности начальных запасов
    if values.loc[2] <= QgasSum.loc[strokFact - 1]:
        values.loc[2] = round(1.2 * QgasSum.loc[strokFact - 1])
        print(lng_tuple['ls_ini_reserv_correct'])
        rootLogger.info(lng_tuple['ls_ini_reserv_correct'])
    Reserver=values.loc[2]
    
    
    
    
    for i in range(0,strokAll):
        # Дозаполнение количества дней между двумя датами
        if  pd.isna(CD.loc[i,'Days']):
           if i==0:
               if CD.loc[i,'DateCalc'] >= values[29]:
                   CD.loc[i,'Days']=((CD.loc[i,'DateCalc']-values[29]).days)
               else:
                   CD.loc[i,'Days'] = 0
           else:
               CD.loc[i,'Days']=((CD.loc[i,'DateCalc']-
                           CD.loc[i-1,'DateCalc']).days) 
    # Проверка заполненности добычи воды
        if  pd.isna(CD.loc[i,'QwaterSum']):
               if i==0:
                   if pd.isna(values[6]):
                       CD.loc[0,'QwaterSum'] = 0
                   else:
                       CD.loc[0,'QwaterSum'] = values[6]
               else:
                   CD.loc[i,'QwaterSum']= CD.loc[i-1,'QwaterSum']
                   
    # Проверка заполненности количества скважин        
    # for i in range(0,strokFact):        
        if  pd.isna(CD.loc[i,'Wells']) or CD.loc[i,'Wells']<=0 :
            warning = lng_tuple['ls_Fixed number of wells']
            if pd.isnull(CD.loc[i,'Remark']):
                CD.loc[i,'Remark']='Rem.'
            CD.loc[i,'Remark']=warning+CD.loc[i,'Remark']
            if i==0:
                CD.loc[i,'Wells'] = 1
            else:
                CD.loc[i,'Wells'] = CD.loc[i-1,'Wells'] 
                
   #  Начальные данные - на первую дату

    CDD=pprg.prognosis_ppl(LogFilePath, values)
                
    Days = CD.loc[0,'Days']
    CD.loc[0,'pPl_C'] = CDD.loc[0,'pPl_C']
    CD.loc[0,"QgasSum_C"]=values.loc[4] 
    CD.loc[0,"qGas_C"] = 0 
    CD.loc[0,"Reserver_C"]=values[2]
    CD.loc[0,"QcondSum_C"]=values[28]
    CD.loc[0,"Influx_C"]=values[27]
    CD.loc[0,"pBottom_C"]=None
    CD.loc[0,"pHead_C"]=CD.loc[0,"pHead"]
    CD.loc[0,"p-z_C"]=(CD.loc[0,'pPl_C']/
                             Z.zNew(CD.loc[0,'pPl_C'],values[1],
                             values[9],values[10],values[11],values[12])[0])  
            
    # Период фактической добычи        
    for i in range(1,strokFact):
        CD.loc[i,'QgasSum_C']= CD.loc[i,'QgasSum']
        CD.loc[i,'QcondSum_C']= CD.loc[i,'QcondSum']
        CD.loc[i,'QgasDif_C']=(CD.loc[i,'QgasSum_C'] -  CD.loc[i-1,'QgasSum'])
        if CD.loc[i,'Days']==0:
            CD.loc[i,'qGas_C']=CD.loc[i-1,'qGas_C']
        else:
            CD.loc[i,'qGas_C']=(CD.loc[i,'QgasDif_C']
                                  /CD.loc[i,'Days']/
                                  CD.loc[i,'Wells']*1000)
        CD.loc[i,'Reserver_C']=(CD.loc[0,'Reserver_C']-
                                      CD.loc[i,'QgasSum_C'])
        Reserver=CD.loc[0,'Reserver_C']
        QgasSum=CD.loc[i,'QgasSum']
        QwaterSum=CD.loc[i,'QwaterSum']
        Influx=CD.loc[i-1,"Influx_C"]
        Days=CD.loc[i,'Days']

        """ ppp=ppl.GDW_p_plast(Ppl, Reserver, QgasSum, 
                        QwaterSum, Influx, Days,  values) """
        # CD.loc[i,'pPl_C']=ppp[0]
        CD.loc[i,'pPl_C']=CDD.loc[i,'pPl_C']
        
        p_p= CD.loc[i,'pPl_C']
        zzz = Z.zNew(p_p,values[1],
                             values[9],values[10],values[11],values[12])[0]
        CD.loc[i,"p-z_C"]=p_p/zzz
        # CD.loc[i,'Influx_C']=ppp[1]
        CD.loc[i,'Influx_C']=CDD.loc[i,'Influx_C']
        CD.loc[i,'pore_Volume_C']=pv.pore_volume( Reserver,  Ppl, 
                     CD.loc[i,'pPl_C'], CD.loc[i,'Influx_C'], QwaterSum,  values)        
        p1 = CD.loc[i,'pPl_C']
        p2 = CD.loc[i-1,'pPl_C']
        p_mid = (p1+p2)/2 
        CD.loc[i,'P_mid']=  p_mid




        CD.loc[i,'pHead_C']=CD.loc[i,'pHead']
        p_p = CD.loc[i,'qGas_C']
        p_h =  CD.loc[i,'pHead_C']
        P_b = pz.p_zab(p_p, p_h, values)[0]        
        CD.loc[i,'pBottom_C']=P_b    
        CD.loc[i,'dpRob_C'] = p_mid-CD.loc[i,'pBottom_C']       
        if CD.loc[i,'pBottom_C']>=p_mid or CD.loc[i,'dpRob_C']<=0:
            warning = lng_tuple['ls_low_high_wrn'] 
            CD.loc[i,'Remark']= warning
        if  CD.loc[i,'qGas_C']==0 or CD.loc[i,'dpRob_C']<0:
            CD.loc[i,'A']=np.nan
        else:
            p_p = CD.loc[i-1,'pPl_C']
            p_b = CD.loc[i,'pBottom_C']
            p_q = CD.loc[i,'qGas_C']
            CD.loc[i,'A']=(p_p**2 - p_b**2)/ p_q
        CD.loc[i,'B']=0

       
 
    """" На период прогноза  """    
    
    # Контроль создания имен и данных для групп скважин
    iniName, RegimeGroups, group_namelist = gf.group_find(LogFilePath, lng_tuple )
    
    
    nr = len(iniName)
    values.loc[30] = nr
    
    for j in range (0,nr):
        name=iniName[j]        
        RegimeGroups[j]=pd.read_excel(LogFilePath,name)
        # print ('Удаление строки размерностей RegimeGroups ' j)
        RegimeGroups[j] = dr.dimRowdrop(RegimeGroups[j],'Wells' )
        
        # Добавление столбцов
        RegimeGroups[j] = insR.addRegColumns(RegimeGroups[j])
        RegimeGroups[j]['DateCalc'] = CD['DateCalc']
        RegimeGroups[j]['Days'] = CD['Days'] 
        
        for i in range(0,strokFact): 
            RegimeGroups[j].loc[i,'A'] = CD.loc[i,'A']
            RegimeGroups[j].loc[i,'B'] = CD.loc[i,'B']
    # Valid regime names         
    regims = ['pHead' , 'dpRob' ,  'pBottom' , 'pB_pPl_fraction',  'q'] 
    
    R_flag = 1 # Flag запасы еще не исчерпаны
    for i in range(strokFact, strokAll ):
        
        
        Influx = CD.loc[i-1,'Influx_C']
        Days = CD.loc[i,'Days']
        CD.loc[i,'Wells']= 0
        CD.loc[i,'QgasDif_C']= 0
        CD.loc[i,'QgasSum_C'] = 0
        CD.loc[i,'qGas_C'] = 0
        # расчет по режимным группам
        for j in range (0,nr):
            # name='Group_'+str(j)
            CR=RegimeGroups[j]
            # Проверка наличия группы j на временном слое i
            if not pd.isnull(CR.loc[i,'Wells']):
                # Начало расчета по режимной группе j
                if CR.loc[i,'Regim'] not in regims:
                # Regime name  checking      
                    warning =lng_tuple['ls_nreg_wrn']
                    if pd.isnull(CR.loc[i,'Remark']):
                        
                        CR.loc[i,'Remark']='Rem.'
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']     
                        CR.loc[i,'Regim']='pHead' 
                        CR.loc[i,'pHead']=CR.loc[i-1,'pHead_C']
                        
                    if i == strokFact:
                        
                        warning = lng_tuple['ls_wpr_wrn']
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']  
                        CR.loc[i,'Regim']='pHead' 
                        CR.loc[i,'pHead']=CD.loc[i-1,'pHead']
                    else:
                        warning = lng_tuple['ls_perv_wrn']
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']
                        CR.loc[i,'Regim']=CR.loc[i,'Regim']
                        CR.loc[i,'pHead']=CR.loc[i-1,'pHead_C']
                        CR.loc[i,'dpRob']=CR.loc[i-1,'dpRob_C']
                        CR.loc[i,'pBottom']=CR.loc[i-1,'pBottom']
                        CR.loc[i,'q']=CR.loc[i-1,'q'] 
                # Flow resistencess factors checking        
                A=CR.loc[i,'A']
                B=CR.loc[i,'B']
                if pd.isnull(A) or pd.isnull(B) or np.isnan(A) or np.isnan(B) or A==0:
                        warning =lng_tuple['ls_nindex_wrn']
                        if pd.isnull(CR.loc[i,'Remark']):
                            CR.loc[i,'Remark']='Rem.'
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']
                        k=i-1  
                        m=i                    
                        for jk in range(m-1,0,-1):
                            A=CR.loc[jk,'A']
                            B=CR.loc[jk,'B']
                        
                            if (not pd.isnull(A) and not  pd.isnull(B) 
                                and not np.isnan(A) and not np.isnan(B) and A!=0):
                                k=jk                            
                                break
                            
                        A=CR.loc[k,'A']
                        B=CR.loc[k,'B']
                    
                CR.loc[i,'A']=A
                CR.loc[i,'B']=B
    
                # Режим постоянного дебита    
                if CR.loc[i,'Regim'] == 'q':
                    if pd.isnull(CR.loc[i,'q']):
                        warning =lng_tuple['ls_nreg_par_wrn']
                        CR.loc[i,'Remark']='Rem.'
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark'] 
                        CR.loc[i,'q']=0 
                    
                    CR.loc[i,'qGas_C']=CR.loc[i,'q']
    
                    # Depression revising 
                    dtc=CD.loc[i-1,'pPl_C']**2
                    if not pd.isnull(CR.loc[i,'q']):
                        dtc=(CD.loc[i-1,'pPl_C']**2 - (A*CR.loc[i,'q']
                                - B*CR.loc[i,'q']**2)*np.sign(CR.loc[i,'q']))
                                    
                    if dtc < 0:
                            warning =lng_tuple['ls_abfree_wrn']
                            if pd.isnull(CR.loc[i,'Remark']):
                                CR.loc[i,'Remark']='Rem. '                        
                            CR.loc[i,'Remark']=warning +CR.loc[i,'Remark']
                            
                            pHead=0.101325
                            CR.loc[i,'qGas_C']=qpH.qGas( pHead, p_mid,
                                            A, B, values)[0]
                            CR.loc[i,'pBottom_C']=pz.p_zab( CR.loc[i,'qGas_C'], pHead,  values)[0]
                    else: 
                            CR.loc[i,'pBottom_C']=math.sqrt(dtc) 
                            
                    CR.loc[i,'pHead_C']=pH.pHead(CR.loc[i,'q'], 
                                    CR.loc[i,'pBottom_C'], values)[0]
                    if CR.loc[i,'pHead_C'] < 0.101325:
                            warning =lng_tuple['ls_abfree_wrn']
                            if pd.isnull(CR.loc[i,'Remark']):
                                CR.loc[i,'Remark']='Rem. '                        
                            CR.loc[i,'Remark']=warning +CR.loc[i,'Remark']                          
                            pHead=0.101325
                            CR.loc[i,'pHead_C']=pHead
                            
                            CR.loc[i,'qGas_C']=qpH.qGas( pHead, p_mid,
                                            A, B, values)[0]                            
                            CR.loc[i,'pBottom_C']=pz.p_zab( CR.loc[i,'qGas_C'], pHead,  values)[0]
                            
                    CR.loc[i,'dpRob_C']=CD.loc[i-1,'pPl_C']-CR.loc[i,'pBottom_C']  
                    CR.loc[i,'QgasDif_C']=(CR.loc[i,'q']*CR.loc[i,'Days']*
                                    CR.loc[i,'Wells']/1000*values[19])
                    
                # Режим постоянного рабочого давления
                if CR.loc[i,'Regim'] == 'pHead':                     
                    # Проверка параметра режима 
                    if pd.isnull(CR.loc[i,'pHead']):
                        warning =lng_tuple['ls_nreg_par_wrn']
                        if pd.isnull(CR.loc[i,'Remark']):
                            CR.loc[i,'Remark']='Rem.'
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']     
                        if i==strokFact:
                            CR.loc[i,'pHead']=CD.loc[i-1,'pHead_C']
                        else:    
                            CR.loc[i,'pHead']=CR.loc[i-1,'pHead_C']
                            
                    pHead = CR.loc[i,'pHead']
                    q = qpH.qGas( pHead, CD.loc[i-1,'pPl_C'], A, B, values)[0]
                    
                    CR.loc[i,'qGas_C'] = q
                    if CR.loc[i,'qGas_C'] < 0:
                        if pd.isnull(CR.loc[i,'Remark']):
                            CR.loc[i,'Remark']='Rem.'
                        warning =lng_tuple['ls_inject_wrn']
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']
                    pBott =  pz.p_zab( CR.loc[i,'qGas_C'], pHead,  values)[0]   
                    CR.loc[i,'pBottom_C'] = pBott    
                    CR.loc[i,'dpRob_C']=CD.loc[i-1,'pPl_C']-CR.loc[i,'pBottom_C']      
                    # Контрольное рабочее пересчитанное с забойного                    
                    CR.loc[i,'pHead_C']=pH.pHead(q,  pBott, values)[0]
                    
                    day = CR.loc[i,'Days']
                    wls = CR.loc[i,'Wells']
                    sq = q*day*wls*values[19]/1000
                    CR.loc[i,'QgasDif_C'] = sq
    
                # Режим постоянной депрессии                       
                if CR.loc[i,'Regim'] == 'dpRob':
                    # Проверка параметра режима 
                    if pd.isnull(CR.loc[i,'dpRob']):
                        warning =lng_tuple['ls_nreg_par_wrn']+lng_tuple['ls_30dpr_wrn']
                        if pd.isnull(CR.loc[i,'Remark']):
                            CR.loc[i,'Remark']='Rem.'
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']       
                        CR.loc[i,'dpRob']=0.3*CD.loc[i-1,'pPl_C']                    
                                    
                    Dp= CR.loc[i,'dpRob']
                    pl= CD.loc[i-1,'pPl_C']
                    # Проверка не превішает-ли депрессия пластовое давление 
                    if Dp>=pl:
                        Dp = 0.3 * pl
                        if pd.isnull(CR.loc[i,'Remark']):
                            CR.loc[i,'Remark']='Rem.'
                        warning =lng_tuple['ls_impos_wrn']+lng_tuple['ls_30dpr_wrn']
                        CR.loc[i,'Remark']=  warning+CR.loc[i,'Remark'] 
                        
                    CR.loc[i,'dpRob_C']=Dp
                    CR.loc[i,'qGas_C']=qDp.qGas_Dp(Dp, pl, A, B, values)
                    if CR.loc[i,'qGas_C'] < 0:
                        if pd.isnull(CR.loc[i,'Remark']):
                            if pd.isnull(CR.loc[i,'Remark']):
                                CR.loc[i,'Remark']='Rem.'
                        warning =lng_tuple['ls_inj_mode_wrn']
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']
                        
                    CR.loc[i,'pBottom_C'] = CD.loc[i-1,'pPl_C'] - CR.loc[i,'dpRob_C']                    
                    CR.loc[i,'pHead_C']=pH.pHead(q, CR.loc[i,'pBottom_C'], values)[0]
                    
                    q =  CR.loc[i,'qGas_C']    
                    day = CR.loc[i,'Days']
                    wls = CR.loc[i,'Wells']
                    sq = q*day*wls*values[19]/1000
                    CR.loc[i,'QgasDif_C'] = sq    
                    
                    
                # Режим постоянного забойного давления                
                if CR.loc[i,'Regim'] == 'pBottom':
                    # Проверка параметра режима 
                    if pd.isnull(CR.loc[i,'pBottom']) or CR.loc[i,'pBottom']>=CD.loc[i-1,'pPl_C']:
                        warning =lng_tuple['ls_incorrect_wrn']+lng_tuple['ls_bhpr70_wrn']
                        CR.loc[i,'Remark']='Rem.'
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']   
                        CR.loc[i,'pBottom']=0.7*CD.loc[i-1,'pPl_C']                          
                    pBottom = CR.loc[i,'pBottom']
                    pl= CD.loc[i-1,'pPl_C']
                    q = qpZ.qGas_Bt(pBottom, pl, A, B, values)
                    CR.loc[i,'qGas_C'] = q
                    CR.loc[i,'pBottom_C']=pBottom
                    CR.loc[i,'dpRob_C']= CD.loc[i-1,'pPl_C'] - pBottom
                    
                    if CR.loc[i,'qGas_C'] < 0:
                        if pd.isnull(CR.loc[i,'Remark']):
                            CR.loc[i,'Remark']='Rem.'
                        warning =lng_tuple['ls_inj_mode_wrn']
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']
                    CR.loc[i,'pHead_C']=pH.pHead(q, CR.loc[i,'pBottom_C'], values)[0]    
                    q =  CR.loc[i,'qGas_C']    
                    day = CR.loc[i,'Days']
                    wls = CR.loc[i,'Wells']
                    sq = q*day*wls*values[19]/1000
                    CR.loc[i,'QgasDif_C'] = sq   
                # Режим постоянного забойного давления в доле от пластового                 
                if CR.loc[i,'Regim'] == 'pB_pPl_fraction':
                    # Проверка параметра режима 
                    if pd.isnull(CR.loc[i,'pB_pPl_fraction']):
                        warning =lng_tuple['ls_incorrect_wrn']+lng_tuple['ls_bhpr70_wrn']
                        CR.loc[i,'Remark']='Rem.'
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']   
                        CR.loc[i,'pB_pPl_fraction']=0.7                          
                    pBottom = CR.loc[i,'pB_pPl_fraction']*CD.loc[i-1,'pPl_C']
                    pl= CD.loc[i-1,'pPl_C']
                    q = qpZ.qGas_Bt(pBottom, pl, A, B, values)
                    CR.loc[i,'qGas_C'] = q
                    CR.loc[i,'pBottom_C']=pBottom
                    CR.loc[i,'dpRob_C']= CD.loc[i-1,'pPl_C'] - pBottom
                    
                    if CR.loc[i,'qGas_C'] < 0:
                        if pd.isnull(CR.loc[i,'Remark']):
                            CR.loc[i,'Remark']='Rem.'
                        warning =lng_tuple['ls_inj_mode_wrn']
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']
                    CR.loc[i,'pHead_C']=pH.pHead(q, CR.loc[i,'pBottom_C'], values)[0]    
                    q =  CR.loc[i,'qGas_C']    
                    day = CR.loc[i,'Days']
                    wls = CR.loc[i,'Wells']
                    sq = q*day*wls*values[19]/1000
                    CR.loc[i,'QgasDif_C'] = sq                           
            
                # Конец расчета по режимной группе j
                RegimeGroups[j]=CR
            else:
                CR.loc[i,'Wells'] = 0
                CR.loc[i,'QgasDif_C'] = 0
            
            # Суммирование по группам скважин      
        
            CD.loc[i,'Wells'] = CD.loc[i,'Wells'] + CR.loc[i,'Wells']
            
            qdd =  CD.loc[i,'QgasDif_C']
            qdr = CR.loc[i,'QgasDif_C']
            CD.loc[i,'QgasDif_C'] = qdd + qdr                
            CD.loc[i,'QgasSum_C']=CD.loc[i-1,'QgasSum_C'] + CD.loc[i,'QgasDif_C']
            
            w = CD.loc[i,'Wells']
            d = CD.loc[i,'Days']
            CD.loc[i,'qGas_C'] = CD.loc[i,'QgasDif_C']*1000/w/d/values[19]
                 
        # Расчет запасов и пластового давления после суммирования добычи по режимам 

        CD.loc[i,'Reserver_C']=(CD.loc[0,'Reserver_C'] -  CD.loc[i,'QgasSum_C'])


        if CD.loc[i-1,'Reserver_C']<=0.00 or  CD.loc[i-1,'pPl_C']<=0.101325 or CD.loc[i,'QgasDif_C']>=CD.loc[i-1,'Reserver_C']:
            R_flag = 0   # запасы исчерпаны
            if pd.isnull(CD.loc[i,'Remark']):
                CD.loc[i,'Remark']='Rem.'
            warning =lng_tuple['ls_exhaust_wrn']
            print(lng_tuple['ls_to_wrn'], CD.loc[i,'DateCalc'].strftime("%Y-%m-%d"),  lng_tuple['ls_exhaust_wrn'])
            rootLogger.info("To "+ CD.loc[i,'DateCalc'].strftime("%Y-%m-%d")+lng_tuple['ls_exhaust_wrn'])
            CD.loc[i,'Remark']=warning+CD.loc[i,'Remark']
            # Остаточное пластовое давление при давлении на устье 0.101325 МПа
            
            # Остаточные неизвлекаемые запасы
            # rest =  rs.reserv_plast(prest, Ppl, Reserver, QwaterSum, Influx, Days, values)            
           
            CD.loc[i-1,'Reserver_C']=0
            CD.loc[i,'Reserver_C']=0
            CD.loc[i-1,'QgasSum_C']=CD.loc[0,'Reserver_C']
            CD.loc[i,'QgasSum_C']=CD.loc[0,'Reserver_C']
            CD.loc[i-1,'QgasDif_C']=0
            CD.loc[i,'QgasDif_C']=0
            CD.loc[i-1,'qGas_C']=0
            CD.loc[i,'qGas_C']=0

        ppp=ppl.GDW_p_plast(Ppl, Reserver, 
                CD.loc[i,'QgasSum_C'], CD.loc[i,'QwaterSum'],  
                CD.loc[i-1,'Influx_C'], CD.loc[i,'Days'],
                values)
      
        CD.loc[i,'pPl_C']= ppp[0]
        CD.loc[i,'Influx_C']=ppp[1]
        CD.loc[i,'pore_Volume_C']=pv.pore_volume( Reserver,  Ppl,  ppp[0], ppp[1],
                                                 CD.loc[i,'QwaterSum'],  values) 
        # CD.loc[i,'pore_Volume_C']=pv.pore_volume( Reserver,  Ppl,  ppp[0], ppp[1], QwaterSum,  values) 
        CD.loc[i,"p-z_C"]=(CD.loc[i,'pPl_C']/
                            Z.zNew(CD.loc[i,'pPl_C'],values[1],
                            values[9],values[10],values[11],values[12])[0])
        CD.loc[0,'P_mid']= CD.loc[0,'pPl_C']

       
        # Среднее за период пластовое давление
        for i in range(1,len(CD['pPl_C'])):        
            a=CD.loc[i-1,'pPl_C']
            b=CD.loc[i,'pPl_C']
            CD.loc[i,'P_mid']= (a+b)/2

    "Расчет добычи конденсата" 
    if pd.isnull(CD.loc[strokFact-1,'QcondSum']):       
        print(lng_tuple['ls_n_cnd_wrn']) 
        warning =lng_tuple['ls_n_cnd_wrn']
        CD.loc[i,'Remark']='Rem.'
        CD.loc[i,'Remark']=  warning+CD.loc[i,'Remark']
        CD.loc[strokFact-1,'QcondSum']=0 
    print(lng_tuple['ls_cnd_clc_wrn'])
    CndData = pd.DataFrame(columns = ['Pres','kgf','','P_mid', 'QgasSum','QcondDif','QcondSum','KGF','a','b','c']) 
    
    
    
    CdChrt = pd.read_excel(LogFilePath,'CondFactor')
      # Удаление строки размерностей
    CdChrt = dr.dimRowdrop(CdChrt,'Pres' )
    CndData['P_mid']=CD['P_mid']
    CndData['QgasSum']=CD['QgasSum']
    CndData['QcondSum']=CD['QcondSum']
    CndData['Pres']=CdChrt['Pres']     
    CndData['kgf']=CdChrt['kgf']
    
    CndData =  cnd.condensat(CndData,lng_tuple)
    # Возвращен фрейм фрейм  CndData['Pres','kgf', 'P_mid', 'QgasSum','QcondSum','KGF','a','b','c']]
   
    CD['kgf'] = CndData['KGF']

    for i in range(0,strokFact):            
        CndData.loc[i,'QgasSum']=CD.loc[i,'QgasSum']
        CndData.loc[i,'QcondSum']=CD.loc[i,'QcondSum']

   
    for i in range(strokFact,strokAll ):
        if CD.loc[i,'QgasDif_C']<0:
            CD.loc[i,'QgasDif_C'] = 0
        if pd.isna(CD.loc[i-1,'QcondSum_C']):
            CD.loc[i-1,'QcondSum_C']=0
        cs0 = CD.loc[i-1,'QcondSum_C']        
        kgf = CD.loc[i,'kgf']
        CD.loc[i,'kgf'] =  kgf
        gs = CD.loc[i,'QgasDif_C']            
        cdd = gs * kgf / 1000
        CD.loc[i,'QcondDif_C']= cdd
        scd = cs0+cdd            
        CD.loc[i,'QcondSum_C']= scd   
   
        CndData.loc[i,'QgasSum']=CD.loc[i,'QgasSum_C']
        CndData.loc[i,'QcondSum']=CD.loc[i,'QcondSum_C'] 
        
    CndData['QcondDif']=CD['QcondDif_C']   
    # CD['DateCalc'] =np.array(CD['DateCalc'],dtype='datetime64[D]')
    # cols = ['Intepolated','ppl/z','P_prognz','p/z','Q_all', 'Remark']
    # DF = pd.DataFrame (columns=cols, index=[]) 
    # print('DF',DF.columns)
    # DF.insert(2,'RyadName',[])
    # print('DF',DF.columns)


    # Создание фрейма для листа WellTestData
    # Исправление суммарной добычи в таблице WellTestData сплайн интерполяцией

    LogDataSheet='WellTestData'
    TestData = pd.read_excel(LogFilePath,LogDataSheet)
    


    try:
        
        print(lng_tuple['ls_prd_correct_wrn'])
        rootLogger.info(lng_tuple['ls_prd_correct_wrn'])    
        LogDataSheet='WellTestData'
        TestData = pd.read_excel(LogFilePath,LogDataSheet)
        # Удаление строки размерностей
        TestData = dr.dimRowdrop(TestData,'ppl')
        try:
            TestData.insert(2,'RyadName',' ')
        except:
            pass

        # Формирование имен для категорий точек измерения давления,
        # если категорий больше 15, все в одной категории 'All'
        
        df2 = TestData['Wellname'] 
        df3 = TestData['Method']
        df3 = df3.replace(np.nan, '', regex=True) 
        RyadName = df2.astype(str) + df3.astype(str)
        categories=np.unique(RyadName)
        if len(categories) <16:
            TestData['RyadName']=RyadName
        else:
            for i in range(0,len(df2)):
               TestData.loc[i,'RyadName'] = 'All wells'

        cols = ['Intepolated','ppl/z','P_prognz','p/z','Q_all', 'Remark']
        WTD = pd.DataFrame (columns=cols, index=[])
        try:
            WellTestData=pd.concat([TestData,WTD])
        except:
            WellTestData = TestData
        # Исправление если не введено  'Weight'
        for i in range(0,len(TestData['Weight'])):
            if pd.isna(TestData.loc[i,'Weight'] ):
                WellTestData.loc[i,'Weight'] = 1
                WellTestData.loc[i,'Remark']="<Weight> is set to 1" 
            else:
                WellTestData['Weight']=TestData['Weight']
        
        try:
            WellTestData=qin.SumQ_interpolated(LogFilePath, WellTestData, values,lng_tuple)
           
        except:
            print(lng_tuple['ls_inter_failed_wrn'])
            rootLogger.info(lng_tuple['ls_inter_failed_wrn'])
        else:
            print(lng_tuple['ls_inter_suc_wrn'])
            rootLogger.info(lng_tuple['ls_inter_suc_wrn'])
        
        
        # RyadName =  WellTestData['RyadName']   
        # categories=np.unique(RyadName)
        
        Tp = values[1]
        ro=values[9]
        H2S=values[10]
        Co2=values[11]
        N2=values[12]
        
        #  Создание столбца для фактичнского  'ppl/z'          
        # WellTestData['ppl/z']=WellTestData['ppl']
        for i in range(0,len(WellTestData.index)):
            Z_ryad=Z.zNew(WellTestData.loc[i,'ppl'], Tp, ro, H2S, Co2, N2)[0]
            WellTestData.loc[i,'ppl/z']=WellTestData.loc[i,'ppl']/Z_ryad
        
        
        # Прогнозные значения пластового давления на дату исследования
        sum_sq_err, RMS, sum_weight, progn, bgn, lst  = err.errorer(LogFilePath,values,lng_tuple)  
        WellTestData['P_prognz'] = progn

        
        for i in range(0, len(WellTestData.index)):
            date = WellTestData.loc[i,'dateTest'].date()
            if date > lst:                
                    WellTestData.loc[i,'Weight'] = 0 
                    
        #  Создание столбца для прогнозного 'p/z'          
        # WellTestData['p/z']=WellTestData['ppl']
        for i in range(0,len(WellTestData.index)):
            Z_ryad=Z.zNew(WellTestData.loc[i,'P_prognz'], Tp, ro, H2S, Co2, N2)[0]
            WellTestData.loc[i,'p/z']=WellTestData.loc[i,'P_prognz']/Z_ryad
             
        try:
            WellTestData['Q_all']=WellTestData['Intepolated']
            print(lng_tuple['ls_use_inter_wrn'])
            rootLogger.info(lng_tuple['ls_use_inter_wrn'])
        except ValueError:
            WellTestData['Q_all']=WellTestData['SumQ_inputed']
            print(lng_tuple['ls_use_enter_wrn'])
            rootLogger.info(lng_tuple['ls_use_enter_wrn'])
            
        except:
            WellTestData['Q_all'] = np.round(values[2]/2,decimals=0)
            print(lng_tuple['ls_int_failed_nent _wrn'])
            rootLogger.info(lng_tuple['ls_int_failed_nent _wrn'])
         
            
        # Создание отдельного фрейма  для приведенного давления  p/z 
        cols = ['RyadName','p/z fact','Q_all','  ','p/z model','Q model','  ','Value','Dimention','Info']
        pzData = pd.DataFrame (columns=cols)
        pzData['RyadName']=RyadName
        pzData['p/z fact']= WellTestData['p/z']
        pzData['Q_all']= WellTestData['Q_all']        
        pzData['p/z model']= CD['p-z_C']
        pzData['Q model']= CD['QgasSum_C']
    except:
        cols = ['Wellname','Method','Weight','dateTest','ppl','SumQ_inputed','Intepolated','ppl/z','P_prognz','p/z','Q_all','Remark']
        WellTestData = pd.DataFrame (columns=cols)
        cols = ['RyadName','p/z fact','Q_all','  ','p/z model','Q model','  ','Value','Dimention','Info']
        pzData = pd.DataFrame (columns=cols)
        # pzData.loc[1,'RyadName'] = lng_tuple['ls_no_pressure_data']+LogFilePath
        pzData.loc[2,'RyadName'] = 'No pressure_data in file' + LogFilePath
        colst = ['Wellname','Method','Weight','dateTest','ppl','SumQ_inputed','Intepolated','ppl/z','P_prognz','p/z','Q_all','Remark']
        WellTestData = pd.DataFrame (colst)
        WellTestData.loc[2,'Wellname'] = 'No pressure_data in file' + LogFilePath
    print(lng_tuple['ls_succes_wrn'])
 
    return CD, WellTestData, pzData,  RegimeGroups, group_namelist, CndData
