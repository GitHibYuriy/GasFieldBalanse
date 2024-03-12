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

import func_zRC as Z
import fun_pZab_Phead as pz
import fun_Phead_pZab as pH
import fun_ppl as ppl
import fun_reserv_ppl as rs
import fun_q_pHead  as qpH
import fun_q_Dp  as qDp
import fun_q_pZab  as qpZ
import fun_Condensat_main  as cnd

import fun_pore_Volume  as pv

import fun_dimRowdrop as dr
import fun_insertColumns as ins
import fun_insertRegColumns  as insR
import groupsFinder  as gf

def prognosis(LogFilePath,values,lng_tuple):
    """ Основной модуль расчета показателей разработки без процедуры адаптации """
    
    СalcDataSheet='Calculated'
    CD = pd.read_excel(LogFilePath,СalcDataSheet)
    
    # Удаление строки размерностей
    CD = dr.dimRowdrop(CD,'QgasSum')
    # Добавление столбцов
    CD = ins.addColumns(CD)

    # strokAll=len(CD)
    QgasSum=CD['QgasSum']
    Dat=CD['DateCalc']
    strokFact = 0
    for i in range(len(CD)):
        Qg=QgasSum.loc[i]
        Dt=Dat.loc[i]
        if  Qg >=0:
            strokFact = i
            
        if  not pd.isna(Dt):
             strokAll =i 
    strokFact = strokFact + 1
    strokAll = strokAll + 1
    Ppl=values.loc[3]
    Reserver=values.loc[2]
    QgasSum=values.loc[4]
    QwaterSum=values.loc[6]
    Influx=values.loc[27]
    Days=0
    CD.loc[0,'Days']=None
    
    CD.loc[0,'pPl_C']=ppl.GDW_p_plast(Ppl, Reserver, QgasSum, 
                            QwaterSum, Influx, Days,  values)[0] 
    
    
    CD.loc[0,"QgasSum_C"]=values.loc[4]
    CD.loc[0,"QgasSum"]=values.loc[4]
    CD.loc[0,"Reserver_C"]=values.loc[2]
    CD.loc[0,"QcondSum_C"]=values.loc[28]
    CD.loc[0,"QcondSum"]=values.loc[28]
    CD.loc[0,"Influx_C"]=values.loc[27]
    CD.loc[0,"pBottom_C"]=None
    CD.loc[0,"pHead_C"]=None
    CD.loc[0,"p-z_C"]=(CD.loc[0,'pPl_C']/
                             Z.zNew(CD.loc[0,'pPl_C'],values.loc[1],
                             values.loc[9],values.loc[10],values.loc[11],values.loc[12])[0])
    
    for i in range(0,strokAll):
        if i==0:
            CD.loc[i,'Days']=0
            
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
                      CD.loc[i,'QwaterSum']=CD.loc[i-1,'QwaterSum']        
                       
                
    # Проверка заполненности количества скважин        
    for i in range(0,strokAll):        
        if  pd.isna(CD.loc[i,'Wells']):
            if i==0:
                CD.loc[i,'Wells'] = 1
            else:
                if  i > strokFact-1:
                   CD.loc[i,'Wells'] = 0
                else:
                   CD.loc[i,'Wells'] = CD.loc[i-1,'Wells']


    # Период фактической добычи если он существует   
    
    # CDD=pprg.prognosis_ppl(LogFilePath, values)     
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
        # CD.loc[i,'pPl_C']=CDD.loc[i,'pPl_C']
        
        p_p= CD.loc[i,'pPl_C']
        zzz = Z.zNew(p_p,values[1],
                             values[9],values[10],values[11],values[12])[0]
        CD.loc[i,"p-z_C"]=p_p/zzz
        # CD.loc[i,'Influx_C']=ppp[1]
        # CD.loc[i,'Influx_C']=CDD.loc[i,'Influx_C']
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
    for j in range (0,nr):
        name=iniName[j]        
        RegimeGroups[j]=pd.read_excel(LogFilePath,name)
        # Удаление строки размерностей
        RegimeGroups[j] = dr.dimRowdrop(RegimeGroups[j],'Wells' )
        # Добавление столбцов
        RegimeGroups[j] = insR.addRegColumns(RegimeGroups[j])
        RegimeGroups[j]['DateCalc'] = CD['DateCalc']
        RegimeGroups[j]['Days'] = CD['Days'] 
    
        
            
    # Valid regime names    
    regims = ['pHead' , 'dpRob' ,  'pBottom', 'pB_pPl_fraction', 'q'] 
    

    for i in range(strokFact, strokAll ):
        p_mid = CD.loc[i-1,'pPl_C']            
        Influx = CD.loc[i-1,'Influx_C']
        Days = CD.loc[i,'Days']
        # CD.loc[i,'Wells']= 0
        CD.loc[i,'QgasDif_C']= 0
        CD.loc[i,'qGas_C'] = 0

        for j in range (0,nr):
            name='Group_'+str(j)
            CR=RegimeGroups[j] 
            # Проверка наличия группы j на временном слое i
                        
            if not pd.isnull(CR.loc[i,'Wells']) and CR.loc[i,'Wells']!=0 :
                
                # Начало расчета по режимной группе j
                # Well regimes checking
                if CR.loc[i,'Regim'] not in regims:
                    warning =lng_tuple['ls_nreg_wrn']
                    if pd.isnull(CR.loc[i,'Remark']):
                        CR.loc[i,'Remark']='Rem.'
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']     
                        CR.loc[i,'Regim']=regims[0] 
                        CR.loc[i,'pHead']=CR.loc[i-1,'pHead_C']
                    if i == 1:
                        warning = lng_tuple['ls_nreg_par_wrn']+lng_tuple['ls_30dpr_wrn']
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']  
                        CR.loc[i,'Regim']=regims[1] 
                        CR.loc[i,'dpRob_C']=0.7 * CD.loc[i-1,'pPl_C']
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
                        if i == 1:
                            A = 10 
                            B = 0
                        else:
                            k=i-1  
                            m=i
                            for jk in range(m-1,0,-1):
                                A=CR.loc[jk,'A']
                                B=CR.loc[jk,'B']
                                # print('i=',i,'j=', j, 'A=', A,) 
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
                        if i==0:
                            CR.loc[i,'pHead']=0.95*CD.loc[i-1,'pPl_C']
                        else:    
                            CR.loc[i,'pHead']=CR.loc[i-1,'pHead_C']
                            
                    pHead = CR.loc[i,'pHead']
                    q = qpH.qGas( pHead, CD.loc[i-1,'pPl_C'], A, B, values)[0]
                    
                    CR.loc[i,'qGas_C'] = q
                    if CR.loc[i,'qGas_C'] < 0:
                        if pd.isnull(CR.loc[i,'Remark']):
                            CR.loc[i,'Remark']='Rem.'
                        warning =lng_tuple['ls_nreg_wrn']
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
                        warning = lng_tuple['ls_impos_wrn']+lng_tuple['ls_30dpr_wrn']
                        CR.loc[i,'Remark']=  warning+CR.loc[i,'Remark'] 
                        
                    CR.loc[i,'dpRob_C']=Dp
                    CR.loc[i,'qGas_C']=qDp.qGas_Dp(Dp, pl, A, B, values)
                    if CR.loc[i,'qGas_C'] < 0:
                        if pd.isnull(CR.loc[i,'Remark']):
                            if pd.isnull(CR.loc[i,'Remark']):
                                CR.loc[i,'Remark']='Rem.'
                        warning ="Режим закачки газа. "
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
                    if pd.isnull(CR.loc[i,'dpRob']):
                        warning =lng_tuple['ls_incorrect_wrn']+lng_tuple['ls_bhpr70_wrn']
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
                        warning = lng_tuple['ls_incorrect_wrn']+lng_tuple['ls_bhpr70_wrn']
                        CR.loc[i,'Remark']=  warning+CR.loc[i,'Remark'] 
                        
                    CR.loc[i,'dpRob_C'] = Dp
                    q = qDp.qGas_Dp(Dp, pl, A, B, values)
                    CR.loc[i,'qGas_C'] = q
                    if CR.loc[i,'qGas_C'] < 0:
                        if pd.isnull(CR.loc[i,'Remark']):
                            if pd.isnull(CR.loc[i,'Remark']):
                                CR.loc[i,'Remark']='Rem.'
                        warning ="Режим закачки газа. "
                        CR.loc[i,'Remark']=warning+CR.loc[i,'Remark']
                        
                    CR.loc[i,'pBottom_C'] = CD.loc[i-1,'pPl_C'] - CR.loc[i,'dpRob_C']                    
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
                        CR.loc[i,'pBottom']=0.7*CD.loc[i-1,'pPl_C']                          
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
        CD.loc[i,'Reserver_C']=(CD.loc[0,'Reserver_C']-
                            CD.loc[i,'QgasSum_C'])
        if CD.loc[i-1,'Reserver_C']<=0.00 or  CD.loc[i-1,'pPl_C']<=0.101325:
            R_flag = 0   # запасы исчерпаны
            if pd.isnull(CD.loc[i,'Remark']):
                CD.loc[i,'Remark']='Rem.'
            warning =lng_tuple['ls_exhaust_wrn']
            print(lng_tuple['ls_to_wrn'], CD.loc[i,'DateCalc'].strftime("%Y-%m-%d"),  lng_tuple['ls_exhaust_wrn'])
            rootLogger.info("To "+ CD.loc[i,'DateCalc'].strftime("%Y-%m-%d")+" gas reserves are exhausted!")
            CD.loc[i,'Remark']=warning+CD.loc[i,'Remark']
            # Остаточное пластовое давление при давлении на устье 0.101325 МПа
            prest = pz.p_zab(0, 0.101325, values)[0]
            CD.loc[i,'pPl_C'] = prest
            # Остаточные запасы
            rest =  rs.reserv_plast(prest, Ppl, Reserver, QwaterSum, Influx, Days, values)            
            CD.loc[i-1,'Reserver_C']=rest
            CD.loc[i,'Reserver_C']=rest
            CD.loc[i-1,'QgasSum_C']=CD.loc[0,'Reserver_C']-rest
            CD.loc[i,'QgasSum_C']=CD.loc[0,'Reserver_C']-rest

        ppp=ppl.GDW_p_plast(Ppl, Reserver, 
                CD.loc[i,'QgasSum_C'], CD.loc[i,'QwaterSum'],  
                CD.loc[i-1,'Influx_C'], CD.loc[i,'Days'],
                values)
        CD.loc[i,'pPl_C']= ppp[0]
        CD.loc[i,'Influx_C']=ppp[1]
        CD.loc[i,'pore_Volume_C']=pv.pore_volume( Reserver,  Ppl,  ppp[0], ppp[1], QwaterSum,  values) 
        CD.loc[i,"p-z_C"]=(CD.loc[i,'pPl_C']/
                            Z.zNew(CD.loc[i,'pPl_C'],values.loc[1],
                            values.loc[9],values.loc[10],values.loc[11],values.loc[12])[0])
        CD.loc[0,'P_mid']= CD.loc[0,'pPl_C']

        # Среднее за период пластовое давление
        for i in range(1,len(CD['pPl_C'])):        
            a=CD.loc[i-1,'pPl_C']
            b=CD.loc[i,'pPl_C']
            CD.loc[i,'P_mid']= (a+b)/2

    "Расчет добычи конденсата" 
    # if pd.isnull(CD.loc[strokFact-1,'QcondSum']):       
    #     print(lng_tuple['ls_n_cnd_wrn']) 
    #     warning =lng_tuple['ls_n_cnd_wrn']
    #     CD.loc[i,'Remark']='Rem.'
    #     CD.loc[i,'Remark']=  warning+CD.loc[i,'Remark']
    #     CD.loc[strokFact-1,'QcondSum']=0 
    # print(lng_tuple['ls_cnd_clc_wrn'])



    CndData = pd.DataFrame(columns = ['Pres','kgf', '','P_mid', 'QgasSum','QcondDif','QcondSum','KGF','a','b','c']) 
    
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
   
    for i in range(1,strokAll ):
        if CD.loc[i,'QgasDif_C']<0:
            CD.loc[i,'QgasDif_C'] = 0
        
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
    CD['DateCalc'] =np.array(CD['DateCalc'],dtype='datetime64[D]')
    cols=['Wellname','Method']
    # cols=['Wellname','Method','Weight','dateTest','ppl','SumQ_inputed','Intepolated','ppl/z','P_prognz','p/z','Q_all']
    WellTestData = pd.DataFrame(columns = cols)
    WellTestData.loc[2,'Wellname'] = 'Simple prognosis, no fact pressure data'
    cols=['RyadName',	'p/z fact',	'Q_all']
    pzData = pd.DataFrame(columns = cols)
    pzData.loc[2,'RyadName'] = 'Simple prognosis, no fact pressure data'
    return CD, WellTestData, pzData,  RegimeGroups, group_namelist,  CndData   



            

        