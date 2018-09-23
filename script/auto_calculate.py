#-*-coding:utf-8-*-
import json
import sys 
import time 
import os
from collections import Counter

class Calculate(object):
	#加载全局配置文件
	def read_conf(self,conf_file_name):
		f=open(conf_file_name,'r')
		self.conf=json.load(f,encoding='utf8')
		#print self.conf
		
	#加载标签字典
	def load_label_dict(self,label_dict_name):
		with open(label_dict_name,'r') as gg:
			for line in gg:
				data=line.strip().split('\t')
				self.label_dict[data[1]]=data[0]
	
	#获取文件夹中指定开头的文件
	def get_required_folder_name(self,folderpath,prefix_string):
		file_name_list=os.listdir(folderpath)
		retlist=[]
		for i in file_name_list:
			if len(i.strip().split('.'))>0 and i.strip().split('.')[0]==prefix_string:
				retlist.append(folderpath+'/'+i)
		return retlist
		
				
	def load_label_dict_by_folder(self,filetype):
		#label编号
		label2num_dict={}
		count=1
		self.label_dict={}
		#print self.conf
		#print filetype
		for key in sorted(self.conf["CLASS_ENABLE"]):
			#print key,'test1'
			if self.conf["CLASS_ENABLE"][key]>0:
				label2num_dict[key]=count
				count+=1
		if filetype=='train':
			file_name_list=os.listdir(self.conf["DATA_PATH"]["Label_Train"])
		elif filetype=='test':
			file_name_list=os.listdir(self.conf["DATA_PATH"]["Label_Test"])
		#print file_name_list
		#load label labelname:MOV,MUS.... 
		for i in file_name_list:
			#print i
			if len(i.strip().split('.'))<2:
				#print "test2",i,i.strip().split(r'.'),'ok'
				#print i.strip().split(r'.'),'ok'
				continue
			if i.strip().split('.')[0]!=u'label':
				#print "test1"
				continue
			labelname=i.strip().split('.')[1] 
			#print labelname
			if labelname in label2num_dict:
				#print filetype,labelname
				if filetype=='train':
					label_file_path=self.conf["DATA_PATH"]["Label_Train"]+'/'+i
				elif filetype=='test':
					label_file_path=self.conf["DATA_PATH"]["Label_Test"]+'/'+i
				with open(label_file_path,'r') as f:
					#print filetype,label_file_path 
					for line in f:
						ispositive="1"
						'''
						name=line.strip().split('\t')[1]
						if len(line.strip().split('\t'))>=3:
							ispositive=line.strip().split('\t')[2]
						'''
						name=line.strip().split('\t')[0]
						if len(line.strip().split('\t'))>=2:
							ispositive=line.strip().split('\t')[1]
						if filetype=='train':
							self.label_dict[name]=label2num_dict[labelname]
						elif filetype=='test':
							self.label_dict[name]=[label2num_dict[labelname],ispositive]

	
	def generate_train_test_data(self):
		self.load_feature("FUSED_FEATURE")
		#print len(self.Feature_Dict_Dict["FUSED_FEATURE"])
		self.load_label_dict_by_folder("train")
		train_file_path=self.conf["DATA_PATH"]["Train_File"]
		#print len(self.label_dict)
		with open(train_file_path,'w') as f:
			#for key in self.Feature_Dict_Dict["FUSED_FEATURE"]:
			for key in self.final_feature_dict:
				if key in self.label_dict:
					#f.write(self.Serialization_feature_list2(self.label_dict[key],self.Feature_Dict_Dict["FUSED_FEATURE"][key]))
					f.write(self.Serialization_feature_list2(self.label_dict[key],self.final_feature_dict[key]))
		self.load_label_dict_by_folder("test")
		#print len(self.label_dict)
		test_file_path=self.conf["DATA_PATH"]["Test_File"]
		test_label_path=self.conf["DATA_PATH"]["Test_Label_File"]
		f=open(test_file_path,'w')
		g=open(test_label_path,'w')
		#for key in self.Feature_Dict_Dict["FUSED_FEATURE"]:
		for key in self.final_feature_dict:
			if key in self.label_dict:
				#f.write(self.Serialization_feature_list2(self.label_dict[key][0],self.Feature_Dict_Dict["FUSED_FEATURE"][key]))
				f.write(self.Serialization_feature_list2(self.label_dict[key][0],self.final_feature_dict[key]))
				g.write(key+'\t'+str(self.label_dict[key][0])+'\t'+self.label_dict[key][1]+'\n')
		f.close()
		g.close()

	#加载idf词典
	def load_idf_dict(self):
		d={}
		idf_dict_name=self.conf["DATA_PATH"]["Idf_Data"]
		#print idf_dict_name
		with open(idf_dict_name,'r') as gg:
			for line in gg:
				#print line 
				data=line.strip().split()
				word_id=int(data[0])
				query=data[1].strip()
				idf=float(data[3].strip())
				d[query]=[word_id,idf]
		return d

	def load_urlidf_dict(self):
		d={}
		idf_dict_name=self.conf["DATA_PATH"]["Url_Idf_Data"]
		#print idf_dict_name
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
	#@profile
	def load_idf_dict_with_stopword(self):
		idf_dict_name=self.conf["DATA_PATH"]["Idf_Data"]
		stopword_file_list=self.get_required_folder_name(self.conf["DATA_PATH"]["Stopword"],'stopword')
		stopword_dict={}
		for stopword_dict_name in stopword_file_list:
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
		'''
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
		'''
		with open(idf_dict_name,'r') as gg:
			for line in gg:
				word_id=int(line.strip().split()[0])
				query=line.strip().split()[1].strip()
				idf=float(line.strip().split()[3].strip())
				if query in stopword_dict and stopword_dict[query]==1:
					idf=0
				d[query]=[word_id,idf]
		return d
	#序列化特征列表	
	def Serialization_feature_list(self,name,featurelist):
		string=''
		if name=='':
			return string
		string=name+'\t'
		for i in featurelist:
			string=string+(str(i[0][0])+':'+str(i[1])+' ')
		string+='\n'
		return string
	#序列化特征列表
	def Serialization_feature_list2(self,name,featurelist):
		string=''
		if name=='':
			return string
		string=str(name)+'\t'
		for i in featurelist:
			string=string+(str(i[0])+':'+str(i[1])+' ')
		string+='\n'
		return string

	#按行读取切词之后的搜索信息并计算tfidf特征
	def read_segfile_tfidf_calculate(self):
		segfile_name=self.conf["DATA_PATH"]["Seg_File_Data"]
		feature_file=self.conf["DATA_PATH"]["TFIDF"]
		f=open(feature_file,'w')
		count=0
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
				elif data[0].strip()=='end':
					Ltitle.sort(key=lambda x:x[0])
					Lcontent.sort(key=lambda x:x[0])
					L_feature=self.tfidf_calculate_and_print([Ltitle,Lcontent,Lurl])
					#self.print_feature_perquery(name,L_feature)
					f.write(self.Serialization_feature_list(name,L_feature))
					count+=1
					print (count)
					if count%10000==0:
						print ('finished tfidf record num', count)
		f.close()
					
	#tfidf特征计算
	# input:seg_info_dict,conf,idf_dict
	# output:tfidf_feature_dict
	def tfidf_calculate_and_print(self,L):
		tfidf_dict={}
		self.idf_dict=self.Feature_Manager["TFIDF"]["Element_Dict"]
		for i in L[0]:
			if int(i[0])>20:
				continue
			tfidf_dict=self.__dict_plus_with_rank(tfidf_dict,Counter(i[1].strip().split()),self.conf["TFIDF_TITLE_RANK"][int(i[0])-1],self.idf_dict)
			#for key in self.Feature_Manager["TFIDF"]["Element_Dict"]:
			#	print key,self.Feature_Manager["TFIDF"]["Element_Dict"][key]
			#tfidf_dict=self.__dict_plus_with_rank(tfidf_dict,Counter(i[1].strip().split()),self.conf["TFIDF_TITLE_RANK"][int(i[0])-1],self.Feature_Manager["TFIDF"]["Element_Dict"])
		for i in L[1]:
			if int(i[0])>20:
				continue
			tfidf_dict=self.__dict_plus_with_rank(tfidf_dict,Counter(i[1].strip().split()),self.conf["TFIDF_CONTENT_RANK"][int(i[0])-1],self.idf_dict)
		LL=[]
		#print self.idf_dict
		#print len(self.Feature_Manager["TFIDF"]["Element_Dict"])
		for word in tfidf_dict:
			if word in self.idf_dict:
				LL.append([self.idf_dict[word],tfidf_dict[word]])
		LL.sort(key=lambda x:x[0])
		return LL



	#按行读取切词之后的搜索信息并计算url特征
	def read_segfile_url_calculate(self):
		segfile_name=self.conf["DATA_PATH"]["Seg_File_Data"]
		feature_file=self.conf["DATA_PATH"]["URL"]
		f=open(feature_file,'w')
		count=0
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
				elif data[0].strip()=='url':
					rank=int(data[1].strip())
					url=''
					if len(data)>=2:
						url=data[2]
					Lurl.append([rank,url])
				elif data[0].strip()=='end':
					Lurl.sort(key=lambda x:x[0])
					L_feature=self.url_calculate_and_print([Ltitle,Lcontent,Lurl])
					#self.print_feature_perquery(name,L_feature)
					f.write(self.Serialization_feature_list(name,L_feature))
					count+=1
					if count%10000==0:
						print ('finished url record num',count)
		f.close()
	
	#url特征计算
	def url_calculate_and_print(self,L):
		tfidf_dict={}
		self.url_idf_dict=self.Feature_Manager["URL"]["Element_Dict"]
		for i in L[2]:
			if int(i[0])>20:
				continue
			#print len(self.url_idf_dict)
			#print Counter(i[1].strip().split())
			#print self.conf["URL_RANK"][int(i[0])-1]
			tfidf_dict=self.__dict_plus_with_rank(tfidf_dict,Counter(i[1].strip().split()),self.conf["URL_RANK"][int(i[0])-1],self.url_idf_dict)
		LL=[]
		for word in tfidf_dict:
			if word in self.url_idf_dict:
				LL.append([self.url_idf_dict[word],tfidf_dict[word]])
		LL.sort(key=lambda x:x[0])
		return LL
		#print len(self.url_feature_dict)

	#每个query特征合并在一起
	def feature_fuse(self):
		id_base=[0]
		with open(self.conf["DATA_PATH"]["FEATURE_ID_MEAN"],'w') as ff:
			count_feature=0
			for key in sorted(self.conf["FEATURE_ENABLE"]):
				if int(self.conf["FEATURE_ENABLE"][key])>0:
					temp_L=[]
					self.Feature_Manager[key]["Element_Dict"]=self.Feature_Manager[key]["Element_Load_Func"]()
					for query in self.Feature_Manager[key]["Element_Dict"]:
						temp_L.append([self.Feature_Manager[key]["Element_Dict"][query][0]+id_base[count_feature],query])
					temp_L.sort()
					for i in temp_L:
						#print type(i[1]),type(key.encode('utf8')),type(str(i[0]))
						string=str(i[1])+'\t'+str(key.encode('utf8'))+'\t'+str(i[0])+'\n'
						#print (string)
						ff.write(string)
						#ff.write('\t'.join([i[1].decode('utf8'),key.decode('utf8'),str(i[0])]))
						#print i[1],key,i[0]
						#print query,self.Feature_Manager[key]["Element_Dict"][query][0]+id_base[count_feature]
					id_base.append(len(self.Feature_Manager[key]["Element_Dict"])+id_base[count_feature])
					count_feature+=1
		
		for key in sorted(self.conf["FEATURE_ENABLE"]):
			if int(self.conf["FEATURE_ENABLE"][key])>0 and key in self.Feature_Manager:
				#print key
				self.load_feature(key)
				self.feature_calculated_list.append(self.Feature_Manager[key]["Feature_Dict"])
				#self.feature_calculated_list.append(self.Feature_Dict_Dict[key])
		#if len(self.feature_calculated_list)==1:
		#	self.final_feature_dict=self.feature_calculated_list[0]
		#	return
		keyset=set()
		count_feature_max=[None]*len(self.feature_calculated_list)
		#默认feature的location从小到大排序
		for count in range(len(self.feature_calculated_list)):
			for key in self.feature_calculated_list[count]:
				#print key
				keyset.add(key)
				#print key
				#count_feature_max[count]=max(self.feature_calculated_list[count][key][-1][0],count_feature_max[count])
				if count>0:
					#for i in self.feature_calculated_list[count][key]:
					#	print i
					#print count_feature_max[count-1]
					#self.feature_calculated_list[count][key]=[[(i[0]+count_feature_max[count-1]),i[1]] for i in self.feature_calculated_list[count][key]]
					self.feature_calculated_list[count][key]=[[(i[0]+id_base[count]),i[1]] for i in self.feature_calculated_list[count][key]]
		for key in keyset:
			if key=='':
				continue
			self.final_feature_dict[key]=[]
			for i in self.feature_calculated_list:
				#print 'test',key,key in i,key in self.final_feature_dict
				if key in i:
					self.final_feature_dict[key]+=i[key]
		fused_featurefile=self.conf["DATA_PATH"]["FUSED_FEATURE"]
		with open(fused_featurefile,'w') as f:
			for key in self.final_feature_dict:
				f.write(self.Serialization_feature_list2(key,self.final_feature_dict[key]))
				
		
	#打印计算后的feature
	def print_feature(self,d):
		#for key in self.final_feature_dict:
		for key in d:
			if key=='':
				continue
			print (key,)
			for i in d[key]:
				#print i
				#print str(i[0])+':'+str(i[1]),
				#优化内存使用format
				print ('{0}:{1}'.format(i[0],i[1]),)
				pass
			print ('')
		return
	
	def print_feature_perquery(self,name,featurelist):
		if name=='':
			return 
		print (name+'\t',)
		for i in featurelist:
			print (str(i[0][0])+':'+str(i[1]),)
		print ('')
		return 
	
	#打印计算后的feature及其相关含义
	def print_feature_with_meaning(self):
		return 

	#加载计算好的feature
	def load_feature(self,feature_name):
		d={}
		if feature_name in self.conf["DATA_PATH"]:
			feature_file=self.conf["DATA_PATH"][feature_name]
		else:
			return 
		with open(feature_file,'r') as gg:
			for line in gg:
				#print line
				data=line.strip().split()
				if len(data)<2:
					continue
				L=[]
				if len(data)>1:
					for i in data[1:]:
						#print i
						L.append([int(i.split(':')[0]),float(i.split(':')[1])])
				d[data[0]]=L
		if feature_name in self.Feature_Manager and feature_name != "FUSED_FEATURE":
			self.Feature_Manager[feature_name]["Feature_Dict"]=d
		elif feature_name not in self.Feature_Manager and feature_name == "FUSED_FEATURE":
			self.final_feature_dict=d
		#self.tfidf_feature_dict[data[0]]=L
		#print self.Feature_Dict_Dict[feature_name]
		
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
	
	def modelinfo_generate(self):
		with open(self.conf["DATA_PATH"]["Trained_model"],'r') as f:
			ff=f.readlines()
			FEATURE_NUM=int(ff[2].strip().split()[0])
			CLASS_NUM=int(ff[1].strip().split()[0])
			data=ff[14].strip().split()
		LL=[]
		with open(self.conf["DATA_PATH"]["FEATURE_ID_MEAN"],'r') as g:
			gg=g.readlines()
			if len(gg)!=int(gg[-1].strip().split('\t')[2]):
				print ('test')
				print ('feature length error!')
				return
			if len(gg)<FEATURE_NUM:
				print ('feature length error!')
				return
			for count in xrange(len(gg)):
				LL.append(CLASS_NUM*[0])
			for di in data[2:-1]:
				index=int(di.strip().split(":")[0])
				weight=float(di.strip().split(":")[1])
				if index%len(gg)==0:
					x=len(gg)-1
				else:
					x=index%len(gg)-1
				#print x,index/len(gg),len(LL[x]),LL[x]
				LL[x][index/len(gg)]=weight
		with open(self.conf["DATA_PATH"]["Modelinfo"],'w') as g:
			for i,vi in enumerate(LL):
				string=''
				#print gg[i].strip().split('\t')[0],
				temp=gg[i].strip().split('\t')[0].strip()
				string+=(temp+'\t')
				for j in vi:
					#print j,
					string+=(str(j)+'\t')
				string=string[0:-1]+'\n'
				#print string
				g.write(string)
					
					
	def result_analyze(self):
		#label编号
		label2num_dict={}
		count=1
		for key in sorted(self.conf["CLASS_ENABLE"]):
			#print key,'test2'
			if (self.conf)["CLASS_ENABLE"][key]>0:
				label2num_dict[key]=count
				count+=1
		label2num_dict_reverse= { str(value):key for key,value in label2num_dict.items()}
		outputpath=self.conf["DATA_PATH"]["Output"]
		test_label_path=self.conf["DATA_PATH"]["Test_Label_File"]
		f=open(outputpath,'r')
		g=open(test_label_path,'r')
		ff=f.readlines()
		gg=g.readlines()
		if len(ff)!=len(gg):
			print ('length error')
			return
		deresult={}
		for key in label2num_dict_reverse:
			deresult[key]=[0,0,0,0]#TP,TN,FP,FN
		for count in range(len(ff)):
			prediction=ff[count].strip().split()[0]
			label=gg[count].strip().split('\t')[1]
			ispositive=gg[count].strip().split('\t')[2]
			if prediction==label and ispositive=='1':
				deresult[label][0]+=1
			elif prediction!=label and ispositive=='0':
				deresult[label][1]+=1
			elif prediction==label and ispositive=='0':
				deresult[label][2]+=1
				if label2num_dict_reverse[label]=='mus':
					#print gg[count].strip().split('\t')[0],label2num_dict_reverse[prediction],ff[count].strip()
					pass
			elif prediction!=label and ispositive=='1':
				if label2num_dict_reverse[label]=='mus':
					'''
					for key in sorted(label2num_dict):
						print key,
					print ''
					'''
					#print gg[count].strip().split('\t')[0],label2num_dict_reverse[prediction],ff[count].strip()
					pass
				deresult[label][3]+=1
		for key in deresult:
			if deresult[key]==[0,0,0,0]:
				continue
			sumal=0
			for i in deresult[key]:
			   sumal+=i
			print (label2num_dict_reverse[key])
			precision=float(deresult[key][0])/(deresult[key][0]+deresult[key][2])
			recall=float(deresult[key][0])/(deresult[key][0]+deresult[key][3])
			print ('precision',round(precision,3),'recall',round(recall,3))

		f.close()
		g.close()

	'''
	def feature_calculate(self):
		for key in self.conf['FEATURE_ENABLE']:
			if int(self.conf['FEATURE_ENABLE'][key])>0:
				self.Feature_Function_Dict[key]()
	'''
	def __init__(self):

		#全局配置文件
		self.conf={}
		self.label_dict={}

		#分词后的百度检索信息
		self.seg_info_dict={}

		#tfidf特征的参数
		#self.tfidf_max_index=0
		self.idf_dict={} 
		self.tfidf_feature_dict={} 

		#url特征参数
		#self.url_max_index=0
		self.url_idf_dict={} 
		self.url_feature_dict={} 

		self.feature_calculated_list=[]
		self.final_feature_dict={} 

		#配置函数字典
		'''
		self.Feature_Function_Dict={
			'TFIDF':self.tfidf_calculate,
			'URL':self.url_calculate
		}
		self.Element_Dict={
			'TFIDF':self.idf_dict
			'URL':self.url_idf_dict
		}
		self.Feature_Dict_Dict={
			'TFIDF':self.tfidf_feature_dict,
			'URL':self.url_feature_dict,
			'FUSED_FEATURE':self.final_feature_dict
		}
		'''

		self.Feature_Manager={
			'TFIDF':{
						"Element_Dict":self.idf_dict,
						"Element_Load_Func":self.load_idf_dict_with_stopword,
						"Feature_Dict":self.tfidf_feature_dict,
						"Feature_Calc_Func":self.read_segfile_tfidf_calculate
					},
			'URL':	{
						"Element_Dict":self.url_idf_dict,
						"Element_Load_Func":self.load_urlidf_dict,
						"Feature_Dict":self.tfidf_feature_dict,
						"Feature_Calc_Func":self.read_segfile_url_calculate
					}
		}

		self.Command_Register={
			'TFIDF':self.TFIDF_Calculate,
			'URL':self.URL_Calculate,
			'FEATURE_ENABLE_EXPLAIN':self.Feature_Enable_Explain,
			'FUSE':self.feature_fuse,
			'LABEL':self.generate_train_test_data,
			'ANALYZE':self.result_analyze,
			'MODEL_GEN':self.modelinfo_generate
		}

	def TFIDF_Calculate(self):
		self.Feature_Manager["TFIDF"]["Element_Dict"]=self.Feature_Manager["TFIDF"]["Element_Load_Func"]()
		#print self.Feature_Manager["TFIDF"]["Element_Dict"]
		self.Feature_Manager["TFIDF"]["Feature_Calc_Func"]()
		#self.idf_dict=self.load_idf_dict_with_stopword()
		#self.read_segfile_tfidf_calculate()
	def URL_Calculate(self):
		self.Feature_Manager["URL"]["Element_Dict"]=self.Feature_Manager["URL"]["Element_Load_Func"]()
		self.Feature_Manager["URL"]["Feature_Calc_Func"]()
		#self.url_idf_dict=self.load_urlidf_dict()
		#self.read_segfile_url_calculate()
	def Feature_Enable_Explain(self):
		for i in self.conf["FEATURE_ENABLE"]:
			if self.conf["FEATURE_ENABLE"][i]>0:
				print (i,)
		print ('')
		return
	
	def Commanding(self,conf_file_name,command):
		self.read_conf(conf_file_name)
		#print 'test'
		self.Command_Register[command]()
		'''
		self.idf_dict=self.load_idf_dict()
		self.read_segfile_tfidf_calculate()
		self.url_idf_dict=self.load_urlidf_dict()
		self.read_segfile_url_calculate()
		'''
		#print self.tfidf_feature_dict
		#print self.Feature_Dict_Dict["TFIDF"]
		#self.print_feature(self.Feature_Dict_Dict["TFIDF"])
		#self.load_feature("URL")
		#self.load_feature("TFIDF")
		#print 'test',self.Feature_Dict_Dict["URL"]
		#self.print_feature(self.Feature_Dict_Dict["URL"])
		#self.feature_fuse()
		#self.generate_train_test_data()
		#for key in self.label_dict:
		#	print key,self.label_dict[key]
		#self.print_feature(self.Feature_Dict_Dict["URL"])
		#self.print_feature(self.Feature_Dict_Dict["TFIDF"])
		#self.print_feature(self.final_feature_dict)
		#for key in self.url_idf_dict:
		#	print key,self.url_idf_dict[key]

if __name__=='__main__':
	'''
	conf_file_name=sys.argv[1]
	tfidf_dict_name=sys.argv[2]
	url_dict_name=sys.argv[3]
	segfile_name=sys.argv[4]
	stopword_dict_name=sys.argv[5]
	label_dict_name=sys.argv[6]
	Calculate().auto_procedure(conf_file_name,tfidf_dict_name,url_dict_name,segfile_name,stopword_dict_name,label_dict_name)
	'''
	if len(sys.argv)!=3:
		print ('input error!')
		sys.exit()
	conf_file_name=sys.argv[1]
	command_string=sys.argv[2]
	Calculate().Commanding(conf_file_name,command_string)
