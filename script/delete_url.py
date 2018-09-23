# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import redis

client =redis.Redis(host='140.143.185.78',port=6666,db=0)
key = 'bd:start_urls'
client.delete(key)
print "delete successfully"


