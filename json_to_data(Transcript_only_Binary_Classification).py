# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 21:23:32 2017

@author: weilun
"""

import json
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical


with open('Contr_cind.json', 'r') as dic:
    x_cc = json.load(dic)

with open('Contr_cind_lab.json', 'r') as lab:
    y_cc = json.load(lab)

with open('Contr_sand.json', 'r') as dic:
    x_cs = json.load(dic)

with open('Contr_sand_lab.json', 'r') as lab:
    y_cs = json.load(lab)

with open('Apha_cind.json', 'r') as dic:
    x_ac = json.load(dic)

with open('Apha_cind_lab.json', 'r') as lab:
    y_ac = json.load(lab)

with open('Apha_sand.json', 'r') as dic:
    x_as = json.load(dic)

with open('Apha_sand_lab.json', 'r') as lab:
    y_as = json.load(lab)

def char_to_int(a):
    for item in a.items():
        a[item[0]][0]=list(map(int,a[item[0]][0]))  
        a[item[0]][1]=list(map(int,a[item[0]][1]))
    return a

x_ac=char_to_int(x_ac)
x_as=char_to_int(x_as)
x_cc=char_to_int(x_cc)    
x_cs=char_to_int(x_cs)   

x=[x_ac,x_as,x_cc,x_cs]
y=[y_ac,y_as,y_cc,y_cs]

def dic_to_list(x,y):
    subject=[]
    sgra=[]
    smor=[]
    swrd=[]
    slab=[]
    
    for k in range(len(x)):
        for sub, i in x[k].items():
            if len(i[0])*len(i[1])*len(i[2])!=0:
                subject.append(sub)
                sgra.append(i[0])
                smor.append(i[1])
                swrd.append(i[2])
                slab.append(y[k][sub])
                
    return sgra, smor, swrd, slab, subject

sgra,smor,swrd,slab,subject=dic_to_list(x,y)

def wrd_seq(x):
    w=''
    for wrd in x:
        if wrd!=x[len(x)-1]:
            w=w+wrd+' '
        else:
            w=w+wrd
    return w

def asc(y):
	for s in y:
		for t in s:
			try:
				t.encode("ascii")
			except UnicodeEncodeError:
				s.pop(s.index(t))


while True:

	try:
		swrd1=list(map(wrd_seq,swrd))
		swrd1=[s.encode('ascii') for s in swrd1]
		break
	except UnicodeEncodeError:
		asc(swrd)


# Specify the max sequence length: no larger than 800 
sgra=[sgra[i] for i in range(len(swrd)) if len(swrd[i])<=800]
smor=[smor[i] for i in range(len(swrd)) if len(swrd[i])<=800]
slab=[slab[i] for i in range(len(swrd)) if len(swrd[i])<=800]
subject=[subject[i] for i in range(len(swrd)) if len(swrd[i])<=800]
swrd=[x for x in swrd if len(x)<=800]


max_len_wrd=0
for x in swrd:
    if len(x)>max_len_wrd:
        max_len_wrd=len(x)



def wrd_seq(x):
    w=''
    for wrd in x:
        if wrd!=x[len(x)-1]:
            w=w+wrd+' '
        else:
            w=w+wrd
    return w

	
swrd=list(map(wrd_seq,swrd))

swrd =[s.encode('ascii') for s in swrd]

#Pad/truncate zeros/values to construct 800-length vector

def trunc_pad_zero(l):
    for x in l:
        while len(x)< max_len_wrd:
            x.append(0)
        while len(x)> max_len_wrd:
            x.pop(-1)
    return l    
    
sgra=trunc_pad_zero(sgra)
smor=trunc_pad_zero(smor)



# Vectorize the word samples into a 2D integer tensor via Keras functions
MAX_SEQUENCE_LENGTH = max_len_wrd
tokenizer = Tokenizer(nb_words=None)
tokenizer.fit_on_texts(swrd)
sequences = tokenizer.texts_to_sequences(swrd)
word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

data1 = np.asarray(sgra) # grammar feature
data2 = np.asarray(smor) # morpheme feature
data3 = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH) # word feature
labels = to_categorical(np.asarray(slab)) # Labels: Aphasia or Control

#Feature tensor shape: (910,800); Label tensor shape: (910,2).
print('Shape of data tensor:', data1.shape)
print('Shape of data tensor:', data2.shape)
print('Shape of data tensor:', data3.shape)
print('Shape of label tensor:', labels.shape)  
