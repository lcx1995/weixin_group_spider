from scrapy_splash import SplashRequest
from scrapy import Request
from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
import re
from ..items import TiebaImgItem
from urllib import parse
from posixpath import normpath
import datetime


class TiebaSpider(RedisSpider):
    #时间范围(天)
    days_range = 5
    # next url
    re_next = re.compile(r'/f/search/res\?.*?pn=[1-9]\d*')
    # next string
    re_next_string = re.compile(r'\d+')
    # tiezi url
    re_tiezi = re.compile(r'(/p/.*)\?.*')
    # image url check
    http_pattern = re.compile(r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$')

    name = 'TiebaSpider'
    redis_key = 'TiebaSpider:start_urls'  # RedisSpider
    allowed_domains = ['tieba.baidu.com']

    # rules = (
    #     Rule(LinkExtractor(allow=('/f/search/res\?.*?pn=[1-9]\d*',),),follow=True),# 其他页
    #     Rule(LinkExtractor(allow=('/p/.*?\?pid=.*',),),callback='parse_item')# 抓每个贴吧链接
    # )

    # 事先将需要爬去的种子页面放入 redis_key中
    # def start_requests(self):
    #     for key_word in self.key_words:
    #         yield Request(self.url_template%(parse.quote(key_word)),dont_filter=True)

    def parse(self, response):
        flag_next = False #继续抓取开关
        soup = BeautifulSoup(response.body, 'lxml')
        url_parse = parse.urlparse(response.url)
        # 寻找帖子
        for tiezi in soup.find_all(class_='s_post'):
            # 判断是否是帖子
            if tiezi.find(href=self.re_tiezi):
                # 帖子时间
                tiezi_datetime = datetime.datetime.strptime(tiezi.find(class_='p_date').string, '%Y-%m-%d %H:%M')
                # {days_range}天内的贴子
                if (tiezi_datetime - datetime.datetime.now()).days <= self.days_range:
                    flag_next = True #出现七天内的帖子 则继续抓取下一页
                    url = parse.urlunparse((url_parse.scheme, url_parse.netloc, normpath(
                        self.re_tiezi.search(tiezi.find(href=re.compile(r'/p/.*?\?pid=.*')).attrs['href']).group(1)),
                                            '', '', ''))
                    yield Request(url, callback=self.parse_item)

        # 寻找其他页
        if flag_next:
            for next in soup.find_all(href=self.re_next, string=self.re_next_string):
                url = parse.urlunparse(
                    (url_parse.scheme, url_parse.netloc, normpath(next.attrs['href']), '', '', ''))
                yield Request(url, callback=self.parse)  # callback 还是parse

    def parse_item(self, response):
        item = TiebaImgItem()
        item['src_url'] = response.url
        item['image_urls'] = []
        soup = BeautifulSoup(response.body, 'lxml')
        for img in soup.find_all('img'):
            try:  # 抓取img的链接 给默认值 最后为空 不处理
                h = img.attrs.get('src', '') or img.attrs.get('data-src', '') or ''
                if not h:
                    continue
            except Exception as ex:
                continue
            if not bool(self.http_pattern.search(h)):  # 判断是否是http[s]
                continue
            item['image_urls'].append(h)
        yield item
