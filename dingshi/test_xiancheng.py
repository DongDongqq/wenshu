#-*-coding:utf-8-*-
import arrow, requests, time
from pymongo import MongoClient, UpdateOne, InsertOne
from spider.function import *
from queue import Queue
from pymongo.errors import *
from bson import ObjectId
import threading, traceback

all_queue = Queue()
mongo123 = MongoClient("mongodb://192.168.1.123:27017/").wss_caipan
mongo_save = MongoClient("mongodb://192.168.1.123:27017/").zgh_test
aliyun = MongoClient('mongodb://web:1234as@47.99.242.139:27017/ngsxt').ngsxt
red = redis.Redis(host='192.168.1.157', port=6379, db=0)


def huoqudata(times):
    data = mongo123[times].find({},{'wenshu_id':1}).batch_size(100).limit(10)
    for i in data:
        all_queue.put(i)


def shanchu():
    while True:
        data = all_queue.get()
        print(data)
        if all_queue.empty():
            time.sleep(10)
            if all_queue.empty():
                return data


if __name__ == '__main__':
    times = arrow.now().shift(days=-2).format("YYYY-MM-DD")
    hou = threading.Thread(target=huoqudata, args=(times,))
    hou.start()
    shan = threading.Thread(target=shanchu)
    shan.start()


