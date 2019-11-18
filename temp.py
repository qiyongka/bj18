# -*- coding: utf-8 -*-
"""
Created on Tue 10 22  2019

@author: 齐用卡
"""
import csv
import threading
import os
import pandas as pd
import numpy as np
from scipy.fftpack import fft
import glob

path = '/home/qyk/Desktop/电抗器'
input_path = '/home/qyk/Desktop/电抗器/dataset'
output_path = '/home/qyk/Desktop/电抗器/output'
fft_size = 125000
sampling_rate = 1250000

def mkdir(path):        #创造文件夹
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True

def file_num(path):     #文件的数目
    input = path + '/' +'*csv'
    files=glob.glob(input)
    num=len(files)
    return num

folder_filenames = os.listdir(input_path)
folder_filenames.sort()
print(folder_filenames[0])
for folder in range(len(folder_filenames)):
    input_path = '/home/qyk/Desktop/电抗器/dataset'
    output_path = '/home/qyk/Desktop/电抗器/output'
    input_path = input_path +'/'+folder_filenames[folder]

    output_path = output_path + '/'+folder_filenames[folder]
    mkdir(output_path)

    #print(input_path,output_path)

    filenames = os.listdir(input_path)
    filenames.sort()
    #print(len(filenames))
    data = np.array([0]*125000)
    for i in range(len(filenames)):
        #print(filenames[i])
        filename = filenames[i]
        #print(filename)
        if filename[-4:] == '.CSV' or filename[-4:] == '.csv':  
            print(i,':',filename)
            input_file = input_path + '/' +filename
            temp = pd.read_csv(input_file, sep = ',', header=14,engine = 'c')
            keys = list(temp)
            index = keys[1]
            CH1 = temp[index] 
            length = len(CH1)
            if length < 125000:
                for ii in range(length,125000):
                    CH1[ii]=0
            data = np.vstack((data,CH1))


    samples = data.shape[0] #训练集样本数量
    timestamps = data.shape[1] #每个样本的采样点数量
    print(samples,timestamps)

    sample = np.zeros((int(samples),int(timestamps+1))) 
    for row in range (0,samples):    
        for column in range (0,timestamps):   
            temp = data[row][column]  
            if temp =='-'    :
                temp = 0
            sample[row,column+1] = temp
        sample[row][0] = row
    sample = np.array(sample[1:len(filenames)+1])
    sample = pd.DataFrame(sample)
    sample[0] = sample[0].astype(int) 
    output_file = output_path +'/' +folder_filenames[0] + '.csv'
    sample.to_csv(output_file,header=0,sep = ',',columns=None,index=0)









