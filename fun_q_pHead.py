# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 06:48:05 2020

@author: zarub
"""


import math
import numpy as np
"""Импорт собственных модулей"""

import func_zRC as Z
import fun_pZab_Phead as pz


def qGas( pHead, pPl, A, B, values):
   
    Ty = values.loc[16]    
    Tp = values.loc[1]
    ro=values.loc[9]
    H2S=values.loc[10]
    Co2=values.loc[11]
    N2=values.loc[12]
    
    L=values.loc[0]
    D=values.loc[17]
    lbd=values.loc[18]
    
    Ppl=pPl
    py=pHead
    if py < 0.101325:
        py = 0.101325
    p = 0.101325
    Tm = (Tp - Ty) / math.log(Tp / Ty) 
    pm  = 2 / 3 * (p + py **2 / (p + py)) 
    z=Z.zNew(pm, Tm, ro, H2S, Co2, N2)[0]
    pex = math.exp(0.0683 * ro * L / Tm / z)
    tet = 0.013225 * lbd * Tm ** 2 * z ** 2 / (D ** 5)
    QLow=-((py**2*pex-0.101325**2)/tet/(pex-1))**0.5
    p = pPl
    Tm = (Tp - Ty) / math.log(Tp / Ty) 
    pm = 2 / 3 * (p + py **2 / (p + py)) 
    z=Z.zNew(pm, Tm, ro, H2S, Co2, N2)[0]
    pex = math.exp(0.0683 * ro * L / Tm / z)
    tet = 0.013225 * lbd * Tm ** 2 * z ** 2 / (D ** 5)
    det=(pPl**2-py**2*pex)/tet*(pex-1)    
    QUp=((pPl**2-py**2*pex)/tet*(pex-1)*np.sign(det))**0.5    
  
    eps=0.00000001
    k=0
    F=1
    k = 0  
    
    while abs(QUp - QLow) > eps :
        k=k+1
        Q=(QUp + QLow )/2
        
        pzz=pz.p_zab(Q, py, values)[0]
        
        F=B*Q**2*np.sign(Q)+A*Q - (Ppl*Ppl - pzz**2)
    
    
        if F < 0:
          QLow = Q
        else:
          QUp = Q
    q=Q
    return q,k