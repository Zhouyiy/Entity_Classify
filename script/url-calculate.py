import sys
from collections import Counter
import math

f=open(sys.argv[1],'r')
ff=f.readlines()
word_filenum_dict={}# the number of files which contains the word
word_freq_dict={}# the frequence of words in all files
filecounter=0
for line in ff:
	data=line.strip().split('\t')
	if data[0].strip()=='url':
		if len(data)>=3:
			seg_string=data[2]
		else:
			seg_string=''
		#print seg_string
		uc=Counter([seg_string.strip()])
		#print uc
		filecounter+=1
		for key in uc:
			#print key
			if key in word_filenum_dict:
				word_filenum_dict[key]+=1
			else:
				word_filenum_dict[key]=1
			if key in word_freq_dict:
				word_freq_dict[key]+=uc[key]
			else:
				word_freq_dict[key]=uc[key]
		#print filecounter
word_id=1
for key in word_filenum_dict:
	print word_id,'\t',key,'\t',word_freq_dict[key],'\t',math.log(float(filecounter)/word_filenum_dict[key])
	word_id+=1
