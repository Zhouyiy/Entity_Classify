import sys
for line in sys.stdin:
	string=""
	#print len(line.strip().split('\t')[1:])
	for i in line.strip().split('\t')[1:]:
		print i.strip()+'\t',
	print ''
	#print string 
