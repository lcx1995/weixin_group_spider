from scrapy import cmdline
import sys
import os
from multiprocessing import cpu_count,Pool
sys.path.append(os.path.dirname(__file__))

def run_spider(number):
    print('spider %s is started...'%number)
    cmdline.execute('scrapy crawl TiebaSpider'.split(' '))


if __name__ == '__main__':
    pool = Pool(4)
    for i in range(4):
        pool.apply_async(run_spider,args=(i,))
    pool.close()
    pool.join()
