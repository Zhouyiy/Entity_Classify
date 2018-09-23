import sys 
import os
import re
import json
import urllib.request
#reload(sys) 
#sys.setdefaultencoding('utf8')
sys.path.append('./pythonlib')

f_main=open(sys.argv[1],"r")
fm=f_main.readlines()
#temp_file=open('temp_file','w')
#L_resgister=['rank','title','content','url','items','tags']
#multi_seg_dict_path=sys.argv[2]
def json_explain(fm):
    d={}
    dd={}
    #wd={}
    #for lines in fs:
    #    data=lines.strip().split()
    #    if len(data)>1:
    #        wd[data[0].decode('utf8')]=1
    for linem in fm:
        d=json.loads(linem)
        #proto, rest = urllib.request.urlretrieve(d['url'])
        #print (rest)
        #res, rest = urllib.splithost(rest)
        #d['url']=res
        d['url']=""
        if d["query"] not in dd:
            dd[d["query"]]=[]
            #dd[d["query"]].append([int(d['rank'].strip()),d["title"].strip(),d["content"].strip(),d['url'].strip()])
            main_name=re.sub("[()]","",d["query"])
            dd[d["query"]].append([int(d['rank'].strip()),re.sub(main_name,"",d["title"].strip()),re.sub(main_name,"",d["content"].strip()),d['url'].strip()])
            if "items" in d:
                dd[d["query"]][-1].append(d["items"])
            if "tags" in d:
                dd[d["query"]][-1].append(d["tags"])
        else: 
            L=[] 
            for i in dd[d['query']]:
                L.append(int(i[0]))
            if int(d['rank']) not in L:
                #dd[d["query"]].append([int(d['rank'].strip()),d["title"].strip(),d["content"].strip(),d['url'].strip()])
                main_name=re.sub("[()]","",d["query"])
                dd[d["query"]].append([int(d['rank'].strip()),re.sub(main_name,"",d["title"].strip()),re.sub(main_name,"",d["content"].strip()),d['url'].strip()])
                if "items" in d:
                    dd[d["query"]][-1].append(d["items"])
                if "tags" in d:
                    dd[d["query"]][-1].append(d["tags"])
    for key in dd:
        L=dd[key]
        L.sort()
        print ('start'+'\t'+'start')
        print ('query'+'\t'+key) 
        #temp_file.write('query'+'\t'+key+'\n')
        for i in L:
            if len(i)>4:#contain the tags and items
                print ('title'+'\t'+str(i[0])+'\t'+i[1]+list2str(i[4])+list2str(i[5]))
            else:
                print ('title'+'\t'+str(i[0])+'\t'+i[1])
            print ('content'+'\t'+str(i[0])+'\t'+i[2])
            print ('url'+'\t'+str(i[0])+'\t'+i[3])
            if len(i)>4:
                pass
        print ('end'+'\t'+'end')
                #print type(list2str(i[4]))
                #print 'items'+'\t'+str(i[0])+'\t'+list2str(i[4])
                #print 'tags'+'\t'+str(i[0])+'\t'+list2str(i[5])
            #temp_file.write('title'+'\t'+str(i[0])+'\t'+i[1]+'\n')
            #temp_file.write('content'+'\t'+str(i[0])+'\t'+i[2]+'\n')
    #print 'start'
    #os.system('../../tools/wordseg_multi ../../tools/dict/ 1 < temp_file > 3')
    return 

def list2str(L):
    #print L
    string=''
    for i in L:
        #print i
        #print type(i)
        #print type(i.encode('unicode-escape').decode('string_escape'))
        #print type(string)
        #string+=i.encode('unicode-escape').decode('string_escape'),
        string+=str(i)
    return string

json_explain(fm)
f_main.close()
#temp_file.close()
