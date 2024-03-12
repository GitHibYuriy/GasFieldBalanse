# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 16:59:13 2020

@author: zarub
"""

import pandas as pd
import numpy as np
import math

"""Импорт собственных модулей"""

import func_zRC as Z


def p_zab(qGas, pHead, values): 
    errp = 0.00001
    Q = qGas                
    Ty = values.loc[16]
    L = values.loc[0]
    Tp = values.loc[1]    
    ro=values.loc[9]
    H2S=values.loc[10]
    Co2=values.loc[11]
    N2=values.loc[12]        
    lbd = values.loc[18]
    D = values.loc[17] 
    py=pHead 
    
    if py <= 0:
        py = 0.1
  
    aprox1 = 1 * py
    Tm = (Tp - Ty) / math.log(Tp / Ty)
    pm = 2 / 3 * (aprox1 + py **2 / (aprox1 + py))  
    z=Z.zNew(pm, Tm, ro, H2S, Co2, N2)[0]

    pex = math.exp(0.03415 * 2 * ro * L / Tm / z)
    tet = 0.013225 * lbd * Tm ** 2 * z ** 2 / (D ** 5)    
    aprox2 = (py ** 2 * pex + tet * Q ** 2 * (pex - 1)*np.sign(Q))**0.5
    aprox2=3*aprox1
    counter = 0     
    while abs(aprox1 - aprox2) > errp and counter < 1000:
        counter = counter + 1
        aprox1 = aprox2
        pm = 2 / 3 * (aprox1 + py **2 / (aprox1 + py))
        z=Z.zNew(pm, Tm, ro, H2S, Co2, N2)[0]
        pex = math.exp(0.03415 * 2 * ro * L / Tm / z)
        tet = 0.013225 * lbd * Tm ** 2 * z ** 2 / (D ** 5)
        aprox2 = (py ** 2 * pex + tet * Q ** 2 * (pex - 1)*np.sign(Q))**0.5 
         
    pBottom = ((aprox1 + aprox2) / 2)
    return pBottom, counter