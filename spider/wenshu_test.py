#-*-coding:utf-8-*-
from spider.function import *
from pymongo.errors import *
from bson.objectid import ObjectId


# data = db.wss_wenshuid_test.remove({'_id': {'$lt': ObjectId("5dce2f19a6cf11603991c84f")}})
# print(data)
collection = db['2019-10-24_detail'].find()

for i in collection:
    del i['_id']
    print(i['wenshu_id'])
    try:
        db['wen_details'].insert(i)
    except DuplicateKeyError as e:
        pass