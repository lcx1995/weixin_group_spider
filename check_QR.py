from zxing import *
import shutil
import os
import logging
logger = logging.getLogger(__name__)

class CHECK_QRCORE(object):

    def __init__(self,redis_url,save_dir):
        self.redis_url = redis_url #redis去重
        self.save_dir = save_dir

    def check_copy(self,names):
        '''
        微信群二维码保存
        '''
        # ~ zx = BarCodeReader(zxing_location)
        zx = BarCodeReader()

        for name in names:
            try:
                #zxing 无法识别 含有\\的路径 必须 \\ 替换成 / , 同时添加"file:///"
                barcode = zx.decode("file:///"+name.replace('\\','/'))
                if barcode or barcode.raw:  # 识别出二维码信息 移动文件
                    logger.debug('-识别出二维码信息-%s-' % (barcode.raw))
                    if barcode.raw.startswith('https://weixin.qq.com/g/') and not self.redis_url.ismember_url_hash(url=barcode.raw):  # 只保存微信群 二维码
                        self.redis_url.add_url_hash(url=barcode.raw) #添加
                        shutil.move(name, os.path.join(self.save_dir,os.path.split(name)[-1]))
                        logger.debug(os.path.join(self.save_dir,os.path.split(name)[-1]))
                    else:
                        os.remove(name)
                else:
                    os.remove(name)
            except Exception as ex:
                logger.error(ex)


