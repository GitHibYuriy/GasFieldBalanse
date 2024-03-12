# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 18:03:05 2022

@author: zarub

"""
""" Create a unique filename   """
import os

def out_file(LogFilePath):
    # print(LogFilePath)
    outdir = os.path.dirname(LogFilePath)    
    bas_name = os.path.basename(LogFilePath)
    
    if bas_name.count('out'):
       n = bas_name.find('out') 
       bas_name = bas_name[0: n-1]
    else:
       bas_name = bas_name[0: len(bas_name)-5] 
       
    outdir = os.path.dirname(LogFilePath)
    exist = outdir.count('Out_files')
    if exist:
        outdir = os.path.dirname(LogFilePath)
    else:
        outdir = os.path.dirname(LogFilePath)+('\Out_files')
        if not os.path.isdir(outdir):
          os.mkdir(outdir)
    i=0
    out_name = bas_name + '_out_' + str(i) + '.xlsx'
    outFile = outdir+str('/') + out_name
    while os.path.exists( outFile ):
        n = outFile.find('out') 
        outFile = outFile[0: n-1]
        i=i+1
        outFile =  outFile + '_out_' + str(i) + '.xlsx'
        
    return  outFile 





# LogFilePath ="D:\Phyton_MBE_exe\Project_Shablons\Out_files\Shablon_B.xlsm_out-0.xlsx"
# LogFilePath = "D:\Phyton_MBE_exe\Project_Shablons\Shablon_B.xlsm"
# LogFilePath = "D:\Phyton_MBE_exe\Project_Shablons\Out_files\Shablon_Kobz_3_grwell_out-0.xlsx"

# outFile = out_file(LogFilePath)
# print(LogFilePath)
# print('rez outfile is ',outFile)



