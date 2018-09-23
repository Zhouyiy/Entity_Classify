#encoding=utf-8
import sys 
import os
import re
import json
import urllib
reload(sys) 
sys.setdefaultencoding('utf8')
sys.path.append('./pythonlib')

f=open(sys.argv[1],'r')
ff=f.readlines()
for line in ff:
	data=line.strip().split('\t')
	string=''
	if data[0].strip()=='query':
		if len(data) > 1:
			for i in data[1].split():
				string+=i.strip()
			print data[0].strip()+'\t'+string
		else:
			print data[0].strip()+'\t'+string
		continue
	elif data[0].strip()=='url':
		for i in data[2].split():
			string+=i.strip()
		print data[0].strip()+'\t'+data[1].strip()+'\t'+string
		continue
	elif data[0].strip()=='items':
		for i in data[2].split():
			string+=i.strip()
		print data[0].strip()+'\t'+data[1].strip()+'\t'+string
		continue
	elif data[0].strip()=='tags':
		for i in data[2].split():
			string+=i.strip()
		print data[0].strip()+'\t'+data[1].strip()+'\t'+string
		continue
	elif data[0].strip()=='title' or data[0].strip()=='content' or data[0].strip()=='start' or data[0].strip()=='end':
		print line.strip()
		continue
