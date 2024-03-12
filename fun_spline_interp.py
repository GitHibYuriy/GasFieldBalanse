# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 09:07:17 2020

@author: zarub
"""

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt


def splineMykub(x,y,xnew):
        clmn={'x':[],'y':[], 'h':[],'Lm':[],'Dl':[],'Lb':[],'b':[],'c':[], 'd':[]}
        spl=pd.DataFrame(clmn)
        
        spl['x']=x
        spl['y']=y
        N=len(x)
        for k in range(1,N):
            spl.loc[k,'h']=spl.loc[k,'x']-spl.loc[k-1,'x']
        spl=spl.drop(spl[spl.h==0].index) 
        spl=spl.reset_index()
        spl=spl.drop(['index'],axis=1)
        N=len(spl)
        for k in range(1,N):
            spl.loc[k,'Lm']=(spl.loc[k,'y'] - spl.loc[k-1,'y'])/(spl.loc[k,'h'])
        
        spl.loc[1,'Dl']=-spl.loc[2,'h']/(2*(spl.loc[1,'h']+spl.loc[2,'h']))
        spl.loc[1,'Lb']=1.5*(spl.loc[2,'Lm']-spl.loc[1,'Lm'])/(spl.loc[1,'h']+spl.loc[2,'h'])
        for k in range(3,N): 
            spl.loc[k-1,'Dl'] = (-spl.loc[k,'h']/(2*spl.loc[k-1,'h']+
                                    2*spl.loc[k,'h'] + spl.loc[k-1,'h']*spl.loc[k-2,'Dl']))
            spl.loc[k-1,'Lb']=((3*spl.loc[k,'Lm'] -3*spl.loc[k-1,'Lm'] 
                                  -spl.loc[k-1,'h']*spl.loc[k-2,'Lb'])/
                                  (2*spl.loc[k-1,'h']+2*spl.loc[k,'h']+
                                   spl.loc[k-1,'h']*spl.loc[k-2,'Dl']))
        spl.loc[:0,'c']= 0
        spl.loc[:0,'b']= 0
        spl.loc[:0,'d']= 0
        spl.loc[:N,'c']= 0
        for k in range(N-1,1,-1):  
            spl.loc[k-1,'c']=spl.loc[k-1,'Dl']*spl.loc[k,'c']+spl.loc[k-1,'Lb']
              
        for k in range(1,N): 
            spl.loc[k,'d']=(spl.loc[k,'c']-spl.loc[k-1,'c'])/3/spl.loc[k,'h']
            spl.loc[k,'b']=(spl.loc[k,'Lm']+(2*spl.loc[k,'c']*spl.loc[k,'h']
                            +spl.loc[k-1,'c']*spl.loc[k,'h'])/3)
        clmn={'ynew':[],'xnew':[],'splNod':[]}
        res=pd.DataFrame(clmn)               
        res['xnew']=xnew
        for i in range (0,len(res)):
            for k in range (0,len(spl)):
                if res.loc[i,'xnew']<=spl.loc[k,'x']:
                    res.loc[i,'splNod']=k
                    break
            m=res.loc[i,'splNod']
            
            res.loc[i,'ynew']=(spl.loc[m,'y'] + spl.loc[m,'b']*(xnew[i]-spl.loc[m,'x'])+spl.loc[m,'c']*(xnew[i]-spl.loc[m,'x'])**2 +spl.loc[m,'d']*(xnew[i]-spl.loc[m,'x'])**3)
        return(res['ynew'])     

       
        
                
