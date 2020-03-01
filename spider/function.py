
"""
    @author: 王帅帅
    @project: yingyongbao
    @file: function.py
    @time: 2019/7/18/018 18:09
    @desc:
"""
import redis,requests,execjs, arrow, base64
from pymongo import MongoClient
from pycrypto_code import encrypt
from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad


def conRedis():
    return redis.Redis(host='192.168.1.157', port=6379)

redis_client = conRedis()


def conMongo():
    conMongo = MongoClient(host='192.168.1.123', port=27017)
    return conMongo


def zhengshi_Mongo():
    conMongo =  MongoClient(host='47.99.242.139',port=27017, username='web', password='1234as', authSource='ngsxt')
    return conMongo


db = conMongo()['wss_caipan']
GS_db = zhengshi_Mongo()['ngsxt']

def get_ip():
    ip = redis_client.brpop('qcc_guanxi_proxy', 0)[1]
    ip = ip.decode('utf-8')
    proxy = {"http": "http://pig444:1234as@"+ip,"https": "https://pig444:1234as@"+ip}
    print('ip地址：', ip)
    return ip


def get_proxy():
    ip = redis_client.brpop('wss_wenshu_proxy', 0)[1]
    ip = ip.decode('utf-8')
    proxy = {"http": "http://pig444:1234as@"+ip,"https": "https://pig444:1234as@"+ip}
    # proxy = {"http": 'http://' + ip, "https": 'https://' + ip}
    print('ip地址：', ip)
    return proxy


def get_ciphertext():
    with open('../demo.js') as fp:
        js = fp.read()
    context = execjs.compile(js)
    vl5x = context.call('cipher')
    timestamp = vl5x['timestamp']
    salt = vl5x['salt']
    iv = arrow.now().format('YYYYMMDD')
    enc = encrypt(timestamp, salt, iv)
    str = salt + iv + enc
    ciphertext = context.call('strTobinary', str)
    return ciphertext


def get_url():
    resp = requests.get(url='http://192.168.1.117:5000/getparam')
    main_data = resp.json()
    cookie = main_data['cookie']
    baseurl = main_data['url']
    return cookie,baseurl


def get_result(result,secretKey,date):
    des3 = DES3.new(key=secretKey.encode(), mode=DES3.MODE_CBC, iv=date.encode())
    decrypted_data = des3.decrypt(base64.b64decode(result))
    plain_text = unpad(decrypted_data, DES3.block_size).decode()
    return plain_text


def short_to_province(short):
    if short == "京":
        return "北京市"
    elif short == "津":
        return "天津市"
    elif short == "渝":
        return "重庆市"
    elif short == "沪":
        return "上海市"
    elif short == "冀":
        return  "河北省"
    elif short == "晋":
        return "山西省"
    elif short == "辽":
        return "辽宁省"
    elif short == "吉":
        return "吉林省"
    elif short == "黑":
        return "黑龙江省"
    elif short == "苏":
        return "江苏省"
    elif short == "浙":
        return "浙江省"
    elif short == "皖":
        return "安徽省"
    elif short == "闽":
        return "福建省"
    elif short == "赣":
        return "江西省"
    elif short == "鲁":
        return "山东省"
    elif short == "豫":
        return "河南省"
    elif short == "鄂":
        return "湖北省"
    elif short == "湘":
        return "湖南省"
    elif short == "粤":
        return "广东省"
    elif short == "琼":
        return "海南省"
    elif short == "川"or short == "蜀":
        return "四川省"
    elif short == "黔"or short == "贵":
        return "贵州省"
    elif short == "云"or short == "滇":
        return "云南省"
    elif short == "陕"or short == "秦":
        return "陕西省"
    elif short == "甘"or short == "陇":
        return "甘肃省"
    elif short == "青":
        return "青海省"
    elif short == "台":
        return "台湾省"
    elif short == "蒙":
        return "内蒙古自治区"
    elif short == "桂":
        return "广西壮族自治区"
    elif short == "宁":
        return "宁夏回族自治区"
    elif short == "新":
        return "新疆维吾尔自治区 "
    elif short == "藏":
        return "西藏自治区"
    elif short == "港":
        return "香港特别行政区"
    elif short == "澳":
        return "澳门特别行政区"
    else:
        return ''



if __name__ == '__main__':
    get_proxy()


















