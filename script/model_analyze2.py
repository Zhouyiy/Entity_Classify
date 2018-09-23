import sys
f=open(sys.argv[1],'r')#model
g=open(sys.argv[2],'r')#dict
ff=f.readlines()
gg=g.readlines()
d={}

FEATURE_NUM=int(ff[2].strip().split()[0])
#print FEATURE_NUM
CLASS_NUM=int(ff[1].strip().split()[0])
#print CLASS_NUM
L=[]
for i in range(CLASS_NUM):
	L.append([])

for line in gg:
	d[line.strip().split()[0]]=line.strip().split()[1]

data=ff[14].strip().split()
LL=[]
for i in range(FEATURE_NUM*CLASS_NUM+1):
	LL.append(0)
for i in data[2:-1]:
	index=int(i.strip().split(":")[0])
	weight=float(i.strip().split(":")[1])
	LL[index]=weight 

count=1
class_index=0
for i in LL[1:]:
	if count%FEATURE_NUM==0:
		L[class_index].append(LL[count])
		class_index+=1
		count+=1
	else:
		L[class_index].append(LL[count])
		count+=1

for count in range(FEATURE_NUM):
	print d[str(count+1)]+'\t',
	for class_count in range(CLASS_NUM):
		print L[class_count][count],
	print ''


                                        
