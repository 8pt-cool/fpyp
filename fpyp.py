# coding=utf-8
import ssl
import requests
from urllib.request import urlopen
from urllib.request import urlretrieve
# from mutagen.mp3 import MP3
from bs4 import BeautifulSoup
import re
import os
import time


def write_episode_info(file_rss, title, audio_link, cover_link, time_local):
    title_label = '<title>' + title + '</title>'
    link_label = '<link>' + audio_link + '</link>'
    guid_label = '<guid>' + audio_link + '</guid>'
    enclousure_label = '<enclosure url="' + audio_link + '" type="audio/mpeg"/>'
    itunes_author_label = '<itunes:author>波米和他的朋友们</itunes:author>'
    itunes_subtitle_label = '<itunes:subtitle>' + title + '</itunes:subtitle>'
    itunes_summary_label = '<itunes:summary>欢迎关注“反派影评”公众号，可听到30分钟行业类谈话节目“反派马后炮”及短语音评电影的“电影耳旁风”，另外还可获取节目中提及的电影片单及其它延展信息。</itunes:summary>'
    itunes_image_label = '<itunes:image href="' + cover_link + '"/>'
    time_label = '<pubDate>' + time_local + '</pubDate>'
    decription_label = '<description>欢迎关注“反派影评”公众号，可听到30分钟行业类谈话节目“反派马后炮”及短语音评电影的“电影耳旁风”，另外还可获取节目中提及的电影片单及其它延展信息。</description>'
    item = '<item>' + title_label + enclousure_label + time_label + itunes_author_label + itunes_subtitle_label + itunes_summary_label + itunes_image_label + guid_label + link_label + decription_label + '</item>\n'
    file_rss.write(item)


def get_correct_link(seq):
    link_dic = {
        '异形：契约': 'http://audio.xmcdn.com/group33/M00/53/30/wKgJnVmbIMKiuLtUA3lZv1QmE44924.m4a',
        '夜行动物': 'http://audio.xmcdn.com/group24/M06/25/FB/wKgJMFhrgTvzPSUOAq2mrxJdruI201.m4a',
        '比利·林恩的中场战事': 'http://audio.xmcdn.com/group21/M03/65/A0/wKgJKFg3GL-A-EIfA7wMsbItbYI100.m4a',
        '屏住呼吸': 'https://s3-ap-southeast-1.amazonaws.com/fpyp/DontBreath.mp3',
        '奇异博士': 'http://music.163.com/#/dj?id=796114662',
        '第69届戛纳电影节专题': 'http://audio.xmcdn.com/group15/M07/7C/C2/wKgDaFdJawSi30SZAnVujqX1xPw331.m4a',
        '美国队长3': 'http://audio.xmcdn.com/group12/M09/69/BC/wKgDW1c3qjfgq14lAs7aJxkrOZs680.m4a'
    }
    # print(seq)
    if link_dic.get(seq) is not None:
        print(link_dic.get(seq))
        return link_dic.get(seq)
    else:
        return False


rss = 'fpyp.rss'
head = 'channel_info.txt'
# check if the file already exist
if os.path.exists(rss):
    rss_new = 0
else:
    rss_new = 1
print(rss_new)
ssl._create_default_https_context = ssl._create_unverified_context
# open the show list page
r = requests.get(
    "https://mp.weixin.qq.com/s/V6LfeY6Mki8VDyFYyfud2Q"
)
#  the show list page
html = r.text
soup = BeautifulSoup(html, 'lxml')
# write the channel info into rss file
file_rss = open(rss, 'w', encoding='UTF-8')
file_head = open(head, 'r', encoding='UTF-8')
head_text = file_head.read()
file_rss.write(head_text)
file_head.close()
# add every episode to a list to reverse
child_list = []
for child in soup.descendants:
    child_list.append(child)
for child in reversed(child_list):
    # find all paragraph label
    if child.name == 'p':
        # filter the p label without a
        if child.a is None:
            continue
        # if now data-linktype means it's not an episode link
        if not child.a.has_attr('data-linktype'):
            continue
        else:
            # get the sequence number of the episode
            showseq = []
            for string in child.strings:
                showseq.append(string.strip())
                break
            # find all episode link in the paragraph, this is for the extension episode
            ttt = child.find_all('a', {'data-linktype': '2'})
            for t in reversed(ttt):
                # get title
                title_noseq = t.get_text()
                if title_noseq == ' ':
                    continue
                # add episode seq in the title
                title = showseq[0] + '《' + title_noseq.strip() + '》'
                print(title)
                # print(title)
                # print(t.get('href'))
                # get the episode page link
                link = t.get('href')
                # print(link)
                # get all the contents in the page
                link_request = requests.get(link)
                link_html = link_request.text
                # get the audio link and publish time
                for line in link_html.splitlines():
                    # print(line)
                    if 'msg_source_url' in line:
                        # print(line)
                        if (title == '114《超人总动员2》'):
                            audio_link = 'http://image.kaolafm.net/mz/audios/201806/d96f030a-3eba-4447-9d47-0703332f07b4.mp3'
                            continue
                        audio_link = re.findall(r"\'(.+?)\'", line)[0]
                        if get_correct_link(title_noseq):
                            audio_link = get_correct_link(title_noseq)
                            continue
                        # print(audio_link)
                    if 'msg_cdn_url' in line:
                        cover_link = re.findall(r"\"(.+?)\"", line)[0]
                        # print(cover_link)
                    time_stamp = re.findall(r",n=\"(.+?)\"", line)
                    if (time_stamp):
                        time_local = time.localtime(int(time_stamp[0]))
                        time_local = time.strftime("%a, %d %b %Y %H:%M:%S +0800", time_local)
                        # time_label = '<pubDate>' + time_local + '</pubDate>'
                # write the episode info in the rss file
                write_episode_info(file_rss, title, audio_link, cover_link, time_local)
                # add episode 111(bullshit manual work)
                # print(showseq[0])
                if showseq[0] == '112 ':
                    write_episode_info(file_rss, '111 《三和人才市场 中国日结1500日元的年轻人们》',
                                       'http://image.kaolafm.net/mz/audios/201806/a91c444e-cc97-4d88-bf96-5beab506e95d.mp3',
                                       'http://mmbiz.qpic.cn/mmbiz_jpg/xDSn38gQsJZQ7wvX84icCNerf5p1P0ib4cxwuGjdesPITQiahtttFAhO2pMt67pXjAjllCVRyJFicQCEMjXMUz70bg/0?wx_fmt=jpeg',
                                       'Mon, 04 Jun 2018 19:04:15 +0800')
file_rss.write('</channel>\n</rss>')
file_rss.close()
