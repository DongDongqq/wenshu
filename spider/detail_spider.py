
from spider.function import *
from pymongo.errors import *
import pika, time, json

def get_token():
    js = """ function random(size){
            	var str = "",
            	arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
            	for(var i=0; i<size; i++){
            		str += arr[Math.round(Math.random() * (arr.length-1))];
            	}
            	return str;
            }
    """
    ctx = execjs.compile(js)
    result = ctx.call("random", "24")
    return result

data ={
    'cfg': 'com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch',
    '__RequestVerificationToken':  "%s" % get_token()
}


def get_data(doc_id):
    global proxy, ciphertext
    cookie, baseurl = get_url()
    headers = {
        'Connection': 'close',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Cookie': 'HM4hUBT0dDOn80S=TwreMojvHWI4WoJB4VgVv_salJWmc.kx3bJsjCQdBqK7PRMVpFaFGCPj_7diKwxq; HM4hUBT0dDOn80T=%s; ' % cookie
    }
    data['ciphertext'] = ciphertext
    data['docId'] = doc_id
    try:
        resp = requests.post(url=baseurl, headers=headers, data=data, proxies=proxy, timeout=30)
        print(resp.text,'*****')
        resp = resp.json()
        result = resp['result']
        Key = resp['secretKey']
        last_data = json.loads(get_result(result, Key, time.strftime("%Y%m%d")))
        mongo_dict = {}
        mongo_dict['data'] = last_data
        mongo_dict['wenshu_id'] = doc_id
        try:
            db['wen_details'].insert_one(mongo_dict)
        except DuplicateKeyError as D:
            pass
        return {
            'status': 1,
            'content': last_data,
        }
    except requests.exceptions.ConnectionError as r:
        r.status_code = "Connection refused"
        proxy = get_proxy()
        print(r)
        return {
            'status': 0,
            'content': '错误',
        }
    except Exception as e:
        print(e)
        proxy = get_proxy()
        return {
            'status': 0,
            'content': '错误',
        }


def start(pidName):
    queue = 'wss_caipan'
    credentials = pika.PlainCredentials('pig444', '1234as')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        '192.168.1.157', 5672, '/', credentials, heartbeat=2000))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)


    def callback(ch, method, properties, body):
        data_id = body.decode('utf-8')
        print('查询信息：', data_id)
        try:
            check = get_data(data_id)
            print(check)
            if check['status'] == 0:
                ch.basic_ack(delivery_tag=method.delivery_tag)
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
    channel.basic_consume(queue,callback)
    channel.start_consuming()


if __name__ == '__main__':
    proxy = get_proxy()
    ciphertext = get_ciphertext()
    # times = arrow.now().shift(days=-1).format("YYYY-MM-DD")
    start(1)
    # print(get_data('04b11a741b8a4886b9a2aaeb007ed68e'))