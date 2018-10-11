from common import CommonOperation
from bs4 import BeautifulSoup
from exceptions import RefreshPageException

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

import logging

import multiprocessing

logging.basicConfig(level = logging.DEBUG,filename='baidu_tieba_.log',format = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
logging.basicConfig(level = logging.INFO,filename='baidu_tieba_.log',format = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class BAIDU_TIEBA(CommonOperation):

    def __init__(self):
        super(BAIDU_TIEBA,self).__init__(url='https://tieba.baidu.com',
                      keyword='拖拉机',
                      wdxpath='//*[@id="wd1"]',
                      queryxpath='//*[@id="tb_header_search_form"]/span[2]/a')

    def start_collect_href(self,engine='lxml'):
        try:
            bs = BeautifulSoup(self.driver.page_source, 'html5lib')
            _hrefs = []
            for soup in bs.find(class_='s_post_list').find_all('div', recursive=False):
                _href = self.url + soup.find('span').find('a').attrs['href']
                _hrefs.append(_href)
            return _hrefs
        except Exception as ex:
            raise RefreshPageException('出错，刷新页面!')

    def start_next(self):
        try:
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, './/a[@class="next"]')))
            self.driver.find_element_by_xpath('.//a[@class="next"]').click()
        except Exception as ex:
            raise RefreshPageException('出错，刷新页面!')

if __name__ == '__main__':
    baidu_tieba = BAIDU_TIEBA()

    baidu_tieba.start(headless=False)
