from bs4 import BeautifulSoup
import codecs

soup = BeautifulSoup(codecs.open('demo.html','r','gbk',errors='ignore'),'lxml')

print(soup.find(class_='s_post_list'))

print(soup.find(class_='s_post_list').find_all('div', recursive=False))