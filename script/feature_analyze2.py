import sys
from collections import Counter
import math

f=open(sys.argv[1],'r')#baiduseginfo
ff=f.readlines()
g=open(sys.argv[2],'r')#idfdict
gg=g.readlines()
h=open(sys.argv[3],'r')#stopword dict
hh=h.readlines()
s=open(sys.argv[4],'r')#modelfile
ss=s.readlines()
#p=open(sys.argv[5],'r')#wronganalyzefile
#pp=p.readlines()


word_filenum_dict={}# the number of files which contains the word
word_freq_dict={}# the frequence of words in all files
TitleRank=[10,5,3,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
ContentRank=[3,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
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

def softmax(list):
    sum=0
    L=[]
    for i in range(len(list)):
        if float(list[i])>500:
            list[i]=500
        sum+=math.exp(float(list[i]))
        
    for i in range(len(list)):
        L.append(round(math.exp(float(list[i]))/sum,2))
    return L

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
    #for key in stopword_dict:
    #    print key,stopword_dict[key]
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
			stopword_dict[line.strip()]=1
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
def load_label_file(ii):
	d={}
	for line in ii:
		data=line.strip().split('\t')
		#print data
		query=data[0].strip()
		label=data[1].strip()
		predict_type=data[2].strip()
		predict_content=data[3].strip()
		d[query]=[label,predict_type,predict_content]
	return d

def load_modelfile(ss):
	d={}
	for line in ss:
		data=line.strip().split('\t')
		word=data[0].strip()
		L=[]
		for i in data[1].strip().split():
			#print i
			L.append(i)
		d[word]=L
	return d

def listplus(a,b):
    if len(a)==0:
        temp=[]
        for count in range(len(b)):
            temp.append(round(float(b[count]),4))
        return temp
    elif len(b)==0:
        temp=[]
        for count in range(len(a)):
            temp.append(round(float(a[count]),4))
        return temp
    else:
        c=[]
        count=0
        for count in range(len(a)):
            c.append(round(float(a[count])+float(b[count]),4))
        return c

def print_score(modeldict,newdict,rank,idf_dict,sumweight_list):
	sum_frequency=sum([float(newdict[key]) for key in newdict])
	LL=[]
	LN=[]
	for key in newdict:
		if key in modeldict and key in idf_dict:
			newdict[key]=float(newdict[key])*float(rank)*float(idf_dict[key][1])/sum_frequency
			L=[]
			for i in modeldict[key]:
				L.append(float(i)*newdict[key])
				#L.append(float(1)*newdict[key])
			if sum(L)!=0:
				LL.append([key,['%.2f' % (i) for i in L]])
			else:
				LN.append(key)
	LL.sort(reverse=True,key=lambda x:x[1][1])
	sw=[]
	for i in LL:
		sw=listplus(sw,i[1])
	#print sw
	'''
	print 'sum_weight', 
	for i in sw:
		print '%.2f' % (float(i)),
	print ''
	for i in LL:
		print i[0],
		for j in i[1]:
			print j,
		print ''		
	for i in LN:
		print "\""+i+"\"",
	print ''
	'''
	sumweight_list=listplus(sumweight_list,sw)
	#print sumweight_list
	return sumweight_list

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
	'''
	print query+'\t',
	for i in L:
		print str(i[0][0])+':'+str(i[1]),
	print ''
	'''

#label_dict=load_label_file(ii)
#label_dict=load_label_file(pp)
idf_dict=load_idf_dict_with_stopword(gg,hh)
model_dict=load_modelfile(ss)
countq=0
sumweight_list=[]
#predict_type=0
printable=1
for line in ff:
	data=line.strip().split('\t')
	#print line
	if len(data)==0:
		continue
	if data[0].strip()=='query':
		#print tfidf_dict
		#print sumweight_list
		if sum(sumweight_list)!=0 and printable>0:
			print "total_sum_weight",sumweight_list
			print '\n\n\n'
			sumweight_list=[]
		name=''
		if len(data)==2:
			name=data[1].strip()
		query=name
		#if query in label_dict:
		#	printable=1
		#print 'query',name
		#	print label_dict[query]
		#else:
		#	printable=0
		#print countq,query
		#countq+=1
		#tfidf_dict.clear()
		#predict_type=label_dict[name]
		continue
	
	if data[0].strip()=='title' and printable > 0:
		trank=int(data[1].strip())
		if trank>20:
			trank=20
		segstring=''
		if len(data)>=3:
			segstring=data[2]
		#print 'title'+'\t'+str(trank)+'\t'+segstring
		sumweight_list=print_score(model_dict,Counter(segstring.strip().split()),TitleRank[trank-1],idf_dict,sumweight_list)
	if data[0].strip()=='content'and printable > 0:
		crank=int(data[1].strip())
		if crank>20:
			crank=20
		segstring=''
		if len(data)>=3:
			segstring=data[2]
		#print 'content'+'\t'+str(crank)+'\t'+segstring
		sumweight_list=print_score(model_dict,Counter(segstring.strip().split()),ContentRank[crank-1],idf_dict,sumweight_list)
		#print ''
	if line==ff[-1]:
		if sum(sumweight_list)!=0 and printable>0:
			#print "total_sum_weight",sumweight_list
			if sumweight_list.index(min(sumweight_list))==0:
				print name,softmax(sumweight_list)
			#print '\n\n\n'
			sumweight_list=[]

