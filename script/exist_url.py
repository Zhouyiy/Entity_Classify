# -*- coding: utf-8 -*-
# git test
# git test2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import redis
import urllib
import json
s = set()
from urllib import urlencode

client =redis.Redis(host='140.143.185.78',port=6666,db=0)
key = 'bd:start_urls'
print client.exists(key)


