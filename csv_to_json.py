# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 15:22:07 2017

@author: weilun
"""

# Combine language features from CSV files into Json Dictionaries.

import glob
import csv
import os
import json
import collections


# Claim the folder path where the target csv files are located (e.g. 'Sandwich/Control')
extension = '.csv'
path='C:/Users/weilun/Desktop/NRT Practicum/Data/transcripts-extracted/Sandwich/Control'
os.chdir(path)
result = [i for i in glob.glob('*{}'.format(extension))]

#Load data from csv into python dictionaries together with their respective labels
gmw=[]
sub_dict=collections.defaultdict()
lab_dict=collections.defaultdict()

for k in range(len(result)):
    name=result[k]
    py=open(name)
    lg=list(csv.reader(py))
    
    lan=[]
    for i in lg:
        for j in i:
            lan.append(j)
    gmw.append(lan)
    
    if k==len(result)-1 or result[k][:-8]!=result[k+1][:-8]:
        sub_dict[result[k][:-8]]=gmw
        lab_dict[result[k][:-8]]=0 # 0 for Control; 1 for Aphasia, Consistent with the csv data.
        gmw=[]
            
#Store the dictionaries for each subjects in json files 
with open('Apha_sand.json','w') as dic:
    json.dump(sub_dict,dic)
        
with open('Apha_sand_lab.json','w') as lab:
    json.dump(lab_dict,lab)

