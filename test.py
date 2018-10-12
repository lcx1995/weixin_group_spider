def test_split():
    print('.pngt=20140803'.split('?'))

def test_os_remove():
    import os
    os.remove(r'D:\workspace\weixin_group_spider\download\img\67a2b3fe-cdce-11e8-ba2b-c83dd4a7358a.png')

def test_bs4():
    from bs4 import BeautifulSoup
    import codecs
    soup = BeautifulSoup(codecs.open('demo.html', 'r', 'gbk', errors='ignore'), 'lxml')
    print(soup.find(class_='s_post_list'))
    print(soup.find(class_='s_post_list').find_all('div', recursive=False))

def test_format():
    i = 1
    print('{:-^20}'.format('第%d页' % (i + 1)))
    print('https://weixin.qq.com/g/AzDjiKCWy9IWUqHM'.startswith('https://weixin.qq.com/g/'))