# coding=utf-8
import ssl
import requests
from urllib.request import urlopen
from urllib.request import urlretrieve
#from mutagen.mp3 import MP3
from bs4 import BeautifulSoup
import re
import os
import time
import html

rss='fpyp.rss'
head='channel_info.txt'
if (os.path.exists(rss)):
    rss_new = 0
else:
    rss_new = 1
print(rss_new)
ssl._create_default_https_context = ssl._create_unverified_context
r= requests.get(
    "https://mp.weixin.qq.com/s/V6LfeY6Mki8VDyFYyfud2Q"
)
htmls=r.text
soup =BeautifulSoup(htmls,'lxml')
#ttt=soup.find_all('p',{'style':'white-space: normal;line-height: 25.6px;max-width: 100%;min-height: 1em;box-sizing: border-box !important;word-wrap: break-word !important;'})
ttt=soup.find_all('a',{'data-linktype':'2'})
#print(ttt)
for t in ttt:
    link = t.get('href')
    print(link)
    link_href='<a href="'+link+'"'
    print(link_href)
    print(html.unescape(htmls))
#    patten = re.compile(r">[0-9][0-9][0-9]+link_href")
#    print(patten)
    number = re.findall('[0-9][0-9][0-9]\D%s'%link_href,html.unescape(htmls))

    print(number)
    break