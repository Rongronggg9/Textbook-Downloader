#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests  # 第三方库
from requests.adapters import HTTPAdapter
import os
import ConfigParser
# import threading

import Prep

req = requests.Session()
req.mount('http://', HTTPAdapter(max_retries=2))
req.mount('https://', HTTPAdapter(max_retries=2))


# ==========获取图片==========
def spider(url, path, pid, i, name):
    th = Pr(pid, '%s - ' % name)

    if not os.path.isdir(path):
        os.makedirs(path)

    if isinstance(i, int):
        ia = i
    else:
        ia = i = 1

    rpic = re.compile(r'(<IMG .*?src="?\./)(W\d+\.jpg)', re.I)
    urldivi = re.match(r'(http://.+/)(\w+_)(\d+)(\.\w+)', url, re.I).groups()
    index = urldivi[0]
    pre = urldivi[0] + urldivi[1]
    suf = urldivi[3]
    change = int(urldivi[2])

    th.pr('Downloading from %s' % index[7:], 'magenta')

    m = 0

    for a in xrange(change + 5, 0, -1):
        url = pre + str(a) + suf
        try:
            html = req.get(url).text
        except:
            th.pr('Please check your network connection.', 'error')
            break
        picurl1 = rpic.search(html)
        if picurl1:
            picurl = index + picurl1.group(2)
            pic = req.get(picurl)
            fp = open(path + str(ia) + '.jpg', 'wb')
            fp.write(pic.content)
            fp.close()
            th.pr('Downloaded %s to %d.jpg' % (picurl[7:], ia), 'cyan')
            ia += 1
            m = 0
        else:
            th.pr('No matched pic at %s' % url[7:], 'yellow')
            m += 1
        if m > 10:
            break
    if ia - i > 0:
        th.pr('Done! Total pics: %d' % (ia - 1), 'succeed')
        ret = 1
    else:
        th.pr('Failed to download from %s' % index[7:], 'error')
        ret = 0

    return ret


Pr = Prep.Pr

# ==========主程序==========
if __name__ == "__main__":
    try:
        print Prep.ansi.set_title('TextBook Downloader - Alpha')  # 窗口标题
    finally:
        print 'TextBook Downloader - Alpha'

    f0 = Pr(0, '', 'FrFrog')
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    path0 = cf.get('Config', 'Path')
    # totalt = cf.getint('Config', 'ThreadNum')

    if not path0.endswith('\\'):
        path0 += '\\'

    with open('list.ini') as f:
        list0 = f.readlines()
    l = Prep.prepare(list0)
    count = (len(l) + 1) / 3

    # if totalt > count:
    #     totalt = count

    # print l

    f0.pr('Total book(s): %d' % count)
    # f0.pr('Total thread(s): %d' % totalt)
    f0.pr(r'Save to: %s ' % path0.encode('string-escape'))

    rec = 0
    for a in xrange(0, len(l), 3):
        name = l[a + 1]
        path = path0 + name
        if not path.endswith('\\'):
            path += '\\'

        rec += spider(l[a], path, 1, l[a + 2], name)

    if rec == count:
        s = 'Succeeded in downloading all books!'
        color = 'succeed'
    elif rec == 0:
        s = 'Failed to download all books!'
        color = 'error'
    else:
        s = 'Neither success nor failure.'
        color = 'notice'

    f0.pr('Finished.', color)
    f0.pr('Succeeded: %d' % rec, color)
    f0.pr('Failed: %d' % (count - rec), color)
