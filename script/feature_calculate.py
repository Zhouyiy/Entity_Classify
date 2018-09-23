#-*-coding:utf-8-*-
import json
import sys 
import time 
from collections import Counter

class Calculate(object):
	#加载全局配置文件
	def read_conf(self,conf_file_name):
		f=open(conf_file_name,'r')
		self.conf=json.load(f)
		#print self.conf
		
	#加载标签字典
	def load_label_dict(self,label_dict_name):
		with open(label_dict_name,'r') as gg:
			for line in gg:
				data=line.strip().split('\t')
				self.label_dict[data[1]]=data[0]
				
	#加载idf词典
	def load_idf_dict(self,idf_dict_name):
		d={}
		with open(idf_dict_name,'r') as gg:
			for line in gg:
				#print line 
				data=line.strip().split()
				word_id=int(data[0])
				query=data[1].strip()
				idf=float(data[3].strip())
				d[query]=[word_id,idf]
		return d


	#加载带有停止词的词典	
	def load_idf_dict_with_stopword(self,idf_dict_name,stopword_dict_name):
		stopword_dict={}
		with open(stopword_dict_name,'r') as hh:
			for line in hh: 
				data=line.strip().split()
				if data[0].strip() not in stopword_dict:
					if int(data[1].strip())>0:
						stopword_dict[data[0].strip()]=1
					else:
						stopword_dict[data[0].strip()]=0
				else:
					stopword_dict[data[0].strip()]*=int(data[1].strip())
		d={}
		with open(idf_dict_name,'r') as gg:
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
		
	#按行读取切词之后的搜索信息
	def read_segfile(self,segfile_name):
		with open(segfile_name,'r') as gg:
			for line in gg:
				data=line.strip().split('\t')
				if len(data)==0:
					continue
				elif data[0].strip()=='start':
					query=''
					Ltitle=[]
					Lcontent=[]
					Lurl=[]
					continue
				elif data[0].strip()=='query':
					name=''
					if len(data)==2:
						name=data[1].strip()
					query=name
					continue
				elif data[0].strip()=='title' or data[0].strip()=='content':
					rank=int(data[1].strip())
					seg_string=''
					if len(data)>=3:
						#print data[2]
						seg_string=data[2]
					#print 'testseg_string',seg_string
					if data[0].strip()=='title':
						Ltitle.append([rank,seg_string])
					else:
						Lcontent.append([rank,seg_string])
					continue
				elif data[0].strip()=='url':
					rank=int(data[1].strip())
					url=''
					if len(data)>=2:
						url=data[2]
					Lurl.append([rank,url])
				elif data[0].strip()=='end':
					Ltitle.sort(key=lambda x:x[0])
					Lcontent.sort(key=lambda x:x[0])
					Lurl.sort(key=lambda x:x[0])
					self.seg_info_dict[query]=[Ltitle,Lcontent,Lurl]
		 
	#tfidf特征计算
	def tfidf_calculate(self):
		for key in self.seg_info_dict:
			#print count,key
			tfidf_dict={}
			L=self.seg_info_dict[key]
			for i in L[0]:
				if int(i[0])>20:
					continue
				tfidf_dict=self.__dict_plus_with_rank(tfidf_dict,Counter(i[1].strip().split()),self.conf["TFIDF_TITLE_RANK"][int(i[0])-1],self.idf_dict)
			for i in L[1]:
				if int(i[0])>20:
					continue
				tfidf_dict=self.__dict_plus_with_rank(tfidf_dict,Counter(i[1].strip().split()),self.conf["TFIDF_CONTENT_RANK"][int(i[0])-1],self.idf_dict)
			LL=[]
			#print tfidf_dict
			for word in tfidf_dict:
				if word in self.idf_dict:
					LL.append([self.idf_dict[word],tfidf_dict[word]])
			LL.sort(key=lambda x:x[0])
			self.tfidf_feature_dict[key]=LL

	#url特征计算
	def url_calculate(self):
		for key in self.seg_info_dict:
			tfidf_dict={}
			L=self.seg_info_dict[key]
			for i in L[2]:
				if int(i[0])>20:
					continue
				tfidf_dict=self.__dict_plus_with_rank(tfidf_dict,Counter(i[1].strip().split()),self.conf["URL_RANK"][int(i[0])-1],self.url_idf_dict)
			LL=[]
			for word in tfidf_dict:
				if word in self.url_idf_dict:
					LL.append([self.url_idf_dict[word],tfidf_dict[word]])
			LL.sort(key=lambda x:x[0])
			self.url_feature_dict[key]=LL
		#print len(self.url_feature_dict)

	#每个query特征合并在一起
	def feature_fuse(self):
		for key in sorted(self.conf["FEATURE_ENABLE"]):
			if int(self.conf["FEATURE_ENABLE"][key])>0:
				self.feature_calculated_list.append(self.Feature_Dict_Dict[key])
				
		if len(self.feature_calculated_list)==1:
			self.final_feature_dict=self.feature_calculated_list[0]
			return
		keyset=set()
		count_feature_max=[None]*len(self.feature_calculated_list)
		#默认feature的location从小到大排序
		for count in range(len(self.feature_calculated_list)):
			for key in self.feature_calculated_list[count]:
				keyset.add(key)
				count_feature_max[count]=max(self.feature_calculated_list[count][key][-1][0][0],count_feature_max[count])
				if count>0:
					self.feature_calculated_list[count][key]=[[[i[0][0]+count_feature_max[count-1],i[0][1]],i[1]] for i in self.feature_calculated_list[count][key]]
		for key in keyset:
			if key=='':
				continue
			self.final_feature_dict[key]=[]
			for i in self.feature_calculated_list:
				#print 'test',key,key in i,key in self.final_feature_dict
				if key in i:
					self.final_feature_dict[key]+=i[key]
					
	#打印计算后的feature
	def print_feature(self,d):
		#for key in self.final_feature_dict:
		for key in d:
			if key=='':
				continue
			if key in self.label_dict:
				#print key,
				print self.label_dict[key],
				for i in d[key]:
					print str(i[0][0])+':'+str(i[1]),
				print ''
		return
	
	#打印计算后的feature及其相关含义
	def print_feature_with_meaning(self):
		return 


	#加载计算好的feature
	def load_feature(self,feature_file):
		d={}
		with open(feature_file,'r') as gg:
			for line in gg:
				data=line.strip().split()
				L=[]
				if len(data)>1:
					for i in data[1:]:
						L.append([i.split(':')[0],i.split(':')[0]])
				d[data[0]]=L
		return d

	#tfidf加权计算
	def __dict_plus_with_rank(self,oridict,newdict,rank,idf_dict):
		sum_frequency=sum([float(newdict[key]) for key in newdict])
		for key in oridict:
			if key in newdict and key in idf_dict:
				oridict[key]+=float(newdict[key])/sum_frequency*float(rank)*float(idf_dict[key][1])
		for key in newdict:
			if key not in oridict and key in idf_dict:
				oridict[key]=float(newdict[key])*float(rank)*float(idf_dict[key][1])/sum_frequency
		return oridict
	
	def feature_calculate(self):
		for key in self.conf['FEATURE_ENABLE']:
			if int(self.conf['FEATURE_ENABLE'][key])>0:
				self.Feature_Function_Dict[key]()
				
	def __init__(self):

		#全局配置文件
		self.conf={}
		self.label_dict={}

		#分词后的百度检索信息
		self.seg_info_dict={}

		#tfidf特征的参数
		self.tfidf_max_index=0
		self.idf_dict={} 
		self.tfidf_feature_dict={} 

		#url特征参数
		self.url_max_index=0
		self.url_idf_dict={} 
		self.url_feature_dict={} 

		self.feature_calculated_list=[]
		self.final_feature_dict={} 

		#配置函数字典
		self.Feature_Function_Dict={
			'TFIDF':self.tfidf_calculate,
			'URL':self.url_calculate
		}
		self.Feature_Dict_Dict={
			'TFIDF':self.tfidf_feature_dict,
			'URL':self.url_feature_dict
		}


	
	def auto_procedure(self,conf_file_name,tfidf_dict_name,url_dict_name,segfile_name,stopword_dict_name,label_dict_name):
		self.read_conf(conf_file_name)
		self.load_label_dict(label_dict_name)
		self.idf_dict=self.load_idf_dict_with_stopword(tfidf_dict_name,stopword_dict_name)
		#self.load_idf_dict(tfidf_dict_name)
		self.read_segfile(segfile_name)
		#print 'step1'
		#self.tfidf_calculate()
		#self.idf_dict.clear()
		#print 'step2'
		self.url_idf_dict=self.load_idf_dict(url_dict_name)
		#self.url_calculate()
		#print 'step3'
		self.feature_calculate()
		self.feature_fuse()
		self.print_feature(self.final_feature_dict)

if __name__=='__main__':
	conf_file_name=sys.argv[1]
	tfidf_dict_name=sys.argv[2]
	url_dict_name=sys.argv[3]
	segfile_name=sys.argv[4]
	stopword_dict_name=sys.argv[5]
	label_dict_name=sys.argv[6]
	Calculate().auto_procedure(conf_file_name,tfidf_dict_name,url_dict_name,segfile_name,stopword_dict_name,label_dict_name)
