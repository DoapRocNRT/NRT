# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 15:38:08 2017

@author: shaorong & weilun
"""

import os
import glob
import json
import collections
import wave
from scipy.io import wavfile
from scipy.signal import blackmanharris as bmh
import numpy as np
from math import log


extension='.json'
jl = [i for i in glob.glob('*{}'.format(extension))]

dic_list=[]
for item in jl:
    with open(item, 'r') as dic:
        dic_list.append(json.load(dic))

apha_cind=dic_list[1]
apha_sand=dic_list[2]
contr_cind=dic_list[3]
contr_sand=dic_list[4]

#inputfile="ACWT08a.wav"
pro_dict=collections.defaultdict()

def cutwave(start, end, inputfile,outputfile):
        wav = wave.open(inputfile,'r')
        [nchan, sampwidth, framerate, length, haha, comp] = wav.getparams()
        t1 = framerate * start/1000
        t2 = framerate * end/1000
        wav.setpos(t1)
        cutdata = wav.readframes(t2-t1)
        cutfile = wave.open(outputfile,'w')
        cutfile.setnchannels(nchan)
        cutfile.setsampwidth(sampwidth)
        cutfile.setframerate(framerate)
        cutfile.writeframes(cutdata)
        cutfile.close

def getPitchIntensity(inputfile):
        # Get sampling rate and wavefile
        sf, wav = wavfile.read(inputfile)
        # Normalize to 1/-1
        wav = wav/(2.**15)
#        norm = max(max(wav),abs(min(wav)))
#        wav = wav/norm
        # Silence threshold Treating segments with average intensity below 1/5 of the peak as silence (i.e. 14dB, assuming normed to 70dB)
       # thres = (norm * 2 ** 15)**(0.1-1)
        db=5.
        thres= 10.**(db/10)/(2.**15)
        # Get length of wave file
        N = wav.shape[0]
        # Get number of 100ms windows
        nf = N/(100*sf/1000)
        # iterate through the wave file to get pitch and intensity
        i=0
        output = np.empty([2,nf])
        while i < nf:
                wavseg = wav[100*sf*i/1000:100*sf*(i+1)/1000,]
                # Define windows
                n = len(wavseg)
                windowed = wavseg*bmh(n)
                # Perform FFT on segment
                rFFT = np.abs(np.fft.rfft(windowed))
                # Find the peak
                peak = np.argmax(abs(rFFT))
                # Get pitch
                pit = sf*peak/n
		meanwav= np.mean(wavseg**2)
		if meanwav==0:
			intens= log(meanwav+6e-07,10)
		else:
			intens = log(meanwav,10)
                # Getting rid of outliers
                if pit > 350 or pit < 50 or intens < log(thres,10):
                        pit = 0                
                # Treating segments with average intensity below 1/5 of the norm as silence
                if intens < log(thres,10):
                        intens = 0
                output[0,i] = pit
                output[1,i] = intens
                i+=1
        return output

        
def get_dict_list(inputfile,t):
    timestamps=t[inputfile[:-4]]
    num_lines = int(round(len(timestamps)/2))
    if num_lines>0:
        for i in range(num_lines):
            start_line =int(''.join([s for s in timestamps[2*i] if s.isdigit()]))
            end_line = int(''.join([s for s in timestamps[2*i+1] if s.isdigit()]))
            cutwave(start_line,end_line, inputfile, 'Temp.wav')
            pitch_intens_line = getPitchIntensity('Temp.wav')
            if i==0:
                pi=pitch_intens_line
            else:
                pi=np.hstack((pi,pitch_intens_line))
            os.remove('Temp.wav')
        return [list(pi[0]),list(pi[1])]
    
    
    
def task_prosody(inputfile):
    
    if inputfile[:-4] in apha_cind:
        pil=get_dict_list(inputfile,apha_cind)
        pro_dict[inputfile[:-4]+'_Cinderella']=pil
        
    if inputfile[:-4] in apha_sand:
        pil=get_dict_list(inputfile,apha_sand)
        pro_dict[inputfile[:-4]+'_Sandwich']=pil
        
    if inputfile[:-4] in contr_cind:
        pil=get_dict_list(inputfile,contr_cind)
        pro_dict[inputfile[:-4]+'_Cinderella']=pil  
        
    if inputfile[:-4] in contr_sand:
        pil=get_dict_list(inputfile,contr_sand)
        pro_dict[inputfile[:-4]+'_Sandwich']=pil        

extension = '.wav'
result = [i for i in glob.glob('*{}'.format(extension))]

for wav in result:
    try:
	task_prosody(wav)

    except wave.Error:        #Videos are cut to a shorter length than suggested by the actual timestamps
	pass

with open('all_subtask_prosody.json', 'r') as dic:
    pro_subtask = json.load(dic)
    
with open('all_subject_sex.json', 'r') as dic:
    sub_sex = json.load(dic)
    
with open('all_subtask_label.json', 'r') as lab:
    all_subtask_label = json.load(lab)

subject=[]
intens=[]
pitch=[]
sex=[]
label=[]

for item,k in pro_subtask.items():
    
    if k!=None:
        
        if '_Cinderella' in item and item[:-11] in sub_sex:
            sex.append(sub_sex[item[:-11]])
            subject.append(item)
            pitch.append(k[0])
            intens.append(k[1])
            label.append(all_subtask_label[item])
        
        if '_Sandwich' in item and item[:-9] in sub_sex:
            sex.append(sub_sex[item[:-9]])
            subject.append(item)
            pitch.append(k[0])
            intens.append(k[1])
            label.append(all_subtask_label[item])
        
def norm(x):
    arr_x=np.asarray(x)
    intens_task = (arr_x-np.mean(arr_x))/np.std(arr_x)
    return intens_task

    
# Normalize within each subject-task pair.    
norm_intens=list(map(norm,intens))
norm_pitch=list(map(norm,pitch))

    

