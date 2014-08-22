import csv
import re
import sys
import time
import urllib.request

entry_pattern = re.compile('<div class="r-ent">.*?<div class="author">.*?</div>', re.S | re.M)
nrec_pattern = re.compile('<div class="nrec">.*?>([0-9]+)<.*?</div>', re.S | re.M)
mark_pattern = re.compile('<div class="mark">(.*?)</div>', re.S | re.M)
title_pattern = re.compile('<a href=".*?">(.*?)</a>', re.S | re.M)
title_re_pattern = re.compile('(Re:)', re.S | re.M)
title_subcategory_pattern = re.compile('\[(.*?)\]', re.S | re.M)

url_pattern = re.compile('<a href="(.*?)">', re.S | re.M)
url_entry_id_pattern = re.compile('/([^/]*?)\.html', re.S | re.M)

date_pattern = re.compile('<div class="date">(.*?)</div>', re.S | re.M)
author_pattern = re.compile('<div class="author">(.*?)</div>', re.S | re.M)

fop = open('outputlist-hate.csv', 'w', encoding='utf-8', newline='')
csvwriter = csv.writer(fop, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
fop2 = open('urlonly-hate.csv', 'w', encoding='utf-8')
count = 0

def search_or_return_empty_string(pattern, string, default_result=''):
    search_result = pattern.search(string)
    if search_result != None:
        return search_result.group(1)
    return default_result

for i in range(0,3000):
    time.sleep(1)
    print(i)
    pttweb = urllib.request.urlopen("http://www.ptt.cc/bbs/Hate/index%d.html" % i).read().decode("utf-8")
    results = entry_pattern.findall(pttweb)
    for result in results:
        nrec = str(0)
        if nrec_pattern.search(result) != None:
            nrec = nrec_pattern.search(result).group(1)
        nrec = search_or_return_empty_string(nrec_pattern, result, default_result='0')
        mark = search_or_return_empty_string(mark_pattern, result)
        title = search_or_return_empty_string(title_pattern, result)
        re = search_or_return_empty_string(title_re_pattern, result)
        subcategory = search_or_return_empty_string(title_subcategory_pattern, title)
        
        url = search_or_return_empty_string(url_pattern, result)
        url_entry_id = search_or_return_empty_string(url_entry_id_pattern, url)        
        date = search_or_return_empty_string(date_pattern, result)
        author = search_or_return_empty_string(author_pattern, result)
        try:
            csvwriter.writerow([url_entry_id, nrec, mark, re, subcategory, title, url, date, author])
        except UnicodeEncodeError:
            csvwriter.writerow([url_entry_id, nrec, mark, re, subcategory, title.encode("utf-8"), url, date, author])
            print('page %d has problem, count %d' %(i, count))
        fop.flush()
        fop2.write(url + '\n')
        fop2.flush()
        count += 1
