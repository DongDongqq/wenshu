
from spider.function import *
from pymongo.errors import *
import time, pika, arrow, base64, json


def get_data(cookie,baseurl,daihao):
    global proxy,ciphertext
    pageNum =  1
    all_list = []
    headers = {
        'content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'close',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Cookie': 'HM4hUBT0dDOn80S=TwreMojvHWI4WoJB4VgVv_salJWmc.kx3bJsjCQdBqK7PRMVpFaFGCPj_7diKwxq; HM4hUBT0dDOn80T=%s; ' % cookie
    }

    data = {
        'sortFields': 's50:desc',
        'ciphertext': '',
        'pageNum': '1',
        'pageSize': str(daihao['count']),
        'queryCondition': '[{"key":"cprq","value":"%s TO %s"},{"key":"%s","value":"%s"}]' % (daihao['query'], daihao['query'], daihao['daihao'], daihao['value']),
        'cfg': 'com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc'}
    data['ciphertext'] = ciphertext

    try:
        response = requests.post(url=baseurl, headers=headers,data=data, proxies=proxy, timeout=5)
        print(response)
        resp = response.json()
        result = resp['result']
        Key = resp['secretKey']
        last_data = get_result(result, Key, time.strftime("%Y%m%d"))
        last_data = json.loads(last_data)
        print(last_data)
        if last_data['relWenshu']:
            id_list = list(last_data['relWenshu'].keys())
            data_list = []
            for i in id_list:
                data1 = {}
                data1['wenshu_id'] = i
                print(i)
                all_list.append(data1)
                data_list.append(data1)
            try:
                db.wss_wenshuid.insert_many(data_list)
            except BulkWriteError as D:
                pass
            return {
                'status': 1,
                'content': '获取信息成功',
            }
        else:
            return {
                'status': 1,
                'content': '没有信息'
            }
    except requests.exceptions.ConnectionError as r:
        r.status_code = "Connection refused"
        proxy = get_proxy()
        return {
            'status': 0,
            'content': r
        }
    except Exception as e:
        proxy = get_proxy()
        return {
            'status': 0,
            'content': e
        }


def start(pidName):
    cookie, baseurl = get_url()
    queue = 'wss_wenshu'
    credentials = pika.PlainCredentials('pig444', '1234as')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        '192.168.1.157', 5672, '/', credentials, heartbeat=2000))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    def callback(ch, method, properties, body):
        data_id = eval(body)
        print('查询信息：', data_id)
        print(data_id)
        try:
            check = get_data(cookie,baseurl,data_id)
            print(check)
            if check['status'] == 0:
                ch.basic_nack(delivery_tag=method.delivery_tag)
                return
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
        except AttributeError:
            # redis 中 cookie 完了
            print("redis队列为空：AttributeError")
            channel.close()

    # 公平调度
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue, callback)
    channel.start_consuming()


if __name__ == '__main__':
    proxy = get_proxy()
    ciphertext = get_ciphertext()
    start(1)
