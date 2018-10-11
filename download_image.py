import requests
from bs4 import BeautifulSoup
import uuid
import sys,os
import re

import logging
logger = logging.getLogger(__name__)

# url = 'http://www.baidu.com/link?url=AEZJBhRIVY5gJcWHr_qQuhupJ4ser3BlUorkpgfk9miDmScQXFJ9O38yGcOTAxu9'
http_pattern = re.compile(r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$')
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Host": "36kr.com/newsflashes",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.3.6000"
}

'''
根据URL 下载网页中的图片
'''

class DownloadImage(object):
    http_pattern = re.compile(r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$')
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "Host": "36kr.com/newsflashes",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.3.6000"
    }

    def __init__(self,save_dir):
        self.save_dir = save_dir
        self.session = requests.session()
        self.session.headers[
            'User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.3.6000"

    def download(self,url):
        '''
        下载图片
        :param href:网页链接
        :param save_path:保存文件夹
        :return:
        '''
        save_path_list = []
        rq = self.session.get(url)

        soup = BeautifulSoup(rq.text, 'lxml')
        imgs = soup.find_all('img')
        for img in imgs:
            try:  # 抓取img的链接 给默认值 最后为空 不处理
                h = img.attrs.get('src', '') or img.attrs.get('data-src', '') or ''
                if not h:
                    continue
            except Exception as ex:
                logger.error('error:', ex)
                continue

            if not bool(self.http_pattern.search(h)):  # 判断是否是http[s]
                continue

            ext = os.path.splitext(h)[1].split('?')[0] if os.path.splitext(h)[1] else '.jpg'
            logger.info(h)
            r = self.session.get(h)
            save_path = os.path.join(self.save_dir,'%s%s'%(uuid.uuid1(),ext))
            with open(save_path, 'wb') as img_f:
                img_f.write(r.content)
            save_path_list.append(save_path)
        logger.debug(save_path_list)
        return save_path_list

def download_img(url):

    name_l = []

    s = requests.session()
    s.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.3.6000"
    rq = s.get(url= url)

    soup = BeautifulSoup(rq.text,'lxml')
    imgs = soup.find_all('img')

    for img in imgs:

        try:# 抓取img的链接 给默认值 最后为空 不处理
            h = img.attrs.get('src','') or img.attrs.get('data-src','') or ''
            if not h:
                continue
        except Exception as ex:
            logger.error('error:',ex)
            continue

        if not bool(http_pattern.search(h)):#判断是否是http[s]
            continue

        ext = os.path.splitext(h)[1] if os.path.splitext(h)[1] else '.jpg'
        logger.info(h)
        r = s.get(h)
        n = r'%s/%s%s'%('download/tmp',uuid.uuid1(),ext)
        with open(n,'wb') as img_f:
            img_f.write(r.content)

        name_l.append(n)

    return name_l

if  __name__ == '__main__':
    download_img('https://mp.weixin.qq.com/s?src=11&timestamp=1538967094&ver=1169&signature=Q5K66VXUp7yGIqfJ6Okqb5D1d3n4glayknEeqwvYMIWblqW*EnQ*lBBnsSfbqbIvy4HaxIj4Iio0Cxn8rMRUQquuBGfx7rBME*UjnAuAsiv3PE6JLmu6dOGa6rJ1Gz7o&new=1')