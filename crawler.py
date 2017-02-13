# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 19:24:59 2017

@author: weilun
"""    
import re 
import urllib

def getHtml(url):
	page=urllib.urlopen(url)
	html=page.read()
	return html

def getFolder(html):
	r=r'href=".*/"'
	re_folder=re.compile(r)
	folderList=re.findall(re_folder,html)
	return folderList

def getMp4(url,folderlist):
	r=r'href=".*a\.mp4"'
	for folder in folderlist[1:]:
		page=urllib.urlopen(url+folder[6:-1]) 
		htmll=page.read()
		re_mp4=re.compile(r)
		mp4List=re.findall(re_mp4,htmll)
		
		for mp4url in mp4List:
			urllib.urlretrieve(url+folder[6:-1]+mp4url[6:-1],"%s" %(mp4url[6:-1]))
			print  'file "%s"' %(mp4url[6:-1])
		

#The url line below specifies the URL link for Aphasia group video, for Control group video the url below should be 'http://talkbank.org/media/AphasiaBank/English/Control/'
url='http://talkbank.org/media/AphasiaBank/English/Aphasia/' 
html=getHtml(url)
folderList=getFolder(html)
getMp4(url,folderList)
