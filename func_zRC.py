
import numpy as np
def zNew(p,T,ro,H2S,Co2,N2):    
    erp = 0.000000001
     # Пересчет в мольные доли
    H2S = H2S / 100
    Co2 = Co2 / 100
    N2 = N2/ 100
    gr = ro* 1.2041
    mw = gr * 24.0551   
   
    mwCH = mw - 34.082 * H2S - 44.01 * Co2 - 28.01 * N2
    grCH = mwCH / 24.0551 / 1.2041
    PcCH = (48.10953 - 4.81224 * grCH + 0.49076 * grCH* grCH)
    TcCH = (77.67388 + 254.42917 * grCH - 85.62129 * grCH* grCH)
    PcCH = PcCH * (1 - H2S - Co2 - N2) + 9.185 * H2S + 72.8 * Co2 + 33.5 * N2
    TcCH = TcCH * (1 - H2S - Co2 - N2) + 126.2 * N2 + 304.2 * Co2 + 373.6 * H2S 
    AcCH = (-0.08109 + 0.18979 * grCH - 0.04919 *  grCH* grCH) 
    
    eps = 528 * AcCH * ((H2S + Co2) - (H2S + Co2) ** 2) + 5 * ((H2S) ** 0.5 - (H2S) ** 2)    
    PcCH = PcCH * (TcCH - eps) / (TcCH + H2S * (1 - H2S) * eps)
    Ppcr=PcCH * 0.10132501    
    Tpcr = TcCH - eps  
    Ac = AcCH * (1 - H2S - Co2 - N2) + 0.1 * H2S + 0.23 * Co2 + 0.04 * N2
    
    pr = p / Ppcr
    Tr = T / Tpcr  
    k = 0.48508 + 1.55171 * Ac - 0.15613 * Ac * Ac
    alf = Tr ** (-1.5)
    alf = (1 + k * (1 - (Tr) ** 0.5)) ** 2
    
    A = 0.42748 * pr / (Tr**2)* alf 
    B = 0.08664 * pr / Tr
    zLow = 0
    zUp = 4
    counter = 0
    z = zLow  
    F = z*z*z - z*z + (A - B * B - B) * z - A * B
    while abs(F) > erp  and counter<1000:  
        counter = counter + 1
        z = (zLow + zUp) / 2
        F = z*z*z - z*z + (A - B * B - B) * z - A * B
        if F < 0:
          zLow = z
        else:
          zUp = z
    z = (zUp + zLow) / 2

    return z, Ppcr, Tpcr, Ac

# rez = zNew(50,274,0.658,0.001,0.193,7.345)
# print(rez)