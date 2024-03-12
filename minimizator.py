# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 10:57:08 2020

@author: zarub
"""



import datetime
import pandas as pd
import math
from scipy.stats import norm
import random
import logging
rootLogger = logging.getLogger(__name__)

# Импорт собственных модулей
# import prognosis_mid  as prg
import prognosis_Grups as prg
import func_zRC as Z

import control_Well_Test as gwt

import errorer_spline_ppl as err
import fun_dimRowdrop as dr
import global_lng as gln

def minimizator_res(LogFilePath,values,root,lng_tuple,k):
    # Оптимизация запасов методом деления отрезка пополам 
    ERR = pd.DataFrame ()
    X1 =  values.loc[2]
    tres = 100
    A=X1/k
    B=k*X1
    
    Fmin = err.errorer(LogFilePath,values,lng_tuple)[0]
    eps = X1/5000
    t = 0
    while (abs(A - B)) > 2.01*eps and t < tres:
        t=t+1
        # print('t=',t, ' A=', A, ' B=', B, ' A-B=', A-B   )
        C = (A + B) / 2
        X1 = C - eps
        X2 = C + eps
        values.loc[2] = X1
        F1 =  err.errorer(LogFilePath,values,lng_tuple)[0]
        values.loc[2] = X2
        F2 =  err.errorer(LogFilePath,values,lng_tuple)[0]
        # print('t=',t, ' A=', A, ' B=', B, ' A-B=', A-B, 'F1=',F1, 'F2=',F2   )
        if F2 > F1:
            B = C
            Fmin = F1
        else:
            A = C 
            Fmin = F2
        txt = str(str(t)+lng_tuple['ls_#iter_mnm']+" {:.5f}   ".format(Fmin))
        ERR.loc[t,"A"] = A
        ERR.loc[t,"RSMerr(A)"] = F1
        ERR.loc[t,"B"] = B
        ERR.loc[t,"B"] = F2
        ERR.loc[t,"A-B"]= A - B
        ERR.loc[t,"C=(A+B)/2"] = C
        ERR.loc[t,"min RSMerr"] = Fmin
        rootLogger.info(txt)
        root.update()
        print(txt)

    X1 = C
    print('mated iteration',t, X1, " mln. m3")  
    

    return X1, t, ERR          
            
            
    
def minimizator(LogFilePath,values,root,lng_tuple):


    t_begin = datetime.datetime.now()
   
    
    # glc.control_WellTestDatas(LogFilePath,lng_tuple)
    # WellTestDataSheet='WellTestData'
    # WellTestData = pd.read_excel(LogFilePath,WellTestDataSheet)
   
    CGF = pd.read_excel(LogFilePath,'CondFactor')
    # Удаление строки размерностей
    CGF = dr.dimRowdrop(CGF,'Pres' )
    X1 =  values.loc[2]
    # values.loc[5]=values.loc[2]-values.loc[4]
    X2 = values.loc[3]
    X3 =  values.loc[7]
    if X3<=0:
        X3 =  X1/X2/10
    X4 =  values.loc[8] 
    n = values.loc[32] 
    if  values.loc[32] < 1: 
        n=1
    else: 
        n = values.loc[32]
    M1  = values.loc[2]
    M2 = values.loc[3]
    M3= values.loc[7]
    M4 =  values.loc[8] 

    X10=X1
    X20=X2
    X30=X3
    X40=X4
    
    F2=0
    InRes=X1
    InPres=X2
    InPot=X3
    InProd=X4
    R = values.loc[33]

    # print('from minimizator to err line 75', LogFilePath,values)
    # Проверка наличия и содержания листа _WellTestDatas
    flag = gwt.control_WellTestDatas(LogFilePath,lng_tuple)
    ERR = pd.DataFrame ()
    
    if flag==0:
        # Ошибка апроксимации при начальных условиях
        Fmin = err.errorer(LogFilePath,values,lng_tuple)[0]
        Fminini=Fmin
        rootLogger.warning(lng_tuple['ls_rms_mnm']+"{:.3f}".format(Fminini)+" MPa" )
        
    else: 
        rootLogger.warning(lng_tuple['ls_rms_mnm']+"unnown" )
    # Проверка наличия и содержания листа _WellTestDatas
    
    if n < 2 or flag==1:
        rootLogger.warning(lng_tuple['ls_lst_mnm'])
        print(lng_tuple['ls_lst_mnm'])

        
    else:
        # Хотябы запасы оптимизируются
        if values.loc[34]==0 and values.loc[35]==0 and values.loc[36]==0  and values.loc[37]==0:
           values.loc[34]==1 
   
    if n >= 2: 
        
        a1 = values.loc[2]*0.7
        b1 = values.loc[2]*1.3
        a2 = values.loc[3]*0.9
        b2 = values.loc[3]*1.1
        
        if X3==0:
            a3 = values.loc[2]/values.loc[3]*0.1
            b3 = a3/2
        else:
            a3 = values.loc[7]*0.5
            b3 = values.loc[7]*1.5
            
            
        er1 = 0.001 * (a1 + b1) / 2
        er2 = 0.001 * (a2 + b2) / 2
        er3 = 0.001 * (a3 + b3) / 2
        er4 = 0.01
        M1 = X1
        M2 = X2
        M3 = X3
        M4 = X4
        Sig1 = abs(b1 - a1) / 3 
        Sig2 = abs(b2 - a2) / 3
        Sig3 = abs(b3 - a3) / 3
        Sig4 = 6
        # Sig4 = X4

        if values.loc[37]==1 and M4<=0:        
            M4 = math.exp(-Sig4*3)
            X4 = M4
        k=0 

        if  k < n and (values.loc[35] + values.loc[36] + values.loc[37])>0:
            # Сообщение об оптимизации модели методом Монте-Карло
            rootLogger.warning(lng_tuple['ls_mc_mnm'])
            rootLogger.warning(lng_tuple['ls_mc1_mnm'])
        
            rootLogger.warning(lng_tuple['ls_iter_mnm']+'  '+ str(n))
            if values.loc[34]==1:
                rootLogger.warning(lng_tuple['ls_res_mnm'])
            else: rootLogger.warning(lng_tuple['ls_nres_mnm'])            
            if values.loc[35]==1:
                            rootLogger.warning(lng_tuple['ls_pr_mnm'])
            else: rootLogger.warning(lng_tuple['ls_npr_mnm'])  
            
            if values.loc[36]==1:
                rootLogger.warning(lng_tuple['ls_pot_mnm'])
            else:        rootLogger.warning(lng_tuple['ls_npot_mnm'])
        
            if values.loc[37]==1:
                rootLogger.warning(lng_tuple['ls_pi_mnm'])
            else:
                rootLogger.warning(lng_tuple['ls_npi_mnm'])
            root.update()

        while k < n:
            if (values.loc[35] + values.loc[36] + values.loc[37])==0:
                # Оптимизация запасов методом деления отрезка пополам 
                rootLogger.warning('*********'+lng_tuple['ls_dichotomy optimization']+'*********')

                XX = minimizator_res(LogFilePath,values,root,lng_tuple, 1.5)
                X1= XX[0]
                values.loc[2] = X1
                n= XX[1]
                k=n
                F2 =  err.errorer(LogFilePath,values,lng_tuple)[0]
                ERR = XX[2]
            else:
                # Оптимизация модели методом Монте-Карло
                WellTestDataSheet='WellTestData'
                WellTestData = pd.read_excel(LogFilePath,WellTestDataSheet)
                k = k + 1
                tres = 100
               
                if values.loc[34]==1:                      # Для оптимизации запасов
                    # M1 = minimizator_res(LogFilePath,values,lng_tuple)[0]
                    X10=X1                                 # Предыдущее значение праметра
                    rx =random.random()
                    M1 = norm.ppf(rx, loc=X1, scale=Sig1)  # Текущее значение праметра
                    t=0
                    while M1 <= 0 and t < tres:            # Если проба привела к недопустимому значения праметра
                        rx =random.random()
                        M1 = norm.ppf(rx, loc=X1, scale=Sig1)
                        t=t+1
                    values.loc[2] = abs(M1)
                   
                    F2 =  err.errorer(LogFilePath,values,lng_tuple)[0] # Остаточная ошибка  после текущего выстрела
                    if F2 < Fmin:                          # Для успешного выстрела
                        X1 = M1                            # Новое значение праметра
                        Fmin = F2                          # Новое значение минимума остаточной ошибки 
                        if Sig1 > er1:
                            Sig1 = Sig1 / R                # Новое значение дисперпсии праметра
                    values.loc[2] =X1 
                    
                    
                ERR.loc[k,"old_X1"]=X10
                ERR.loc[k,"is_M1"]=M1
                ERR.loc[k,"next_X1"]=X1
                ERR.loc[k,"Sig_X1"]=Sig1
                ERR.loc[k,"is err1"]=F2
                ERR.loc[k,"min err1"]=Fmin
                
                if values.loc[35]==1:                     # Для оптимизации давления
                    X20=X2                                # Предыдущее значение праметра
                    rx =random.random()
                    M2 = norm.ppf(rx, loc=X2, scale=Sig2) # Текущее значение праметра
                    t=0
                    while M2 <= 0 and t < tres:           # Если проба привела к недопустимому значения праметра
                        rx =random.random()
                        M2 = norm.ppf(rx, loc=X2, scale=Sig2)
                        t=t+1
                    values.loc[3] = abs(M2)
                    F2 =  err.errorer(LogFilePath,values,lng_tuple)[0]     
                    if F2 < Fmin:                        # Для успешного выстрела
                        X2 = M2                          # Новое значение праметра
                        Fmin = F2                        # Новая величина минимума
                        if Sig2 > er2:
                            Sig2 = Sig2 / R              # Новое значение дисперпсии праметра
                    values.loc[3] = X2
                
                ERR.loc[k,"old_X2"]=X20
                ERR.loc[k,"is_M2"]=M2
                ERR.loc[k,"Next_X2"]=X2
                ERR.loc[k,"Sig_X2"]=Sig2
                ERR.loc[k,"is err2"]=F2
                ERR.loc[k,"min err2"]=Fmin
            
                if values.loc[36]==1:                   # Для оптимизации потенцила
                    X30=X3               
                    rx =random.random()
                    M3 = norm.ppf(rx, loc=X3, scale=Sig3)
                    t=0
                    while M3 <= 0 and t < tres:
                        rx =random.random()
                        M3 = norm.ppf(rx, loc=X3, scale=Sig3)
                        t=t+1
                    values.loc[7] = abs(M3)
                    F2 =  err.errorer(LogFilePath,values,lng_tuple)[0]
                
                    if F2 < Fmin :
                        X3 = M3
                        Fmin = F2
                        if Sig3 > er3:
                            Sig3 = Sig3 / R
                    values.loc[7] = X3 
                
                ERR.loc[k,"old_X3"]=X30
                ERR.loc[k,"is_M3"]=M3
                ERR.loc[k,"next_X3"]=X3
                ERR.loc[k,"Sig_X3"]=Sig3
                ERR.loc[k,"is err3"]=F2
                ERR.loc[k,"min err3"]=Fmin
                
                if values.loc[37]==1:                  # Для оптимизации индекса продуктивности
                    X40=X4
                    rx =random.random()
                    M4 = norm.ppf(rx, loc=math.log(X4), scale=Sig4)
                    M4 = math.exp(M4)
                    values.loc[8] = M4
                    F2 =  err.errorer(LogFilePath,values,lng_tuple)[0]     
                    if F2 < Fmin:
                        X4 = M4
                        Fmin = F2
                        if Sig4 > er4:
                            Sig4 = Sig4 / R 
                            
                    values.loc[8] = X4
                    
                ERR.loc[k,"old_X4"]=X40
                ERR.loc[k,"is_M4"]=M4
                ERR.loc[k,"next_M4"]=X4
                ERR.loc[k,"Sig_X4"]=Sig4
                ERR.loc[k,"is err4"]=F2
                ERR.loc[k,"min err4"]=Fmin
                
                ERR.loc[k,"err_min"]=Fmin
                
                
                values.loc[2] = X1
                values.loc[3] = X2
                values.loc[7] = X3
                values.loc[8] = X4
                values.loc[5] = values.loc[2] - values.loc[4]
                
                
                t_end = datetime.datetime.now()
                dt=(t_end-t_begin).seconds/k*(n-k)
                dth = dt // 3600
                dtm = (dt // 60) % 60
                dts = dt % 60
                txt = str(str(k)+lng_tuple['ls_#iter_mnm']+" {:.3f}   ".format(Fmin))
                txt = txt + lng_tuple['ls_remaining time']+"  = "  
                txt = (txt + "{:.0f}".format(dth)+ ' h ' + "{:.0f}".format(dtm)
                    + " min "+ "{:.0f}".format(dts) + ' s' ) 
                rootLogger.info(txt)
                print(txt)
                root.update()

    # Формирование фреймов с результатами моделирования
    
    CD, WellTestData, pzData, RegimeGroups, GroupList, CGF = prg.prognosis(LogFilePath,values,lng_tuple)
    CC = CD
    info ='  '
    info_r =''
    info_p =''
    info_v =''
    info_i =''
    if  (values.loc[34] +values.loc[35] + values.loc[36] + values.loc[37]) == 0:
        info = lng_tuple['ls_Simple production forecast without model matching']   
    if n < 2 :
        info = lng_tuple['ls_Simple production forecast without model matching']

    elif (values.loc[35] + values.loc[36] + values.loc[37]) == 0:
           info = lng_tuple['ls_Adaptation of the stocks of the model by the method of dichotomy']
    else:         
        if values.loc[34]:
            info_r = " "+lng_tuple['ls_reserv_ini']+", "
        if values.loc[35]:
            info_p = " "+lng_tuple['ls_p_ini']+", "
        if values.loc[36]:
            info_v = " "+lng_tuple['ls_Water_Poten']+", "
        if values.loc[37]:
            info_i =lng_tuple['ls_Water_Index']+", "

        info = info_r + info_p + info_v + info_i  
        info = lng_tuple['ls_Monte Carlo adapted'] + info 

    pzData.loc[0,'Info'] = info
   
    pzData.loc[1,'Info'] = lng_tuple['ls_iterations']+' = '+ str(n)
    info=str( "{:.3f}".format(values.loc[2]))
    
    pzData.loc[2,'Value'] = values.loc[2]
    pzData.loc[2,'Dimention'] = " mln.m.cub"
    pzData.loc[2,'Info'] = (lng_tuple['ls_reserv_ini']+'  '+ info +" mln.m.cub" )

    info=str( "{:.2f}".format(values.loc[3]))
    pzData.loc[3,'Info'] = str(lng_tuple['ls_p_ini'] +'  '+ info +" MPa")
    pzData.loc[3,'Value'] = values.loc[3]
    pzData.loc[3,'Dimention'] = " MPa"
    info=str( "{:.3f}".format(values.loc[7]))
    pzData.loc[4,'Info'] = (lng_tuple['ls_Water_Poten']+'  '+ info +" mln.m.cub")
    pzData.loc[4,'Value'] = values.loc[7]
    pzData.loc[4,'Dimention'] = " mln.m.cub"
    info=str( "{:.5e}".format(values.loc[8]))
    pzData.loc[5,'Info'] = (lng_tuple['ls_Water_Index']+ '  '+info +" mln.m.cub/(MPa*day)")
    pzData.loc[5,'Value'] = "{:.5e}".format(values.loc[8])
    # pzData.loc[5,'Value'] = values.loc[8]
    pzData.loc[5,'Dimention'] =" mln.m.cub/(MPa*day)"
    if flag==0:
        # При наличии  листа _WellTestDatas

        # Коэффициент детерминации R2        
        from statistics import mean
        import scipy.stats
        from sympy.stats import FisherZ
        Dyxx = 0
        Dyy = 0
        # Степени свободы для режиммов
        if values.loc[7] * values.loc[8] >0:
            M=4
        else:
            M=2
        
        
        N = len(WellTestData.index)
        my = mean(WellTestData['ppl'])
        for i in range(0,N):
            Dyxx = Dyxx +(WellTestData.loc[i,'ppl'] - WellTestData.loc[i,'P_prognz'])**2
            Dyx = Dyxx/(N-1)
            Dyy = Dyy +(WellTestData.loc[i,'ppl'] - my)**2
            Dy = Dyy/(N-M)
            
        R2 = 1 - Dyx/Dy
        # print('N=',N,'Dyxx=',Dyxx,'Dyy=',Dyy,'R2=',R2)
        # print('N=',N,'Dyx=',Dyx,'Dy=',Dy,'R2=',R2)
        # FisherFact = (R2/(1-R2))*(N-2)
        # # F7 = scipy.stats.f.ppf(0.05, N-2, N-2)
        # # F8 = scipy.stats.f.ppf(0.975, N-2, N-2)
        F9 = scipy.stats.f.ppf(0.95, N-M, N-M)
        # print('FisherFact',FisherFact)
       
        # print('Fisher 0.95Z',F9)
        
        R2cr = F9/(1+ F9*(N-1)/(N-M))

        # print('R2',R2)
        # print('R2cr ',R2cr )

        info=str( "{:.4f}".format(Fminini))
        pzData.loc[6,'Info'] = (lng_tuple['ls_ini_rms']+'  '+ info +" MPa")
        pzData.loc[6,'Value'] =Fminini
        pzData.loc[6,'Dimention'] = " MPa"

        F2 =  err.errorer(LogFilePath,values,lng_tuple)[0]

        info=str( "{:.4f}".format(Fmin))
        pzData.loc[7,'Info'] = (lng_tuple['ls_rs_rms']+'  '+ info +" MPa")
        pzData.loc[7,'Value'] = Fmin
        pzData.loc[7,'Dimention'] = " MPa"

        info=str( "{:.4f}".format(R2))
        pzData.loc[8,'Info'] = (lng_tuple['ls_R2']+'  '+ info )
        info=str( "{:.4f}".format(R2cr))
        pzData.loc[9,'Info'] = (lng_tuple['ls_R2cr']+'  '+ info )
        if R2 >= R2cr:
            pzData.loc[10,'Info'] = (lng_tuple['ls_reliable'] )
        else:
            pzData.loc[10,'Info'] = (lng_tuple['ls_unreliable'] )
    
    # Формирование фрейма GlobalData
    GlobalDataIni = pd.read_excel(LogFilePath,'Globals')
    
    GlobalData = pd.DataFrame(columns = ['Parametr','Dimensions','Initial values',
    	'values'])
    name =  gln.global_parametr_name(lng_tuple)
    GlobalData['Parametr'] = name['Name']
    GlobalData['Dimensions'] = name['Dim']

    values_ini = GlobalDataIni['values']
    GlobalData.loc[2,'Initial values'] =  values_ini.loc[2]
    GlobalData.loc[3,'Initial values'] =  values_ini.loc[3] 
    GlobalData.loc[4,'Initial values'] =  values_ini.loc[4]
    GlobalData.loc[5,'Initial values'] =  values_ini.loc[5]
    GlobalData.loc[6,'Initial values'] =  values_ini.loc[6]
    GlobalData.loc[7,'Initial values'] =  values_ini.loc[7]
    GlobalData.loc[8,'Initial values'] =  values_ini.loc[8]
    
    GlobalData['values'] = GlobalDataIni['values']
    GlobalData.loc[2,'values'] = values.loc[2]
    GlobalData.loc[3,'values'] = values.loc[3]
    GlobalData.loc[4,'values'] = values.loc[4]
    GlobalData.loc[5,'values'] = values.loc[5]
    GlobalData.loc[7,'values'] = values.loc[7]
    GlobalData.loc[8,'values'] = values.loc[8]
    GlobalData.loc[30,'values'] = values.loc[30]
    GlobalData.loc[32,'values'] = n
    GlobalData.loc[33,'values'] = R

        
    Tp = values.loc[1]
    ro=values.loc[9]

    H2S=values.loc[10]
    Co2=values.loc[11]
    N2=values.loc[12]
    
    GlobalData.loc[13,'values'] = Z.zNew(values.loc[3], Tp, ro, H2S, Co2, N2)[1]
    GlobalData.loc[14,'values'] = Z.zNew(values.loc[3], Tp, ro, H2S, Co2, N2)[2]
    GlobalData.loc[15,'values'] = Z.zNew(values.loc[3], Tp, ro, H2S, Co2, N2)[3]
    

    name =  gln.global_parametr_name(lng_tuple)
    GlobalData['Parametr'] = name['Name']
    GlobalData['Dimensions'] = name['Dim']
    
    
   
    t_end = datetime.datetime.now()
    
    print("*******************  "+lng_tuple['ls_simResult']+"    *******************") 
    print(lng_tuple['ls_reserv_ini'], "{:.3f}".format(values.loc[2])," mln.m.cub" )
    print(lng_tuple['ls_p_ini'], "{:.3f}".format(values.loc[3])," MPa" )
    print(lng_tuple['ls_Water_Poten'], "{:.3f}".format(values.loc[7])," mln.m.cub" )
    
    if flag==0:
        print(lng_tuple['ls_ini_rms'], "{:.3f}".format(Fminini), " MPa")
        print(lng_tuple['ls_rs_rms'], "{:.3f}".format(F2), " MPa")
        print(lng_tuple['ls_R2'], "{:.4f}".format(R2))
        
    if (t_end-t_begin).seconds < 60:
        print("time = ", "%.2s" % ((t_end-t_begin).seconds), " s;  " + lng_tuple['ls_iterations']+' = ', str(n))
    else:
        print("time = ", "%.4s" % ((t_end-t_begin).seconds/60), " min;  " + lng_tuple['ls_iterations']+' = ' , str(n))
    print( "Initial = ", "{:.2f}; {:.3f}; {:.3f}; {:.4e}"
          .format(InRes, InPres, InPot,  InProd))
    if flag==0:
        print( "Finish =", "{:.2f}; {:.3f}; {:.3f}; {:.4e}; {:.4f}; {:.2f}"
          .format(values.loc[2], values.loc[3], values.loc[7],  values.loc[8], Fmin, R))
  
    print("==================================================================  \n\a") 
    rootLogger.info("\n\a*******************  "+lng_tuple['ls_simResult']+"   *******************") 
    rootLogger.info(lng_tuple['ls_reserv_ini']+"{:.3f}".format(values.loc[2])+" mln.m.cub" )
    rootLogger.info(lng_tuple['ls_p_ini']+ "{:.3f}".format(values.loc[3])+" MPa" )
    rootLogger.info(lng_tuple['ls_Water_Poten']+ "{:.3f}".format(values.loc[7])+" mln.m.cub" )
    rootLogger.info(lng_tuple['ls_Water_Index']+ "{:.5e}".format(values.loc[8])+" mln.m.cub/(MPa*day)" )
    if flag==0:
        rootLogger.info(lng_tuple['ls_ini_rms']+"{:.3f}".format(Fminini)+" MPa" )
        rootLogger.info(lng_tuple['ls_rs_rms']+"{:.3f}".format(F2)+" MPa" )
        rootLogger.info(lng_tuple['ls_R2']+"{:.4f}".format(R2) ) 
        
    if (t_end-t_begin).seconds < 60:
        {rootLogger.info(lng_tuple['ls_simDuration'] +  " = "+ 
            "%.2s" % ((t_end-t_begin).seconds)+" s;   "
            + lng_tuple['ls_iterations']+' = '+ str(n))}
    else:
        {rootLogger.info(lng_tuple['ls_simDuration'] +  " = "+ 
            "%.2s" % ((t_end-t_begin).seconds/60)+" min;   "
            + lng_tuple['ls_iterations']+' = '+ str(n))}
    rootLogger.info( lng_tuple['ls_Initial values'] +  " = "+ "{:.2f}; {:.3f}; {:.3f}; {:.4e}"
         .format(InRes, InPres, InPot,  InProd))
    rootLogger.info( lng_tuple['ls_Finish values'] +  " = "+ "{:.2f}; {:.3f}; {:.3f}; {:.4e}"
     .format(values.loc[2], values.loc[3], values.loc[7],  values.loc[8]))
    
    rootLogger.info("********************************* End *********************************")  
   
    if n<2:
        ERR = pd.DataFrame (columns = ['Shots', 'Info',' '])
        ERR.loc[3,'Info'] = 'The model has not been adapted'
  
    return  GlobalData, CC, WellTestData, pzData, CGF, ERR, GroupList, RegimeGroups, ERR 



