# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TiebaImgItem(scrapy.Item):
    src_url = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    wx_qr_paths = scrapy.Field()

class WxQrScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
