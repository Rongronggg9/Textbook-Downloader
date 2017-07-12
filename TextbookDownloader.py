#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests  # 第三方库
import os
import ConfigParser
# import multiprocessing

import Prep


# ==========输出相关==========
class Pr(object):
    def __init__(self, p, s='Process'):  # 用多线程还是多进程好呢……  ←反正还没有咯……
        self.s = s + ' ' + str(p)
        self.p = p

    def pr(self, *s):
        out = eval("co.p%d('%s') + co.white(' : ')" % (self.p, self.s))

        for i in xrange(0, len(s), 2):
            if i + 1 < len(s):
                q = s[i + 1]
            else:
                q = 'white'
            out += eval("co.%s('%s')" % (q, s[i]))

        print out


# ==========获取图片==========
def spider(url, path, pid, i, name):
    p0 = Pr(pid)

    if not os.path.isdir(path):
        os.makedirs(path)

    if not isinstance(i, int):
        i = 1
        p0.pr('%s - Notice: Download will start from 1.jpg' % name, 'red')

    rpic = re.compile(r'(<IMG .*?src="?\./)(W\d+\.jpg)', re.I)
    urldivi = re.match(r'(http://.+/)(\w+_)(\d+)(\.\w+)', url, re.I).groups()
    index = urldivi[0]
    pre = urldivi[0] + urldivi[1]
    suf = urldivi[3]
    change = int(urldivi[2])

    p0.pr('Downloading %s from %s' % (name, index[7:]), 'magenta')

    m = 0

    for a in xrange(change + 5, 0, -1):
        url = pre + str(a) + suf
        html = requests.get(url).text
        picurl1 = rpic.search(html)
        if not picurl1:
            html = requests.get(url).text
            picurl1 = rpic.search(html)
        if picurl1:
            picurl = index + picurl1.group(2)
            pic = requests.get(picurl)
            if not pic:
                pic = requests.get(picurl)
            fp = open(path + '\\' + str(i) + '.jpg', 'wb')
            fp.write(pic.content)
            fp.close()
            p0.pr('%s - Downloading %s from %s' % (name, i, picurl[7:]), 'cyan')
            i += 1
            m = 0
        else:
            p0.pr('%s - No matched pic at %s' % (name, url[7:]), 'yellow')
            m += 1
        if m > 10:
            break

    p0.pr('%s - Done! Total pics: %d' % (name, i - 1), 'done')

    return


co = Prep.Co()

# ==========主程序==========
if __name__ == "__main__":
    try:
        print Prep.ansi.set_title('TextBook Downloader Alpha')  # 窗口标题
    finally:
        pass

    f0 = Pr(0, 'FrogGua')

    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    path0 = cf.get('Config', 'Path')
    # totalp = cf.getint('Config', 'ProcessNum')

    if not re.search(r'\\', path0):
        path0 += '\\'

    with open('list.ini') as f:
        list0 = f.readlines()

    l = Prep.prepare(list0)
    count = (len(l) + 1) / 3

    # if totalp > count:
    #     totalp = count

    print l

    f0.pr('Total book(s): %d' % count)
    # f0.pr('Total process(es): %d' % totalp)
    f0.pr(r'Save to: %s ' % path0.encode('string-escape'))

    for a in xrange(0, len(l), 3):
        name = l[a + 1]
        path = path0 + name
        if not path.endswith('\\'):
            path += '\\'

        spider(l[a], path, 1, l[a + 2], name)

    f0.pr('Download finished. ', 'done')
