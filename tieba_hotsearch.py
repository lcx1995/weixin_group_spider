'''
获取贴吧热搜排名
'''

import requests
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def tieba_hot():
    url = 'http://tieba.baidu.com/hottopic/browse/topicList'
    session = requests.session()
    session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.3.6000"
    r = session.get(url)
    j = json.loads(r.text)
    l = j['data']['bang_topic']['topic_list']
    topic_names = [l_['topic_name'] for l_ in l]
    logger.info(topic_names)
    return topic_names

if __name__ == '__main__':
    print(tieba_hot())