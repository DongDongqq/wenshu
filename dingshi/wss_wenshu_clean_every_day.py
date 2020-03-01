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


key = False


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


def is_company(info):
    for name in info:
        if len(name) >= 5:
            return 'company'
    return 'person'


def exist_panduan(company_id, data_dic):
    if 's7' in data_dic:
        caseno = data_dic['s7']
    else:
        return False
    if caseno in ['（2019）粤0304执15382-15386、15388-15396、15398-15434、15436-15482、15484-15486、15488-15500、15502-15513、15515-15517、15519-15520、15522-15526、15528-15581号',
                  '（2019）粤0304执13267-13366号','（2019）粤0304执14256-14271、14273-14300、14302-14328、14330-14355号',
                  '（2019）粤03民终4573-4582、6218-6227、7997-8007、8045-8055、10808-10812、10815-10818号',
                  '（2019）粤0304执4130-4131、4133、4135-4153、4155-4158、4160-4198、4200-4211、4213-4216、4218-4221、4223-4230、4233-4243、4245-4254、4256-4260、4262-4273、4275-4280、4282-4283、4285-4288、4290-4306、4308-4316、4318-4329、4331-4358、4360-4364、4366-4379号']:
        if 's1' in data_dic:
            casename = data_dic['s1']
            data = list(aliyun.judgment.find({"company_id": company_id, 'casename': casename}, {'caseno': 1}))
            if data:
                print('存在', company_id, caseno)
                return False
            else:
                return True
    data = list(aliyun.judgment.find({"company_id": company_id, 'caseno': caseno}, {'caseno': 1}))
    if data:
        print('存在', company_id, caseno)
        return False
    else:
        return True


def clean():
    global key
    monitor_notice_list = []
    updateData = []
    save_list = []
    while True:
        item = all_queue.get()
        company_id_list = []
        try:
            party = item['data']['s17']
            wenshu_type = is_company(party)
            data_dic = item['data']
            company_info = {}
            if wenshu_type == "company":
                com_name = [i for i in party if len(i) >= 5 ]
                for com_name_i in com_name:
                    company_info = aliyun.company.find({'entname': com_name_i}, {'company_id': 1})       # 公司名搜索有可能会出现多条数据
                    if company_info.count() == 0:        # 数据库中没有某公司数据，将公司名存下，源数据写入另一个表，暂不清洗
                        item.pop('_id')
                        try:
                            obj_id = mongo123.searchNone_content.save(item)
                            mongo123.searchNone.insert_one({"wenshu_id": item['wenshu_id'], "wenshu_obj_id": obj_id})
                        except DuplicateKeyError as e:
                            pass
                        continue
                    else:
                        for com in company_info:
                            key = exist_panduan(com['company_id'], data_dic,)
                            if key:
                                company_id_list.append(com['company_id'])
            else:
                company_id_list.append("person")
            if not company_id_list:
                continue

            con_head = data_dic['s22'] if 's22' in data_dic else ""
            con_1 = data_dic['s23'] if 's23' in data_dic else ""
            con_2 = data_dic['s25'] if 's25' in data_dic else ""
            con_3 = data_dic['s26'] if 's26' in data_dic else ""
            con_4 = data_dic['s51'] if 's51' in data_dic else ""
            con_result = data_dic['s27'] if 's27' in data_dic else ""
            con_judge = data_dic['s28'] if 's28' in data_dic else ""
            short = data_dic['s7'][6]
            province = short_to_province(short)

            for company_id in company_id_list:
                wenshu_info = {
                'company_id' : company_id,
                'docid': data_dic['s5'],  # 裁判文书页面ID
                "casename" : data_dic["s1"],  # 裁判文书名称
                'caseno' : data_dic['s7'], # 裁判文书案号
                'casetype': data_dic['s8'], # 裁判文书类型
                'casereason': ';'.join(data_dic['s11']), # 案件原由
                'court':data_dic['s2'] ,# 法院
                'judgedate': data_dic['s31'],# 裁判日期
                'pubdate':data_dic['s41'],# 公布日期
                'party':';'.join(data_dic['s17']),# 案件当事人
                'law_list':data_dic['s47'], # 相关法律列表
                'content':data_dic['qwContent'] if 'qwContent' in data_dic else "", # 文书页面
                'caseprocedure':data_dic['s9'] if 's9' in data_dic else "", # 文书执行程序
                'con_text': con_head + '\n' + con_1 + '\n' + con_2 + '\n' + con_3 + '\n' + con_result + '\n' + con_judge + '\n' + con_4 ,# 文书内容
                'province': province,  # 省份
                'rel_wenshu': data_dic['relWenshu'], # 关联文书信息
                'created_at': round(time.time(), 1), # 更新时间
                'identity':'' , # 身份
                }
                if company_id != 'person':
                    company_name = list(aliyun.company.find({'company_id': company_id}))[0]['entname']
                    monitor_notice = {
                        "title": "新增{}".format(wenshu_info['casename']),
                        "company_id": company_id,
                        "company_name": company_name,
                        "date": wenshu_info['pubdate'],
                        "sort": "裁判文书"
                    }
                    monitor_notice_list.append(monitor_notice)
                red.sadd("wss_wenshu_uploadES", company_id)
                if '_id' in wenshu_info:
                    del wenshu_info['_id']
                if company_id != 'person':
                    updateData.append(UpdateOne({"company_id": company_id}, {"$inc": {"fieldcount.judgment": 1}}))
                print(item['num'], wenshu_info)
                save_list.append(wenshu_info)
            aliyun.judgment.insert_many(save_list)
            save_list = []
            if updateData:
                aliyun.other_data3.bulk_write(updateData, ordered=False)
                updateData = []
            if monitor_notice_list:
                aliyun.monitor_notice.insert_many(monitor_notice_list)
                monitor_notice_list = []
        except Exception as e:
            pass


def huoqudata(times):
    data = mongo123[times].find().batch_size(300)
    num = 1
    for i in data:
        print(i['_id'], '***********'+str(num))
        num += 1
        i['num'] = num
        all_queue.put(i)


def start():
    times = arrow.now().shift(days=-28).format("YYYY-MM-DD")
    print(times)
    for i in range(1):
        Thr1 = threading.Thread(target=huoqudata, args=(times,))
        Thr1.start()
    for i in range(30):
        C = threading.Thread(target=clean)
        C .start()


# 清洗至9号

if __name__ == '__main__':
    start()

    # 清洗至12月29号
    # try:
    #     table = start()
    #     data = {"user": "Deng", "content": "失信被执行：{}清洗完成".format(table)}
    #     requests.post("http://192.168.1.157:5002/alert/notice", data=data)
    # except Exception as e:
    #     error = traceback.format_exc()
    #     send_str = '失信被执行数据清洗：\n' + error
    #     data = {"user": "Deng", "content": send_str}
    #     requests.post("http://192.168.1.157:5002/alert/alert", data=data)
    #     raise e

