# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 08:21:12 2022

@author: zarub
"""

import pandas as pd

def global_parametr_name(lng_tuple):
    
   
    name = pd.DataFrame(columns=['Name','Dim'])    
    name.loc[0,'Name']=lng_tuple['ls_Depth']
    name.loc[1,'Name']=lng_tuple['ls_Tpplast']
    name.loc[2,'Name']=lng_tuple['ls_reserv_ini']
    name.loc[3,'Name']=lng_tuple['ls_p_ini']
    name.loc[4,'Name']=lng_tuple['ls_Q_ini']
    name.loc[5,'Name']=lng_tuple['ls_Vin']
    name.loc[6,'Name']=lng_tuple['ls_Water']
    name.loc[7,'Name']=lng_tuple['ls_Water_Poten']
    name.loc[8,'Name']=lng_tuple['ls_Water_Index']
    name.loc[9,'Name']=lng_tuple['ls_ro']
    name.loc[10,'Name']=lng_tuple['ls_H2S']
    name.loc[11,'Name']=lng_tuple['ls_CO2']
    name.loc[12,'Name']=lng_tuple['ls_N2']
    name.loc[13,'Name']=lng_tuple['ls_Pcr']
    name.loc[14,'Name']=lng_tuple['ls_Tcr']
    name.loc[15,'Name']=lng_tuple['ls_Ac']
    name.loc[16,'Name']=lng_tuple['ls_T_Head']
    name.loc[17,'Name']=lng_tuple['ls_d']
    name.loc[18,'Name']=lng_tuple['ls_Lmbd']
    name.loc[19,'Name']=lng_tuple['ls_K_expl']
    name.loc[20,'Name']=lng_tuple['ls_porisity']
    name.loc[21,'Name']=lng_tuple['ls_sat_water']
    name.loc[22,'Name']=lng_tuple['ls_bet_rock']
    name.loc[23,'Name']=lng_tuple['ls_bet_water']
    name.loc[24,'Name']=lng_tuple['ls_bet_all']
    name.loc[25,'Name']=lng_tuple['ls_pst']
    name.loc[26,'Name']=lng_tuple['ls_Tst']
    name.loc[27,'Name']=lng_tuple['ls_Influx']
    name.loc[28,'Name']=lng_tuple['ls_Condensat']
    name.loc[29,'Name']=lng_tuple['ls_BeginDate']
    name.loc[30,'Name']=lng_tuple['ls_AllGroups']
    
    name.loc[32,'Name']=lng_tuple['ls_iter']
    name.loc[33,'Name']=lng_tuple['ls_relax']
    

    name.loc[0,'Dim'] = 'm'
    name.loc[1,'Dim'] = 'K'
    name.loc[2,'Dim'] = 'mln.cub.m'
    name.loc[3,'Dim'] = 'MPa'
    name.loc[4,'Dim'] = 'mln.cub.m'
    name.loc[5,'Dim'] = 'mln.cub.m'
    name.loc[6,'Dim'] = 'mln.cub.m'
    name.loc[7,'Dim'] = 'mln.cub.m'
    name.loc[8,'Dim'] = 'mln.cub.m'
    name.loc[9,'Dim'] = 'mln.cub.m/(MPa∙d)'
    name.loc[10,'Dim'] = 'ND'
    name.loc[11,'Dim'] = '%'
    name.loc[12,'Dim'] = '%'
    name.loc[13,'Dim'] = '%'
    name.loc[14,'Dim'] = 'MPa'
    name.loc[15,'Dim'] = 'K'
    name.loc[16,'Dim'] = 'ND'
    name.loc[17,'Dim'] = 'K'
    name.loc[18,'Dim'] = 'sm'
    name.loc[19,'Dim'] = 'ND'
    name.loc[20,'Dim'] = 'ND'
    name.loc[21,'Dim'] = 'ND'
    name.loc[22,'Dim'] = 'ND'
    name.loc[23,'Dim'] = '1/MPa'
    name.loc[24,'Dim'] = '1/MPa'
    name.loc[25,'Dim'] = '1/MPa'
    name.loc[26,'Dim'] = 'MPa'
    name.loc[27,'Dim'] = 'K'
    name.loc[28,'Dim'] = 'mln.cub.m'
    name.loc[29,'Dim'] = 't'
    name.loc[30,'Dim'] = 'date'
    name.loc[32,'Dim']= 'times'
    name.loc[33,'Dim']=  'ND'

    
    return name
