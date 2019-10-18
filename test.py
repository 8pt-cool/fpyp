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
import librosa




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
#print(htmls)
#regex = re.compile("(>(\d{3,})\s{1,}< a href=(.*)\s{1,}target)")
#print(regex.findall(htmls))

soup =BeautifulSoup(htmls,'lxml')

#ttt=soup.find_all('p',{'style':'white-space: normal;line-height: 25.6px;max-width: 100%;min-height: 1em;box-sizing: border-box !important;word-wrap: break-word !important;'})
#ttt=soup.find_all('a',{'data-linktype':'2'})
#print(soup)
child_list=[]
for child in soup.descendants:
    child_list.append(child)
for child in reversed(child_list):
    if child.name =='p':
        #print(child)
        if child.a is None:
            continue
        if not child.a.has_attr('data-linktype'):
            continue
        else:
            #print(child)
            showseq = []
            for string in child.strings:
                showseq.append(string)
                break
            #print(showseq)
            ttt=child.find_all('a',{'data-linktype':'2'})
            for t in ttt:
                title_noseq = t.get_text()
                if title_noseq == ' ':
                    continue
                # add episode seq in the title
                title_noseq = showseq[0] + '《' + title + '》'
                print(title)
                # print(title)
                # print(t.get('href'))
                # get the episode page link
                link = t.get('href')
                #print(link)
                # get all the contents in the page
                link_request = requests.get(link)
                link_html = link_request.text
                # get the audio link and publish time
                for line in link_html.splitlines():
                    # print(line)
                    if 'msg_source_url' in line:
                        #print(line)
                        if (title == '114 《超人总动员2》'):
                            audio_link = 'http://image.kaolafm.net/mz/audios/201806/d96f030a-3eba-4447-9d47-0703332f07b4.mp3'
                            continue
                        audio_link = re.findall(r"\'(.+?)\'", line)[0]
                        duration = librosa.get_duration(filename=audio_link)
                        print(duration)





            #print(showlist)
    #regex = re.compile("(>(\d{3,})\s{1,}< a href=(.*)\s{1,}target)")
    #print(regex.findall(t))



"""
for t in(ttt):
    print(ttt.parent())
#    print(t)

for t in ttt:
    link = t.get('href')
    print(link)
    link_href=' <a href="'+link
    #     print(link_href)
    # 
    #     patten = re.compile(r'[0-9]{2,5}(%s)(.*)' %link_href)
    #     #    patten = re.compile(r'((/|.)*html)')
    number=patten.search(html.unescape(htmls))
#    print(patten)
    htmls = '<p style="font-size: 16px;line-height: 25.6000003814697px;white-space: normal;max-width: 100%;min-height: 1em;color: rgb(62, 62, 62);box-sizing: border-box !important;word-wrap: break-word !important;background-color: rgb(255, 255, 255);"><span style="max-width: 100%;white-space: pre-wrap;font-size: 14px;box-sizing: border-box !important;word-wrap: break-word !important;">001 <a href="http://mp.weixin.qq.com/s?__biz=MzIxMTMzNTc5OA==&amp;mid=2247483656&amp;idx=1&amp;sn=d7b68107b3e80d87974b02471a976b6c&amp;scene=21#wechat_redirect" target="_blank" data_ue_src="http://mp.weixin.qq.com/s?__biz=MzIxMTMzNTc5OA==&amp;mid=2247483656&amp;idx=1&amp;sn=d7b68107b3e80d87974b02471a976b6c&amp;scene=21#wechat_redirect" data-linktype="2">垫底辣妹</a>（嘉宾：冰心、龙源）</span></p>'
    print(html.unescape(htmls))
    #number = re.findall('[0-9]{3,}%s(.+?)' %link_href,html.unescape(htmls))
    number = re.findall('[0-9]{3,}%s(.+?)' %link_href,html.unescape(htmls))
    print(number)
    
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

    break
"""