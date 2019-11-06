import random
import time
import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) + Chrome/77.0.3865.120 Safari/537.36'}

url = 'https://bbs.hupu.com/bxj'

current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


# 返回当前时间
def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def get_one_page_post(url, headers):
    r = requests.get(url=url, headers=headers)
    doc = pq(r.text)
    # 调用items 方法 返回生成器
    result = doc('.for-list li').items()

    # 获取li中信息
    result_to_list = []
    for i in result:
        post_link = 'https://bbs.hupu.com' + i('.truetit').attr('href')
        post_title = i('.truetit').text()

        # 获取创建者的用户link name create-post-date
        author_info = i('.author').items()
        for info in author_info:
            # print(info, type(info))
            create_post_user = info('.aulink').text()
            create_post_user_link = info('.aulink').attr('href')
            # 使用兄弟节点获取关系获取帖子的创建日期
            create_post_date = info('.aulink').siblings().text()

        # Reply/browse
        # 为什么要新建for 循环呢？因为 pyquery只能选择一层的元素
        for rb in i('.ansour').items():
            reply_browse = rb.text().replace(u'\xa0', '')
            # print('reply/browse: ' + rb.text())

        # 最后回复的日期和用户及最后一楼
        for end_reply in i('.endreply').items():
            end_reply_floor_link = 'https://bbs.hupu.com/' + end_reply('a').attr('href')
            end_reply_date = end_reply('a').text()
            end_reply_author = end_reply('.endauthor').text()
        print(' ')

        #  TODO： 爬虫的时间应该改为实时爬取时间哦
        save_dic = {
            'post_link': post_link,
            'post_title': post_title,
            'create_post_user': create_post_user,
            'create_post_user_link': create_post_user_link,
            'create_post_date': create_post_date,
            'reply_browse': reply_browse,
            'end_reply_floor_link': end_reply_floor_link,
            'end_reply_date': end_reply_date,
            'end_reply_author': end_reply_author,
            'Crawl date': get_time()}
        print(current_time, save_dic, )
        result_to_list.append(save_dic)

    return result_to_list


def save_to_mongo(list1):
    client = MongoClient(host='120.79.mongo数据库, port=27019, username='spider', password='密码',
                         authSource='spider',
                         authMechanism='SCRAM-SHA-1')

    db = client.spider
    collection = db.hupu
    obj_id = collection.insert_many(list1)
    print('正在转存至monogodb数据库')
    print('存储id为' + current_time, obj_id.inserted_ids)
    print('转存成功')


if __name__ == '__main__':
    for i in range(1, 11):
        # 生成url
        new_url = url + '-' + str(i)
        result = get_one_page_post(url=new_url, headers=headers)
        save_to_mongo(list1=result)

        sleep_time = random.randint(0, 2) + random.random()
        print('反反爬虫时间：', sleep_time)
        time.sleep(sleep_time)
