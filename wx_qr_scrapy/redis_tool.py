import redis
import logging
from urllib import parse
logger = logging.getLogger(__name__)

class RedisList(object):
    '''
    获取的url入list
    '''
    def __init__(self,name,host='127.0.0.1',password='lcx',port=6379,db=0):
        pool = redis.ConnectionPool(host=host, password=password,port=port,db=db)
        self.r = redis.Redis(connection_pool=pool)
        self.name = name

    def trim(self):
        self.r.delete(self.name)

    def push(self,url):
        self.r.lpush(self.name,url)

    def pop(self):
        return self.r.rpop(self.name)

    def len(self):
        return self.r.llen(self.name)

class RedisSet(object):
    '''
    获取的url入list
    '''
    def __init__(self,name,host='127.0.0.1',password='lcx',port=6379,db=0):
        pool = redis.ConnectionPool(host=host, password=password,port=port,db=db)
        self.r = redis.Redis(connection_pool=pool)
        self.name = name

    def trim(self):
        self.r.delete(self.name)

    def push(self,url):
        self.r.sadd(self.name,url)

    def pop(self):
        return self.r.spop(self.name)

    def len(self):
        return self.r.scard(self.name)

def trim_tieba_list():
    redis_key = 'TiebaSpider:start_urls'
    redislist = RedisSet(redis_key)
    redislist.trim()

def init_tieba():
    # 将种子文件放入redis_key = 'TiebaSpider:start_urls' 中
    key_words = ['交友 互动群','微信 交友']
    url_template = 'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%s'  # 链接模板
    redis_key = 'TiebaSpider:start_urls'
    redislist = RedisSet(redis_key)
    for key_word in key_words:
        redislist.push(url_template % (parse.quote(key_word)))

if __name__ == '__main__':
    #初始化 开始urls
    init_tieba()