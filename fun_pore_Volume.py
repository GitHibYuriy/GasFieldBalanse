# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 18:13:08 2020

@author: zarub


"""

import pandas as pd
import math

"""Импорт собственных модулей"""

import func_zRC as Z
import func_WaterVolumeFactor as wvf



def pore_volume( res_ini,  p_ini, p_pl, influx, QwaterSum,  values):  
    
    
    Ppl0 = p_ini                             
    Tp = values[1]                           
    Vin=res_ini
    Water =  QwaterSum                      
    wvf.WVF( Ppl0,Tp)
    Water = Water * wvf.WVF( Ppl0,Tp)      
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
    Vporini = Vin * Z0 * Tp * pst / Zst / Tst / Ppl0    
    D_PorVolume = Vporini * ComprPor * (p_ini - p_pl)
    PoreVolume = Vporini - influx +  Water - D_PorVolume     
    return PoreVolume
  
    
    
    