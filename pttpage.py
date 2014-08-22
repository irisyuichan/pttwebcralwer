import csv
import re
import sys
import time
import urllib.request

author_pattern = re.compile('<div class="article-metaline"><span class="article-meta-tag">作者</span><span class="article-meta-value">(.*?)</span></div>', re.S | re.M)
title_pattern = re.compile('<div class="article-metaline"><span class="article-meta-tag">標題</span><span class="article-meta-value">(.*?)</span></div>', re.S | re.M)
time_pattern = re.compile('<div class="article-metaline"><span class="article-meta-tag">時間</span><span class="article-meta-value">(.*?)</span></div>', re.S | re.M)
content_pattern = re.compile('<div id="main-container">(.*?)<span class="f2">※', re.S | re.M)
content_filter_div_pattern = re.compile('<div .*?</div>', re.S | re.M)

push_entry_pattern = re.compile('<div class="push">(.*?)</div>', re.S | re.M)
push_tag_pattern = re.compile('<span class=".*?push-tag">(.*?)</span>', re.S | re.M)
push_user_id_pattern = re.compile('<span class=".*?push-userid">(.*?)</span>', re.S | re.M)
push_content_pattern = re.compile('<span class=".*?push-content">(.*?)</span>', re.S | re.M)
push_ipdatetime_pattern = re.compile('<span class=".*?push-ipdatetime">(.*?)</span>', re.S | re.M)
push_ipdatetime_ip_pattern = re.compile('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', re.S | re.M)
push_ipdatetime_datetime_pattern = re.compile('([0-9]+/[0-9]+ [0-9]+:[0-9]+)', re.S | re.M)

html_tag_pattern = re.compile('(<.*?>)', re.S | re.M)

fop = open('outputpage-hate.csv', 'w', encoding='utf-8', newline='')
csvwriter = csv.writer(fop, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
fop2 = open('outputpage-network-hate.csv', 'w', encoding='utf-8', newline='')
csvwriter_network = csv.writer(fop2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
fin = open('urlonly-hate.csv', 'r', encoding='utf-8')
count = 0

def search_or_return_empty_string(pattern, string, default_result=''):
    search_result = pattern.search(string)
    if search_result != None:
        return search_result.group(1)
    return default_result

for url in fin:
    url = re.sub('\\n', '', url)
    if len(url) == 0:
        continue
    print(count)
    time.sleep(1)
    print('http://www.ptt.cc' + url)
    try:
        pttweb = urllib.request.urlopen('http://www.ptt.cc' + url).read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(e)
        continue
    except:
        continue
    #print(pttweb)
    author = search_or_return_empty_string(author_pattern, pttweb)
    author = re.sub('\(.*?\)', '', author)
    title = search_or_return_empty_string(title_pattern, pttweb)
    timestring = search_or_return_empty_string(time_pattern, pttweb)
    content = search_or_return_empty_string(content_pattern, pttweb)
    content = re.sub('\\n', '<br/>', content)
    content = content_filter_div_pattern.sub('', content)
    content = html_tag_pattern.sub('', content)
    csvwriter.writerow(['發文', author, url, timestring, title, content])
    fop.flush()
    push_entries = push_entry_pattern.findall(pttweb)
    network_row = [author]
    for push_entry in push_entries:
        #print(push_entry)
        push_tag = push_tag_pattern.search(push_entry).group(1)
        push_user_id = push_user_id_pattern.search(push_entry).group(1)
        push_content = push_content_pattern.search(push_entry).group(1)
        push_ipdatetime = push_ipdatetime_pattern.search(push_entry).group(1)
        push_ipdatetime = re.sub('\\n', '', push_ipdatetime)
        push_ipdatetime_ip = search_or_return_empty_string(push_ipdatetime_ip_pattern, push_ipdatetime)
        push_ipdatetime_datetime = search_or_return_empty_string(push_ipdatetime_datetime_pattern, push_ipdatetime)
        csvwriter.writerow([push_tag, push_user_id, push_ipdatetime_ip, push_ipdatetime_datetime, '', push_content])
        fop.flush()
        network_row += [push_user_id]
    count += 1
    csvwriter_network.writerow(network_row)
    fop2.flush()
