if __name__ == '__main__':
    from redis_tool.redis_url import REDIS_URL_QUEUE

    redis_url_queue = REDIS_URL_QUEUE()

    while 1:
        print('\rURL_QUEUE:%d'%(redis_url_queue.len()),end='')