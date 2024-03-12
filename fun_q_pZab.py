# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 06:48:05 2020

@author: zarub
"""

import pandas as pd
import math
import numpy as np
"""Импорт собственных модулей"""
import func_zRC as Z
import fun_pZab_Phead as pz

def qGas_Bt( pBottom, pPl, A, B, values):
    c = pPl*pPl-pBottom*pBottom

    det = A * A - 4 * B * c
    
    if det < 0: 
        q = 0
    else: 
     if B == 0:
        q =  (c/A)
     else: 
        q=(-A + (A * A + 4 * B*np.sign(c) * c) ** 0.5)*np.sign(c) / 2 / B 
    return q