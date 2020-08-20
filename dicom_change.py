import pydicom
import pandas as pd
import os
import xlrd
import multiprocessing as mp
from multiprocessing import Pool
import numpy as np
import math
import time



def scan_root_dir():
    data_dirs = []
    for item in os.listdir('.'):
        if (os.path.isdir(item)):
            if (item[:1] != '.'):
                data_dirs.append(os.path.abspath(os.path.join(os.getcwd(), item)))
    return data_dirs

def cover_Field(data_array):
    ds = pydicom.dcmread(data_array[0]+'/'+data_array[2], force=True)
    try:
        PatientID  = ds['PatientID'].value
    except:
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(data_array[0]+'/'+str(data_array[2])+" not have PatientID"+"\n")
        return [data_array[0]+'/'+data_array[2]+" not have PatientID","not ok"]
    
    try:
        PatientName  = ds['PatientName'].value
    except:
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(data_array[0]+'/'+str(data_array[2])+" not have PatientName"+"\n")
        return [data_array[0]+'/'+data_array[2]+" not have PatientName","not ok"]
    
    for name in os.listdir():
        if name[-4:] == 'xlsx':
            read = pd.read_excel(name,dtype=object)#.astype('object')
            book = xlrd.open_workbook(name)
            sheel = book.sheet_by_index(0)
            field = sheel.row_values(0)
            break
    
    if PatientID =='Unknown':
        ds['PatientID'].value = data_array[1]
        ds['PatientName'].value = data_array[1]

    elif PatientID =='':
        number = data_array[1].find('_')
        ds['PatientID'].value = data_array[1][:number]
        ds['PatientName'].value = data_array[1][:number]+"^AI99"
    
    elif str(PatientName).find(PatientID) > 0:
        ds['PatientName'].value = ds['PatientID'].value+"^AI99"
    
    
    else:
        try:
            change = read[read['raw']==ds['PatientID'].value]
            if change.empty:
                read2 = read.applymap(str)
                change = read[read2['raw']==ds['PatientID'].value]
                if change.empty:
                    with open('log.txt', 'a', encoding='utf-8') as f:
                        f.write(data_array[0]+'/'+data_array[2]+" PatientID not in excel-1"+"\n")
                    return [data_array[0]+'/'+data_array[2]+" not have PatientID","not ok"]
                        
        except:
            read2 = read.applymap(str)
            change = read[read2['raw']==ds['PatientID'].value]
            if change.empty:
                with open('log.txt', 'a', encoding='utf-8') as f:
                    f.write(data_array[0]+'/'+data_array[2]+" PatientID not in excel-2"+"\n")
                return [data_array[0]+'/'+data_array[2]+" not have PatientID","not ok"]
        #change = read[read['raw']==ds['PatientID'].value].to_numpy()[0][1:3]
    
        
        if pd.isnull(change[field[1]]).bool() != True:
            ds['PatientID'].value = change[field[1]].values[0]
            
        if pd.isnull(change[field[2]]).bool() != True:
            ds['PatientName'].value = str(change[field[2]].values[0])
    #change = read[read['raw'] == ds['PatientID'].value].to_numpy()[0][:] 
    
    try:
        change1 = read[read['PatientID']==ds['PatientID'].value]
        if change1.empty:
            read2 = read.applymap(str)
            change1 = read[read2['PatientID']==ds['PatientID'].value]
            if change1.empty:
                with open('log.txt', 'a', encoding='utf-8') as f:
                    f.write(data_array[0]+'/'+data_array[2]+" PatientID not in excel-3"+"\n")
                return [data_array[0]+'/'+data_array[2]+" not have PatientID","not ok"]
                        
    except:
        read2 = read.applymap(str)
        change1 = read[read2['PatientID']==ds['PatientID'].value]
        if change1.empty:
            with open('log.txt', 'a', encoding='utf-8') as f:
                f.write(data_array[0]+'/'+data_array[2]+" PatientID not in excel-4"+"\n")
            return [data_array[0]+'/'+data_array[2]+" not have PatientID","not ok"]
    
    
    
    for i in range(2,len(field)): 
        if pd.isnull(change1[field[i]]).bool() !=True:
            '''
            if type(change1[field[i]].values[0]) == type('float'):
                try:
                    change1[field[i]] = int(change1[field[i]])
                except:
                    pass
            '''
            try:
                ds[field[i]].value = str(change1[field[i]].values[0])
            except Exception as e:
                with open('log.txt', 'a', encoding='utf-8') as f:
                    #f.write(str(change[field[i]])+" "+str(ds['PatientID'].value)+str(e)+"\n")
                    f.write(data_array[0]+'/'+str(data_array[2])+" not have "+str(field[i])+"\n")
                pass
    
    ds.save_as(data_array[0]+'/'+data_array[2])
    return [data_array[0]+'/'+data_array[2]+" ok","ok"]
        
    
            
            

if __name__ == "__main__" :
    '''
    for name in os.listdir():
        if name[-4:] == 'xlsx':
            read = pd.read_excel(name,dtype=object)#.astype('object')
            read2 = read.applymap(str)
            print(read)
            book = xlrd.open_workbook(name)
            sheel = book.sheet_by_index(0)
            field = sheel.row_values(0)
            print(field)
            break
    name ="0001171021"
    try:
        change = read[read['raw']==name]
        if change.empty:
            change = read[read2['raw']==name]
    except:
        change = read[read2['raw']==name]
    #change['StudyID'] =int(change['StudyID'])
    print(change)
    print(change['PatientID'].values[0])
    print(type(change['PatientName'].values[0]) == type('float'))
    '''
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
    
    data_dirs = scan_root_dir()
    data_dir = data_dirs[0]
    
    dir_and_folder=[]
    for index, dir_info in enumerate(os.walk(data_dir+"/projects/")):
        if len(dir_info[2]) > 0:
            for name in dir_info[2]:
                dir_and_folder.append([dir_info[0],dir_info[0].split("\\")[-1],name])
    '''
    for i in dir_and_folder:
        print(i)
        break
    '''
    
    pool = Pool()
    ans = pool.map(cover_Field,dir_and_folder[:])
    '''
    for j in ans:
        print(j)
        break
    '''
        #if i[1] == "ok":
            #print(i)
            #break
    
    #1807450060^AI99
    







        
