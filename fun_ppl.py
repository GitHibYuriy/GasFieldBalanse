# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 16:59:13 2020

@author: zarub
"""



import math

"""Импорт собственных модулей"""
import func_zRC as Z
import func_WaterVolumeFactor as wvf

def GDW_p_plast(Ppl, Reserver, QgasSum, QwaterSum, Influx, Days,                
                values): 
   
    Ppl0 = Ppl                                
    Tp = values[1]                            
    Vin=Reserver                             
    Q = QgasSum                              
    Water =  QwaterSum 
    Water = Water * wvf.WVF( Ppl0,Tp)    
    Wet = Influx                               
    WorkingDays = Days                        
    
    p_ini = values[3]
    Wein = values[7]
    J = values[8]
    Swater = values[21]
    ComprWater = values[23]
    ComprPor = values[22]
    pst=values[25]
    Tst=values[26]
    ro=values[9]
    H2S=values[10]
    Co2=values[11]
    N2=values[12]
    Z0=Z.zNew(Ppl0, Tp, ro, H2S, Co2, N2)[0]
    Zst =Z.zNew(pst, Tst, ro, H2S, Co2, N2)[0]
    Vporini = Vin * Z0 * Tp * pst / Zst / Tst / p_ini
    WaterInVolume = Vporini * Swater    
    Aa = p_ini / Z0 / Tp * Vporini - pst / Zst / Tst * Q
    pLow = 0.1
    pUp = p_ini*100
    counter = 0
    Fp=pUp /  Tp * Vporini
    Influx = Wet
    
    if Wein <= 0 or J <= 0:
        Wet = 0
        J = 0
        pWater = p_ini
        Ind = 0
    else:
        Ind = J * p_ini / Wein
        
        
    while abs(pLow - pUp) > 0.001 and counter<100:
        counter = counter + 1 
        p = (pLow + pUp) / 2 
        pWater = p_ini * (1 - Influx / Wein)  
        Influx =  (Wet +Wein / p_ini * (pWater - p) * 
                    (1 - math.exp(-Ind * WorkingDays)))
        z =Z.zNew(p, Tp, ro, H2S, Co2, N2)[0]  
        D_WaterVolume = WaterInVolume * ComprWater * (p_ini - p)
        D_PorVolume = Vporini * ComprPor * (p_ini - p)        
        Fp =    p / z / Tp * (Vporini - D_WaterVolume - D_PorVolume -  Influx  + Water) - Aa 
        if Fp < 0:
          pLow = p
        else:
          pUp = p
        pPl = (pLow + pUp) / 2 
        
        
    return pPl,  Influx, counter , pLow , pUp, z


# exempl
# import pandas as pd
# LogFilePath = "D:\Phyton_MBE_exe\MBE PyProjects\Перещепинское\Pereschepinske_C-4.xlsm"
# data_values = pd.read_excel(LogFilePath,'Globals')
# values = data_values['values']
# 'Ppl, Reserver, QgasSum, QwaterSum, Influx, Days,'
# resA = GDW_p_plast(22.4, 1963.218, 1225.3, 0, 2.864, 9676,  values)
# resB = GDW_p_plast(22.4, 1963.218, 1225.3, 0, 0, 9676,  values)
# print(resA) 
# # print(resB)