# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import Request
from qrcode_tool import WX_QR
import os,sys
import shutil
from .items import TiebaImgItem
import pymongo
import json

class TiebaImgPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        if isinstance(item,TiebaImgItem):#判断
            image_paths = [x['path'] for ok, x in results if ok]
            if not image_paths:
                raise DropItem("Item contains no images")
            item['image_paths'] = image_paths
        return item

class ImageQRCodePipeline(object):
    '''
    处理item 的 qr 识别
    '''
    def __init__(self,store_uri,settings):
        self.store_uri = store_uri
        self.settings = settings
        self.wx_qr = WX_QR(store_uri)
        #创建qr文件夹
        if not os.path.exists(os.path.join(self.store_uri,'qr')):
            os.makedirs(os.path.join(self.store_uri,'qr'))

    @classmethod
    def from_settings(cls, settings):
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri,settings)

    def process_item(self, item, spider):
        if isinstance(item, TiebaImgItem):#判断
            image_paths = item['image_paths']
            wx_qr_paths = self.wx_qr.check_copy(image_paths)
            #将图片copy到[store_uri]\\wx_qr
            for wx_qr_path in wx_qr_paths:
                shutil.copy(os.path.join(self.store_uri,wx_qr_path),os.path.join(self.store_uri,'qr'))
            item['wx_qr_paths'] = wx_qr_paths #赋值保存后的
        return item

class TiebaImgMongoDBPipeline(object):

    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = 'tieba_image'
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        if isinstance(item, TiebaImgItem):  # 判断
            data = dict(item)
            self.post.insert(data)
        return item