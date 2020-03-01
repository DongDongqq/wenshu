# -*- coding: utf-8 -*-
"""
    @author: 王帅帅
    @project: zhuanlihui
    @file: put_id_rebbit.py
    @time: 2019/11/15/016 15:45
    @desc:
"""
import pika, arrow, time,requests
from pymongo import MongoClient
from bson.objectid import ObjectId


conMongo = MongoClient(host="192.168.1.123", port=27017)
collections = conMongo['wss_caipan']


def star():
    queue = "wss_caipan"
    credentials = pika.PlainCredentials("pig444", "1234as")
    connection = pika.BlockingConnection(pika.ConnectionParameters("192.168.1.157", 5672, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    collections = conMongo[queue].list_collection_names()
    today = arrow.now().shift(days=-1).format("YYYY-MM-DD")
    if today not in collections:
        col = conMongo[queue][today]
        col.create_index([("wenshu_id", 1)], unique=True)
    print(today)
    data = conMongo[queue]['wss_wenshuid'].find({'create_at':today}).batch_size(300)
    count = conMongo[queue]['wss_wenshuid'].find({'create_at':today}).count()
    for i in data:
        del i['_id']
        message = str(i)
        channel.basic_publish(exchange='',routing_key=queue, body=message, properties=pika.BasicProperties(delivery_mode=2))
    connection.close()
    data = {"user": "Deng", "content": "裁判文书ID上传成功,数量总共%s"%count}
    res = requests.post("http://192.168.1.157:5002/alert/notice", data=data)


if __name__ == '__main__':
    star()