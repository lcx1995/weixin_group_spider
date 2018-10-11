import re
from PIL import Image
import codecs
import time
import download_img
from bs4 import BeautifulSoup

from redis_tool.redis_url import REDIS_URL
from check_QR import CHECK_QRCORE

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import logging

logging.basicConfig(level = logging.DEBUG,filename='baidu.log',format = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
logging.basicConfig(level = logging.INFO,filename='baidu.log',format = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def do():
    redis_url = REDIS_URL()  # redis去重
    check_qrcore = CHECK_QRCORE(redis_url)  # QR check

    url = 'https://www.baidu.com/'

    keyword = '入群 闲聊聊天'

    delay_time = 1  # 操作延迟时间

    opt = webdriver.ChromeOptions()
    opt.binary_location = r'D:\Google\Chrome\Application\chrome.exe'
    opt.headless = True  # 无GUI 运行

    driver = webdriver.Chrome(options=opt, executable_path=r'D:\Anaconda3\Scripts\chromedriver.exe')
    driver.implicitly_wait(10)
    driver.set_window_size(1280, 800)
    driver.get(url)

    #浏览器点击逻辑
    driver.find_element_by_xpath('//*[@id="kw"]').send_keys(keyword) #输入搜索关键词
    driver.find_element_by_xpath('//*[@id="su"]').click() #点击查询按钮
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="container"]/div[2]/div/div[2]/div').click() #点击高级工具
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="container"]/div[2]/div/div[1]/span[2]').click() #点击事件
    time.sleep(1)
    # driver.find_element_by_xpath('//*[@id="c-tips-container"]/div[1]/div/div/ul/li[3]/a').click() #点击一周
    driver.find_element_by_xpath('//*[@id="c-tips-container"]/div[1]/div/div/ul/li[2]/a').click() #点击一天

    for i in range(0,100): # 循环获取前十页的 网页内容
        logger.info('{:-^20}'.format('第%d页'%(i+1)))
        time.sleep(5)

        bs = BeautifulSoup(driver.page_source, 'lxml')

        ll = bs.find(id='content_left').find_all('div', recursive=False)
        # logger.debug(ll)
        # logger.debug(len(ll))
        for l in ll:
            _href = l.find('h3').find('a').attrs['href']

            if not redis_url.ismember_url_hash(url=_href):
                redis_url.add_url_hash(url=_href)#添加
                logger.info('%s-%s'%('采集',_href))
                try:
                    name_l = download_img.download_img(_href)
                    check_qrcore.check_copy(name_l)
                except Exception as ex:
                    logger.error('%s-%s' % (_href, ex))
            else:
                logger.info('%s-%s'%('去重',_href))

        #等待点击下一页
        try:
            WebDriverWait(driver,10).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="page"]/a[10]')))
            driver.find_element_by_xpath('//*[@id="page"]/a[10]').click()
        except Exception as ex:
            logger.error(ex)
            break #跳出循环

    time.sleep(10)
    driver.save_screenshot('screenshot.png')
    logger.info('%s结束运行!'%(__file__))


if __name__ == '__main__':
    do()