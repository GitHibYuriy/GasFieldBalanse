# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 16:59:13 2020

@author: zarub
"""



import math
import pandas as pd
"""Импорт собственных модулей"""
import func_zRC as Z
import func_WaterVolumeFactor as wvf

def reserv_plast(p, Ppl, Reserver, QwaterSum, Influx, Days, values): 
    Tp = values[1]
    Ppl0 = Ppl                             
    Vin=Reserver                             
                                 
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
    # pWater = p_ini * (1 - Wet / Wein)
    # Ind = J * p_ini / Wein
    Z0=Z.zNew(Ppl0, Tp, ro, H2S, Co2, N2)[0]
    Zst =Z.zNew(pst, Tst, ro, H2S, Co2, N2)[0]
    z = Z.zNew(p, Tst, ro, H2S, Co2, N2)[0]
    Vporini = Vin * Z0 * Tp * pst / Zst / Tst / Ppl0
    WaterInVolume = Vporini * Swater / (1 - Swater) 
    D_WaterVolume = WaterInVolume * ComprWater * (p_ini - p)
    
    D_PorVolume = Vporini * ComprPor * (p_ini - p)
    # PorVolume = (Vporini - D_WaterVolume - D_PorVolume -
    #         (Wet + Wein / p_ini * (pWater - p) * 
    #         (1 - math.exp(-Ind * WorkingDays))) + Water)
    PorVolume = (Vporini - D_WaterVolume - D_PorVolume -Influx
             + Water)
    reserv =  p / pst * Zst / z * Tst / Tp * PorVolume
    
    
    return  reserv 

""" EXEMPELS """

# LogFilePath="D:\Base_Level\Гадяцке\MBE\Shablon_Gadych_B-16_exhaust.xlsm"
# import func_zRC as Z
# GlobalDataSheet='Globals'
# GlobalData = pd.read_excel(LogFilePath,GlobalDataSheet)

# values=GlobalData['values']
# Ppl= values[3]
# Reserver= values[2]
# Influx=8.413242329
# QwaterSum = 0
# QwaterSum = 0.0124461

# # Influx =0
# p = 0.14
# print(Ppl,Reserver)
# res = reserv_plast(Ppl, Ppl, Reserver, QwaterSum, 0,  0, values)
# resres = reserv_plast(p, Ppl, Reserver,  QwaterSum, Influx,  0, values)


# print('res',res,resres) 

# QgasSum = Reserver - res
# import fun_ppl as ppl
# pp = ppl.GDW_p_plast(Ppl, Reserver, 0, 0, 0, 0, values)[0] 
# ppres = ppl.GDW_p_plast(Ppl, Reserver, Reserver-resres, Influx, 0, 0, values)[0] 
# print(pp,ppres) 
  