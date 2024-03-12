# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:13:48 2020

@author: zarub
"""
def WVF(p,T): 
    T = T - 273.15 
       
    Bwt = -5.1696E-3 + 3.03539E-4 * T + 1.78412E-6 * T ** 2
    Bwp = (-6.113171E-5 * p - 4.856604E-6 * p ** 2- 
           5.098683E-7 * p * T - 6.544308E-9 * p ** 2 * T)
    wvf = (1 + Bwt) * (1 + Bwp)  

    return wvf