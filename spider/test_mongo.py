#-*-coding:utf-8-*-
from spider.function import *


collection_123 = db['wenshu_personal']

my_collection = GS_db['judgment']


# info = my_collection.create_index([("caseno", 1)], background=True)
info = collection_123.create_index({ 'caseno': "hashed" }, background=True)

print(info)
