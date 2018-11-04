def test_split():
    print('.pngt=20140803'.split('?'))

def test_os_remove():
    import os
    os.remove(r'D:\workspace\weixin_group_spider\download\img\67a2b3fe-cdce-11e8-ba2b-c83dd4a7358a.png')

def test_bs4():
    from bs4 import BeautifulSoup
    import codecs
    _hrefs = []
    soup = BeautifulSoup(codecs.open('demo.html', 'r', 'gbk', errors='ignore'), 'lxml')
    for soup in soup.find(class_='s_post_list').find_all('div',id=None, recursive=False):
        _href = soup.find('span').find('a').attrs['href']
        if _href.startswith('/p/'):
            _hrefs.append(_href)
    print(_hrefs)
def test_format():
    i = 1
    print('{:-^20}'.format('第%d页' % (i + 1)))
    print('https://weixin.qq.com/g/AzDjiKCWy9IWUqHM'.startswith('https://weixin.qq.com/g/'))

def test_code():
    # 闭包
    def f1(a, b, c, *d, e, f):
        x = 1

        def f2():
            inner_x = x

        return f2

    ff = f1(1, 2, 3, 4, 5, 6, 7, e=8, f=9)
    print('闭包:', ff.__code__.co_varnames)
    print('闭包:', ff.__code__.co_freevars)
    print('闭包:', ff.__code__.co_cellvars)

    print('外部', f1.__code__.co_varnames)
    print('外部', f1.__code__.co_freevars)
    print('外部', f1.__code__.co_cellvars)

def test_html_escape():
    import html
    from urllib import parse
    print(parse.quote('能量 进群'))

def test_re_tiebap():
    import re
    def process_value(value):
        m = re.search("(/p/.*?)\?pid=.*", value)
        if m:
            return m.group(1)
    str = '/p/5859383637?pid=121717609609&cid=0#121717609609'
    r = re.search('/p/.*?\?pid=.*',str)
    print(r)
    print(process_value(str))

def test_sh_copy():
    import shutil
    import os
    import sys
    os.makedirs(r'G:\wx_qr\qr\full')
    shutil.copy(r'G:\wx_qr\full\0b9f1acaf6ce82ce0fd121cf3273b75ce7594c0b.jpg',r'G:\wx_qr\qr\full\0b9f1acaf6ce82ce0fd121cf3273b75ce7594c0b.jpg')

def test_url():
    import os
    from urllib import parse
    url = 'http://www.cnblogs.com/shijiaoyun/p/4863813.html'
    print(os.path.split(url))
    url_parse = parse.urlparse(url)
    print(url_parse)
    print(parse.urlunparse((url_parse.scheme,url_parse.netloc,'','','','')))

def test_bs4_re_tieba_1():
    '''
    bs4 re 匹配 url 拼接
    :return:
    '''
    from bs4 import BeautifulSoup
    import re
    from urllib import parse
    from posixpath import normpath
    url = 'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=123&red_tag=p0240089871'
    url_parse = parse.urlparse(url)
    with open('demo.html','r') as html:
        soup = BeautifulSoup(html,'lxml')
        next_page = soup.find_all(href=re.compile(r'/f/search/res\?.*?pn=[1-9]\d*'),string=re.compile(r'\d+'))
        for next in next_page:
            print(parse.urlunparse((url_parse.scheme,url_parse.netloc,normpath(next.attrs['href']),url_parse.params,url_parse.query,url_parse.fragment)))

def test_bs4_re_teiba_2():
    '''
    bs4 re 匹配 url 拼接
    :return:
    '''
    from bs4 import BeautifulSoup
    import re
    from urllib import parse
    from posixpath import normpath
    #贴吧 链接 抽取
    re_extract_tieba = re.compile(r'(/p/.*)\?.*')
    url = 'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=123&red_tag=p0240089871'
    url_parse = parse.urlparse(url)
    with open('demo.html','r') as html:
        soup = BeautifulSoup(html,'lxml')
        all_tie = soup.find_all(href=re.compile(r'/p/.*?\?pid=.*'))
        for tie in all_tie:
            # print(tie.attrs['href'],end='===')
            # print(re_extract_tieba.search(tie.attrs['href']).group(1),end='===')
            print(parse.urlunparse((url_parse.scheme,url_parse.netloc,normpath(re_extract_tieba.search(tie.attrs['href']).group(1)),'','','')))

def test_bs4_re_teiba_3():
    '''
    抓取 最近一周的帖子
    bs4 re 匹配 url 拼接
    :return:
    '''
    from bs4 import BeautifulSoup
    import re,time,datetime
    from urllib import parse
    from posixpath import normpath
    #贴吧 链接 抽取
    re_extract_tieba = re.compile(r'(/p/.*)\?.*')
    url = 'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=123&red_tag=p0240089871'
    url_parse = parse.urlparse(url)
    with open('demo.html','r') as html:
        soup = BeautifulSoup(html,'lxml')
        # all_tie = soup.find_all(href=re.compile(r'/p/.*?\?pid=.*'))
        all_ = soup.find_all(class_='s_post')
        for tiezi in all_:
            if tiezi.find(href=re.compile(r'/p/.*?\?pid=.*')):
                tiezi_datetime = datetime.datetime.strptime(tiezi.find(class_='p_date').string,'%Y-%m-%d %H:%M')
                print(tiezi_datetime,end='->')
                print((tiezi_datetime - datetime.datetime.now()).days,end='->')
                print(tiezi.find(href=re.compile(r'/p/.*?\?pid=.*')).attrs['href'],end='->')
                # print(tie.attrs['href'],end='===')
                # print(re_extract_tieba.search(tie.attrs['href']).group(1),end='===')
                print(parse.urlunparse((url_parse.scheme,url_parse.netloc,normpath(re_extract_tieba.search(tiezi.find(href=re.compile(r'/p/.*?\?pid=.*')).attrs['href']).group(1)),'','','')))

if __name__ == '__main__':
    test_bs4_re_teiba_3()