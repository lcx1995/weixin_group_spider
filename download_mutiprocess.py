from redis_tool.redis_url import REDIS_URL,REDIS_URL_QUEUE
from download_image import DownloadImage
from check_QR import CHECK_QRCORE
import multiprocessing
from multiprocessing import cpu_count
import os,random,time,logging

current_dir = os.path.dirname(__file__) #当前文件路径
save_img = os.path.join(current_dir,'download','img') #图片保存路径
save_qr = os.path.join(current_dir,'download','qr') #qr图片保存路径

redis_url = REDIS_URL()  # redis去重
redis_url_queue = REDIS_URL_QUEUE()  # 待抓取队列

downloadimage = DownloadImage(save_img)
check_qrcore = CHECK_QRCORE(redis_url,save_qr)

# logging.basicConfig(level = logging.DEBUG,filename='download_process.log',format = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
# logging.basicConfig(level = logging.INFO,filename='download_process.log',format = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def download_process():
    logger.info('%s-%s'%('begin process',os.getpid()))

    error = 0
    while error < 10:
        url = redis_url_queue.pop()
        if url:
            check_qrcore.check_copy(downloadimage.download(url))
        else:
            error += 1
        time.sleep(random.choice((1,2,3,4,5)))

    logger.info('%s-%s' % ('end process', os.getpid()))


if __name__ == '__main__':
    num = 10

    pool = multiprocessing.Pool(num)

    for i in range(0,num):
        pool.apply_async(download_process)

    pool.close()
    pool.join()