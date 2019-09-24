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
    link_href=' <a href="'+link
    print(link_href)
    print(html.unescape(htmls))
    patten = re.compile(r'[0-9]{2,5}(%s)(.+?)' %link_href)
    #    patten = re.compile(r'((/|.)*html)')
    number=patten.search(html.unescape(htmls))
#    print(patten)
    number = re.findall('[0-9]{3,}%s(.+?)' %link_href,html.unescape(htmls))

    print(number)
    """
    url = "oreilly.com"
    regex3 = re.compile(r"^((/|.)*(%s))" % url)
    regex4 = re.compile(r"^((/|.)*oreilly.com)")
    regex5 = re.compile(r"^((/|.)*" + url + ')')

    string3 = '/oreilly.com/baidu.com'

    mo3 = regex3.search(string3)
    mo4 = regex4.search(string3)
    mo5 = regex5.search(string3)
    print(mo3.group())
    print(mo4.group())
    print(mo5.group())
    """
    break
