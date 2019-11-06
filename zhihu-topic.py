import time
import json
import random
import requests
from pymongo import MongoClient


# 通过接口获取帖子信息
def get_each_post_info(url, headers):
    try:
        r = requests.get(url=url, headers=headers)
        # 返回 json数据
        data = json.loads(r.text)
    except Exception as e:
        print('Error:' + e)

    return data


def save_to_mongo(data):
    client = MongoClient(
        host='ip',
        port=27019,
        username='spider',
        password='password',
        authSource='spider',
        authMechanism='SCRAM-SHA-1')

    db = client.spider
    collection = db.zhihutopic
    result = collection.insert_one(data)
    print('正在转存至monogo数据库')
    # TODO: 这里的id 为何获取报错！！！
    # print(result.inserted_id + '转存成功')


# 反爬虫随机时间
def sleep_time():
    sleep_spider_time = random.randint(0, 2) + random.random()
    print('反反爬虫时间：', sleep_spider_time)
    time.sleep(sleep_spider_time)


if __name__ == '__main__':

    url = 'https://www.zhihu.com/api/v4/topics/19860414/feeds/top_activity?' \
          'include=data[%3F(target.type%3Dtopic_sticky_module)].target.data' \
          '[%3F(target.type%3Danswer)].target.content%2Crelationship.is_auth' \
          'orized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata[%3F' \
          '(target.type%3Dtopic_sticky_module)].target.data[%3F(target.type%' \
          '3Danswer)].target.is_normal%2Ccomment_count%2Cvoteup_count%2Cconte' \
          'nt%2Crelevant_info%2Cexcerpt.author.badge[%3F(type%3Dbest_answerer' \
          ')].topics%3Bdata[%3F(target.type%3Dtopic_sticky_module)].target.da' \
          'ta[%3F(target.type%3Darticle)].target.content%2Cvoteup_count%2Cco' \
          'ment_count%2Cvoting%2Cauthor.badge[%3F(type%3Dbest_answerer)].top' \
          'ics%3Bdata[%3F(target.type%3Dtopic_sticky_module)].target.data[%3F' \
          '(target.type%3Dpeople)].target.answer_count%2Carticles_count%2Cgend' \
          'er%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge[%3F(type%3' \
          'Dbest_answerer)].topics%3Bdata[%3F(target.type%3Danswer)].target.' \
          'annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelatio' \
          'nship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%' \
          '3Bdata[%3F(target.type%3Danswer)].target.author.badge[%3F(type%3Dbes' \
          't_answerer)].topics%3Bdata[%3F(target.type%3Darticle)].target.annotat' \
          'ion_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge[%3F(ty' \
          'pe%3Dbest_answerer)].topics%3Bdata[%3F(target.type%3Dquestion)].targe' \
          't.annotation_detail%2Ccomment_count%3B&limit=5&after_id='

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
    }

    # TODO: 可以做成获取paging的值
    for i in range(5, 25, 5):
        new_url = url + str(i) + '.00000'
        # print(new_url + '正在爬取')
        result = get_each_post_info(url=new_url, headers=headers)
        for dic in result['data']:
            print(dic)
            print(type(dic))
            save_to_mongo(data=dic)

        # 反爬虫时间
        sleep_time()
