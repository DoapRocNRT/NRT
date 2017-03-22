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

# Store dictionaries for subject sex and timestamps of both tasks per subject
path='C:/Users/weilun/Desktop/NRT_Practicum/Data/timestamps/csv'
os.chdir(path)
ts=['control_cinderella.csv','aphasia_cinderella.csv','aphasia_sandwich.csv','control_sandwich.csv']

for l in ts:
    
    ts_dict=collections.defaultdict()
        
    py=open(l)
    ap=list(csv.reader(py))
    
    for i in range(1,len(ap)):
        ts_dict[ap[i][0][:-4]]=ap[i][3:]
    
    with open(l[:-4]+'.json','w') as dic:
        json.dump(ts_dict,dic)
        
        
        

sex_dict=collections.defaultdict()

path='C:/Users/weilun/Desktop'
os.chdir(path)

sex_list=['ACWT01a_Cinderella.kideval.xls','capilouto01a_Cinderella.kideval.xls','capilouto01a_Sandwich.kideval.xls',]
def get_sex_dict(sex_list):
    for group in sex_list:
        normpy=open(group)
        normap=list(csv.reader(normpy))
        for item in normap[1:-1]:
            print(item[0])
            item_split=item[0].split('\t')
            sex_dict[item_split[0][:-15]]=item_split[5]
    return sex_dict
    
sex_dict=get_sex_dict(sex_list)

with open('all_subject_sex.json','w') as dic:
    json.dump(sex_dict,dic)
        


