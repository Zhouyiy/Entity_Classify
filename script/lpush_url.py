# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import redis
import urllib
import json
s = set()
from urllib import urlencode
#
new=[]
file = open(sys.argv[1],'r')
for line in file.readlines():
    line = line[:-1]
    url = 'https://www.baidu.com/s?wd='+urllib.quote(line)
    s.add(url)

# client =redis.Redis(host='127.0.0.1',port=6666,db=0)
client =redis.Redis(host='140.143.185.78',port=6666,db=0)


## Stored data in list (lpush)

key = 'bd:start_urls'

for val in s:
    client.lpush(key,val)

print ('上传成功')
