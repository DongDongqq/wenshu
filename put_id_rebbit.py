# -*- coding: utf-8 -*-
"""
    @author: 王帅帅
    @project: zhuanlihui
    @file: put_id_rebbit.py
    @time: 2019/8/16/016 15:45
    @desc:
"""

import pika
from spider.function import *
queue = "wss_wenshuID_test"
credentials = pika.PlainCredentials("pig444", "1234as")
connection = pika.BlockingConnection(pika.ConnectionParameters("192.168.1.157", 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue=queue, durable=True)



s11 = db['2019-10-24'].find().limit(10)
# s12 = db.wen_details.find().skip(1).limit(21740)
for i in list(s11):
    ID = i['wenshu_id']
    print(ID)
    # break
    channel.basic_publish(exchange='',
                      routing_key= queue,
                      body=ID)
print(" [x] Sent 成功")
connection.close()


# if __name__ == '__main__':
#     num = '201811655000'
#     print(parse_id(num))