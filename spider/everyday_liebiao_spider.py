from spider.function import *
import pika, time

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


def get_data(cookie, baseurl, S, queryCondition):
    global proxy
    data = {
        'facetLimit': '2000',
        'groupFields': S,
        'queryCondition': '[{"key":"cprq","value":"%s TO %s"}]' % (queryCondition, queryCondition),
        'cfg': 'com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@leftDataItem',
        '__RequestVerificationToken': get_token()
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Length': '194',
        'content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'wenshu.court.gov.cn',
        'Origin': 'http://wenshu.court.gov.cn',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html',
        'Connection': 'close',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Cookie': 'HM4hUBT0dDOn80S=TwreMojvHWI4WoJB4VgVv_salJWmc.kx3bJsjCQdBqK7PRMVpFaFGCPj_7diKwxq; HM4hUBT0dDOn80T=%s; ' % cookie
    }
    while True:
        try:
            resp = requests.post(url=baseurl, headers=headers, data=data, proxies=proxy, timeout=10).json()
            data_list = resp['result'][S]
            daihao_list = []
            sum = 0
            for i in data_list:
                daihao_dict = {}
                daihao_dict['value'] = i['value']
                daihao_dict['count'] = i['count']
                daihao_dict['daihao'] = data['groupFields']
                daihao_dict['query'] = queryCondition
                if i['count'] <= 1000:
                    sum += i['count']
                    daihao_list.append(str(daihao_dict))
            print(sum, S,)
            return daihao_list
        except Exception as e:
            print(e)
            cookie, baseurl = get_url()
            proxy = get_proxy()
        except requests.exceptions.ConnectionError as r:
            r.status_code = "Connection refused"
            proxy = get_proxy()


def start():
    global proxy
    queue = "wss_everyday_wenshu"
    # times = arrow.now().shift(days=-1).format("YYYY-MM-DD")
    credentials = pika.PlainCredentials("pig444", "1234as")
    connection = pika.BlockingConnection(pika.ConnectionParameters("192.168.1.157", 5672, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    # proxy = get_proxy()
    '''''s11', 's12', 's13', 's14', 's15', 's16','''
    '''3-27'''
    num_list = ['s11','s12', 's13', 's14', 's15', 's16','s17']
    # 4月份10号-20号
    for month in range(1, 10):
        for time_i in range(1, 32):
            for num in num_list:
                times = '2019-0%s-0%s' % (month, time_i) if time_i <= 9 else '2019-0%s-%s' % (month, time_i)
                # times = '2020-0%s-0%s' % (month, time_i) if time_i <= 9 else '2020-0%s-%s' % (month, time_i)

                print(times)
                cookie, baseurl = get_url()
                daihao_list = get_data(cookie, baseurl, num, times)
                print(daihao_list)
                for i in list(set(daihao_list)):
                    channel.basic_publish(exchange='', routing_key=queue, body=i, properties=pika.BasicProperties(delivery_mode=2))
    print(" [x] Sent 成功")
    connection.close()
    # db[times].create_index([("wenshu_id", 1)], unique=True)


if __name__ == '__main__':
    proxy = get_proxy()
    start()