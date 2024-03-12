

import pandas as pd
import logging
rootLogger = logging.getLogger(__name__)

def fitting(cond,lng_tuple):
    data = pd.DataFrame(columns=['P_mid','Pres']) 
    data['P_mid'] = cond['Pres']
    data['kgf'] = cond['kgf']    
    x = data['P_mid']
    y = data['kgf']
    n = len(data)
   
    # Система коэффициентов  МНК для квадратного уравненя
    a1 = sum(x**4)
    a2 = sum(x**3)
    a3 = sum(x**2)
    b1 = a2
    b2 = a3 
    b3 = sum(x)
    c1 = a3
    c2 = b3
    c3 = n 
    
    d1 = sum(x**2*y)
    d2 = sum(x*y)
    d3 =sum(y)

    mx = b3/n
    my = d3/n    
    vary=sum((y - my)**2)/n
    print('vary',vary)
    if vary==0:
       a = 0
       b = 0
       c = 0
       R2p = 0 
       al = 0
       bl = 0
       R2l = 0
       
    else:   
       
        # Детерминанты и коэффициенты для параболы
        det = a1*b2*c3 -a1 * b3*c2 - a2*b1*c3 + b1*c2*a3  + a2*b3*c1  - a3*b2*c1
        det1 = d1*b2*c3 -d1 * b3*c2 - d2*b1*c3 + b1*c2*d3  + d2*b3*c1  - d3*b2*c1
        det2 = a1*d2*c3 -a1 * d3*c2 - a2*d1*c3 + d1*c2*a3  + a2*d3*c1  - a3*d2*c1
        det3 = a1*b2*d3 -a1 * b3*d2 - a2*b1*d3 + b1*d2*a3  + a2*b3*d1  - a3*b2*d1
        a = det1 / det
        b = det2 / det
        c = det3 / det
        
        y_fit2 = a*x*x + b*x + c
        residial2 = sum((y - y_fit2)**2)/n
        R2p = 1 -  residial2/vary
        # fit2 = [a, b, c, R2p]
       
        # Детерминанты и коэффициенты для прямой 
        al = sum((x-mx)*(y-my))/sum((x-mx)**2)
        bl = my - al*mx
        
        y_fit1 =  al*x + bl
        residial1 = sum((y - y_fit1)**2)/n
        R2l = 1 -  residial1/vary
        # fit1 = [ al, bl, R2l]
        
        print(lng_tuple['ls_aprox_r2'].format(R2l,R2p))
        rootLogger.warning(lng_tuple['ls_aprox_r2'].format(R2l,R2p))
        
        # Проверка физической содержательности аппроксимаций
        if R2p>R2l and a > 0 and (4*a*c - b*b ) > 0:
            print(lng_tuple['ls_aprox_parabola'])
            rootLogger.warning(lng_tuple['ls_aprox_parabola'])

        if R2l>=R2p or a < 0 or (4*a*c - b*b ) < 0  and b + c > 0:
            print(lng_tuple['ls_aprox_linear'])
            rootLogger.warning(lng_tuple['ls_aprox_linear'])
            a=0
            b=al
            c=bl
        if R2l>=R2p or a < 0 or (4*a*c - b*b ) and b + c < 0:
            a=0
            b=0
            c =  d3/n
            print(lng_tuple['ls_aprox_poor'])
            rootLogger.warning(lng_tuple['ls_aprox_poor'])
       
        rootLogger.warning( "GCF = {:.5f} * p^2 + {:.5f} * p + {:.5f} g/m3".format(a, b, c))
   
    return a,b,c


