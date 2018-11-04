import time

from redis_tool.redis_url import REDIS_URL,REDIS_URL_QUEUE

from selenium import webdriver
import logging

logger = logging.getLogger(__name__)

import abc
import six

from exceptions import RefreshPageException

import os

@six.add_metaclass(abc.ABCMeta)
class CommonOperation(object):
    current_dir = os.path.dirname(__file__) #当前文件路径
    save_img = os.path.join(current_dir,'download','img') #图片保存路径
    save_qr = os.path.join(current_dir,'download','qr') #qr图片保存路径

    logger = logging.getLogger(__name__)

    redis_url = REDIS_URL()  # redis去重
    redis_url_queue = REDIS_URL_QUEUE() #待抓取队列

    def __init__(self,url,keyword,wdxpath,queryxpath,delay=2):
        self.url = url #抓取的url
        self.keyword = keyword #抓取的关键词
        self.delay = delay #通用等待时间

        #xpath
        self.wd = wdxpath
        self.query = queryxpath

    def init_driver(self,headless=True,size=(1280,800),implicitly_wait=10):
        '''
        浏览器初始化参数
        :param headless GUI运行 True/Flase
        :return:
        '''
        opt = webdriver.ChromeOptions()
        opt.binary_location = r'D:\Google\Chrome\Application\chrome.exe'
        opt.headless = headless
        driver = webdriver.Chrome(options=opt, executable_path=r'D:\Anaconda3\Scripts\chromedriver.exe')
        driver.implicitly_wait(implicitly_wait)
        driver.set_window_size(size[0],size[1])
        driver.get(self.url)

        self.opt = opt
        self.driver = driver

    def start_query(self):
        '''
        查询操作
        :param wd 关键词 xpath
        :param query 查询按键 xpath
        :return:
        '''
        # 浏览器点击逻辑
        self.driver.find_element_by_xpath(self.wd).send_keys(self.keyword)  # 输入关键词
        self.driver.find_element_by_xpath(self.query).click()  # 点击搜索

    @abc.abstractmethod
    def start_collect_href(self,engine='lxml'):
        '''
        开始该页数据采集
        :param engine bs4 解析器
        :return: 返回href 列表 [href1,href2,href3...]
        '''
        pass

    @abc.abstractmethod
    def start_next(self):
        '''
        点击下一页操作
        :return:
        '''
        pass

    def start(self,max_page=100,query_delay=5,headless=True):
        '''
        数据采集开始
        :param max_page 最大采集页
        :return:
        '''
        #step 1
        self.init_driver(headless=headless)  # 浏览器参数初始化
        time.sleep(self.delay)

        #step 2
        self.start_query()
        time.sleep(query_delay) #查询等待时间

        #step 3
        for i in range(0,max_page):

            self.logger.info('{:-^20}'.format('第%d页' % (i + 1)))

            # 搜集该页的href
            hrefs = None
            while 1:
                try:
                    hrefs = self.start_collect_href()
                    break
                except RefreshPageException as ex:
                    self.driver.refresh()
                finally:
                    time.sleep(query_delay)  # 查询等待时间

            for href in hrefs:
                if not self.redis_url.ismember_url_hash(url=href):
                    self.redis_url.add_url_hash(url=href)  # 添加
                    self.redis_url_queue.push(href) #将待处理链接放入队列 另一个进程处理 download

            #下一页
            error_c = 0
            while 1:
                if error_c > 10:
                    break
                try:
                    self.start_next()
                    time.sleep(query_delay)  # 查询等待时间
                    break
                except RefreshPageException as ex:
                    self.driver.refresh()
                    error_c += 1
                    time.sleep(query_delay)  # 查询等待时间


        #step 4
        time.sleep(self.delay)
        self.driver.save_screenshot('screenshot.png')

        self.driver.close()
        self.logger.info('%s结束运行!' % (__file__))
