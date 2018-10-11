import redis
import logging
import hashlib

logger = logging.getLogger(__name__)

class REDIS_URL_QUEUE(object):
    '''
    获取的url入list
    '''
    def __init__(self,host='127.0.0.1',password='lcx',port=6379,db=0):
        pool = redis.ConnectionPool(host=host, password=password,port=port,db=db)
        self.r = redis.Redis(connection_pool=pool)

    def push(self,url,name='URL_QUEUE'):
        self.r.lpush(name,url)

    def pop(self,name='URL_QUEUE'):
        return self.r.rpop(name)

    def len(self,name='URL_QUEUE'):
        return self.r.llen(name)

class REDIS_URL(object):

    def __init__(self,host='127.0.0.1',password='lcx',port=6379,db=0):
        pool = redis.ConnectionPool(host=host, password=password,port=port,db=db)
        self.r = redis.Redis(connection_pool=pool)

    def add_url_hash(self,url,name='URL_HASH'):
        '''
        hash处理后添加
        :param value:
        :param name:
        :return:
        '''
        self.r.sadd(name,self.hash_url(url))

    def ismember_url_hash(self,url,name='URL_HASH'):
        '''
        hash处理后判断 存在
        :param value:
        :param name:
        :return:
        '''
        flag = self.r.sismember(name,self.hash_url(url))

        return flag


    def list_url_hash(self,name='URL_HASH'):
        return self.r.smembers(name)

    def hash_url(self,url):
        url_hash_handler = hashlib.sha1()
        url_hash_handler.update(url.encode('utf-8'))
        return url_hash_handler.hexdigest()

if __name__ == '__main__':
    # url_redis = REDIS_URL()
    # url_redis.add_url_hash('https://www.baidu.com')
    # url_redis.add_url_hash('https://www.cnblogs.com/franknihao/p/6557561.html')
    #
    # print(url_redis.ismember_url_hash('https://www.baidu.com'))
    #
    # print(url_redis.list_url_hash())

    redis_url_queue = REDIS_URL_QUEUE()
    # redis_url_queue.push('https://www.baidu.com')
    # redis_url_queue.push('https://www.google.com')

    print(redis_url_queue.pop())