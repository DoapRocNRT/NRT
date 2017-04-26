# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 12:12:19 2017

@author: weilun
"""


import numpy as np
import os
import json
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Input, Flatten, Dropout, Activation, Merge
from keras.layers import Convolution1D, MaxPooling1D, Embedding, Reshape
from keras.callbacks import ModelCheckpoint
from keras.models import Model
from keras import regularizers
from keras.layers.recurrent import LSTM
import h5py

np.random.seed(2018)

path='C:/Users/weilun/Desktop/Transcript_Json'
os.chdir(path)

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


with open('all_subtask_prosody.json', 'r') as dic:
    pro_subtask = json.load(dic)
    
with open('all_subject_sex.json', 'r') as dic:
    sub_sex = json.load(dic)
    
with open('all_subtask_label.json', 'r') as lab:
    all_subtask_label = json.load(lab)


intensity=[]
pitch2=[]
ii=[]
for sub in subject:
    
    if sub in pro_subtask:
        
        if pro_subtask[sub]!=None:
            intensity.append(pro_subtask[sub][1])
            pitch2.append(pro_subtask[sub][0])
        else:
            ii.append(subject.index(sub))

    else:
        ii.append(subject.index(sub))
    
sgraa=[sgra[j] for j in range(len(sgra)) if j not in ii]  
smorr=[smor[j] for j in range(len(smor)) if j not in ii]       
swrdd=[swrd[j] for j in range(len(swrd)) if j not in ii]       
slabb=[slab[j] for j in range(len(slab)) if j not in ii]    
         
sgra=sgraa
smor=smorr
swrd=swrdd
slab=slabb

def normalize_pitch(p):
    arr_p=np.asarray(p)
    if (len(arr_p[arr_p!=0])==0):
        return np.zeros(np.shape(arr_p))
    if (float(np.std(arr_p[arr_p!=0]))==0):
        return np.zeros(np.shape(arr_p))
    arr_p[arr_p!=0]=((arr_p[arr_p!=0]-np.mean(arr_p[arr_p!=0]))/float(np.std(arr_p[arr_p!=0])))
    
    return arr_p

def normalize_intensity(p):
    arr_p=np.asarray(p)
    if (len(arr_p[arr_p!=0])==0):
        return np.zeros(np.shape(arr_p))
    if (float(np.std(arr_p[arr_p!=0]))==0):
        return np.zeros(np.shape(arr_p))
    arr_p=((arr_p-np.mean(arr_p[arr_p!=0]))/float(np.std(arr_p[arr_p!=0])))
    return arr_p
    
norm_intens=list(map(normalize_intensity,intensity))
norm_pitch=list(map(normalize_pitch,pitch2))

l_norm_intens=[list(x) for x in norm_intens]
l_norm_pitch=[list(x) for x in norm_pitch]

def trunc_pad_zero(l, max_length=3000):
    for x in l:
        while len(x)< max_length:
            x.append(0)
        while len(x)> max_length:
            x.pop(-1)
    return l

l_norm_intens=trunc_pad_zero(l_norm_intens)
l_norm_pitch=trunc_pad_zero(l_norm_pitch)

data4=np.asarray(l_norm_intens)  # intensity
data5=np.asarray(l_norm_pitch) # pitch

max_len_wrd=0
his=[]
for x in swrd:
    his.append(len(x))
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


print('Shape of data tensor:', data1.shape)
print('Shape of data tensor:', data2.shape)
print('Shape of data tensor:', data3.shape)
print('Shape of data tensor:', data4.shape)
print('Shape of data tensor:', data5.shape)
print('Shape of label tensor:', labels.shape)  


#Split data into training/validation
EMBEDDING_DIM = 100
VALIDATION_SPLIT = 0.1

indices = np.arange(labels.shape[0])
np.random.shuffle(indices)
data1 = data1[indices]
data2 = data2[indices]
data3 = data3[indices]
data4 = data4[indices]
data5 = data5[indices]
labels = labels[indices]
nb_validation_samples = int(VALIDATION_SPLIT * labels.shape[0])

x1_train = np.reshape(data1[:-nb_validation_samples],(data1[:-nb_validation_samples].shape[0],data1[:-nb_validation_samples].shape[1],1))
x2_train = np.reshape(data2[:-nb_validation_samples],(data2[:-nb_validation_samples].shape[0],data2[:-nb_validation_samples].shape[1],1))
x3_train = data3[:-nb_validation_samples]
x4_train = np.reshape(data4[:-nb_validation_samples],(data4[:-nb_validation_samples].shape[0],data4[:-nb_validation_samples].shape[1],1))
x5_train = np.reshape(data5[:-nb_validation_samples],(data5[:-nb_validation_samples].shape[0],data5[:-nb_validation_samples].shape[1],1))
y_train = labels[:-nb_validation_samples]



x1_val = np.reshape(data1[-nb_validation_samples:],(data1[-nb_validation_samples:].shape[0],data1[-nb_validation_samples:].shape[1],1))
x2_val = np.reshape(data2[-nb_validation_samples:],(data2[-nb_validation_samples:].shape[0],data2[-nb_validation_samples:].shape[1],1))
x4_val = np.reshape(data4[-nb_validation_samples:],(data4[-nb_validation_samples:].shape[0],data4[-nb_validation_samples:].shape[1],1))
x5_val = np.reshape(data5[-nb_validation_samples:],(data5[-nb_validation_samples:].shape[0],data5[-nb_validation_samples:].shape[1],1))
x3_val = data3[-nb_validation_samples:]
y_val = labels[-nb_validation_samples:]

#Prepare GloVe Embedding Matrix
BASE_DIR = ''
GLOVE_DIR = BASE_DIR + 'glove.6B/'

embeddings_index = {}
f = open(os.path.join(GLOVE_DIR, 'glove.6B.100d.txt'))
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()    
    
print('Found %s word vectors.' % len(embeddings_index))

EMBEDDING_DIM = 100
nb_words = len(word_index)

embedding_matrix = np.zeros((nb_words + 1, EMBEDDING_DIM))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector


num_hidden_units_lstm=1024
nb_hidden_units=1024

print('Start learning!')

branch1=Sequential([
	LSTM(output_dim = num_hidden_units_lstm, 
	return_sequences=False, 
	input_shape=(MAX_SEQUENCE_LENGTH,1), name='LSTM1')

])

branch2=Sequential([
	LSTM(output_dim = num_hidden_units_lstm, 
	return_sequences=False, 
	input_shape=(MAX_SEQUENCE_LENGTH,1), name='LSTM2')

])




branch3 = Sequential([

    Embedding(nb_words + 1,EMBEDDING_DIM,
              weights=[embedding_matrix], input_length=MAX_SEQUENCE_LENGTH,
              trainable=False, name='embedding'),

    LSTM(output_dim = num_hidden_units_lstm, 
	 return_sequences=False, 
	 input_shape=(MAX_SEQUENCE_LENGTH, EMBEDDING_DIM), name='LSTM3')

])

num_hidden_units_conv=1024
nb_hidden_units=1024
nb_filter=128
filter_length=60
MAX_SEQUENCE_LENGTH_2 = 3000

branch4=Sequential([
	Convolution1D(nb_filter=nb_filter,
	filter_length=filter_length, 
	border_mode='valid',
	activation='tanh', 
	input_shape=(MAX_SEQUENCE_LENGTH_2,1),activity_regularizer=regularizers.activity_l1(0.01), name='CONV11'),
	Flatten(),
      Dense(nb_hidden_units, init='uniform', activation='tanh')

])

branch5=Sequential([
	Convolution1D(nb_filter=nb_filter,
	filter_length=filter_length, 
	border_mode='valid',
	activation='tanh', 
	input_shape=(MAX_SEQUENCE_LENGTH_2,1),activity_regularizer=regularizers.activity_l1(0.01), name='CONV21'),
	Flatten(),
      Dense(nb_hidden_units, init='uniform', activation='tanh')
 
])


model=Sequential([
    Merge([branch1,branch2,branch3,branch4,branch5],mode='mul'),
    Dense(nb_hidden_units, init='uniform', activation='tanh'),
    Dense(nb_hidden_units, init='uniform', activation='tanh'),
    Dropout(0.5),
    Dense(2, init='uniform', activation='softmax'),

])




model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

filepath="weights_best_trans_pros.h5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

model.fit([x1_train,x2_train,x3_train,x4_train,x5_train],y_train, validation_data=([x1_val,x2_val,x3_val,x4_val,x5_val],y_val),nb_epoch=50, batch_size=32,callbacks=callbacks_list)

#model.fit([x1_train,x2_train,x3_train],y_train, validation_data=([x1_val,x2_val,x3_val],y_val),nb_epoch=50, batch_size=32)
