from zxing import *
import shutil
import os
import logging
logger = logging.getLogger(__name__)

class WX_QR(object):
    def __init__(self,store_uri):
        self.store_uri = store_uri

    def check_copy(self,image_paths):
        '''
        微信群二维码保存
        :param names 列表形式的绝对路径文件
        :return 是QR的路径
        '''
        # ~ zx = BarCodeReader(zxing_location)
        zx = BarCodeReader()
        wx_qr_paths = []
        for image_path in image_paths:
            try:
                #zxing 无法识别 含有\\的路径 必须 \\ 替换成 / , 同时添加"file:///"
                barcode = zx.decode("file:///"+os.path.join(self.store_uri,image_path).replace('\\','/'))
                if barcode or barcode.raw:  # 识别出二维码信息 移动文件
                    logger.debug('-识别出二维码信息-%s-' % (barcode.raw))
                    if barcode.raw.startswith('https://weixin.qq.com/g/'):  # 只保存微信群 二维码
                        wx_qr_paths.append(image_path) #保存 路径
            except Exception as ex:
                # logger.error(ex)
                pass
        return wx_qr_paths