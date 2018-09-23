#!/usr/bin/python2.7
import sys
from collections import Counter
import math


f=open(sys.argv[1],'r')#baiduseginfo
ff=f.readlines()
g=open(sys.argv[2],'r')#idfdict
gg=g.readlines()
h=open(sys.argv[3],'r')#stopword dict
hh=h.readlines()
word_filenum_dict={}# the number of files which contains the word
word_freq_dict={}# the frequence of words in all files
TitleRank=[3,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
ContentRank=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#TitleRank=[3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#ContentRank=[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def load_idf_dict(gg):
	d={}
	for line in gg:
		#print line
		data=line.strip().split()
		word_id=int(data[0])
		query=data[1].strip()
		idf=float(data[3].strip())
		d[query]=[word_id,idf]
	return d
def load_idf_dict_with_stopword(gg,hh):
    d={}
    stopword_dict={}
    for line in hh: 
        data=line.strip().split()
        if data[0].strip() not in stopword_dict:
            if int(data[1].strip())>0:
                stopword_dict[data[0].strip()]=1
            else:
                stopword_dict[data[0].strip()]=0
        else:
            stopword_dict[data[0].strip()]*=int(data[1].strip())
    for line in gg: 
        #print line
        data=line.strip().split()
        word_id=int(data[0])
        query=data[1].strip()
        idf=float(data[3].strip())
        if query in stopword_dict and stopword_dict[query]==1:
            idf=0
        d[query]=[word_id,idf]
    return d

'''
def load_idf_dict_with_stopword(gg,hh):
	d={}
	stopword_dict={}
	for line in hh: 
		data=line.strip().split()
		if data[0].strip() not in stopword_dict:
			if int(data[1].strip())>0:
				stopword_dict[data[0].strip()]=1
			else:
				stopword_dict[data[0].strip()]=0
		else:
			stopword_dict[data[0].strip()]*=int(data[1].strip())
	for line in gg: 
		#print line
		data=line.strip().split()
		word_id=int(data[0])
		query=data[1].strip()
		idf=float(data[3].strip())
		if query in stopword_dict and stopword_dict[query]==1:
			idf=0
		d[query]=[word_id,idf]
	return d

def load_idf_dict_with_stopword(gg,hh):
	d={}
	stopword_dict={}
	for line in hh:
		data=line.strip().split()
		if int(data[1].strip())>0:
			stopword_dict[data[0].strip()]=1
		else:
			stopword_dict[data[0].strip()]=0
	for line in gg:
		#print line
		data=line.strip().split()
		word_id=int(data[0])
		query=data[1].strip()
		idf=float(data[3].strip())
		if query in stopword_dict and stopword_dict[query]==1:
			idf=0
		d[query]=[word_id,idf]
	return d
'''
def dict_plus_with_rank(oridict,newdict,rank,idf_dict):
	#print 'testpllus'
	#print newdict
	sum_frequency=sum([float(newdict[key]) for key in newdict])
	#print sum_frequency
	for key in oridict:
		if key in newdict and key in idf_dict:
			oridict[key]+=float(newdict[key])/sum_frequency*float(rank)*float(idf_dict[key][1])
	for key in newdict:
		if key not in oridict and key in idf_dict:
			oridict[key]=float(newdict[key])*float(rank)*float(idf_dict[key][1])/sum_frequency
	#for key in oridict:
	#	print key,oridict[key]
	return oridict

def print_tfidf(query,tfidf_dict,idf_dict):
	if query=='':
		return
	L=[]
	#print 'test'
	for key in tfidf_dict:
		if key in idf_dict:
			#L.append([idf_dict[key],tfidf_dict[key]])
			L.append([idf_dict[key],tfidf_dict[key]])
	L.sort()
	print query+'\t',
	for i in L:
		print str(i[0][0])+':'+str(i[1]),
	print ''

tfidf_dict={}
#idf_dict=load_idf_dict(gg)
idf_dict=load_idf_dict_with_stopword(gg,hh)
countq=0
for line in ff:
	data=line.strip().split('\t')
	#print line
	if len(data)==0:
		continue
	if data[0].strip()=='query':
		#print tfidf_dict
		if len(tfidf_dict)>0:
			print_tfidf(query,tfidf_dict,idf_dict)
		name=''
		if len(data)==2:
			name=data[1].strip()
		query=name
		#print countq,query
		#countq+=1
		tfidf_dict.clear()
		continue
	if data[0].strip()=='title':
		trank=int(data[1].strip())
		if trank>20:
			trank=20
		segstring=''
		if len(data)>=3:
			segstring=data[2]
		temp_dict=dict_plus_with_rank(tfidf_dict,Counter(segstring.strip().split()),TitleRank[trank-1],idf_dict)
		#print temp_dict
		tfidf_dict=temp_dict
	if data[0].strip()=='content':
		crank=int(data[1].strip())
		if crank>20:
			crank=20
		segstring=''
		if len(data)>=3:
			segstring=data[2]
		tfidf_dict=dict_plus_with_rank(tfidf_dict,Counter(segstring.strip().split()),ContentRank[crank-1],idf_dict)
print_tfidf(query,tfidf_dict,idf_dict)
