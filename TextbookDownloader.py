#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests  # 第三方库
from requests.adapters import HTTPAdapter
import os
import ConfigParser
import multiprocessing

import Prep

req = requests.Session()
req.mount('http://', HTTPAdapter(max_retries=1))
req.mount('https://', HTTPAdapter(max_retries=1))


# ==========获取图片==========
class Spider(object):
    def __init__(self, pid, path0, l, strict=1, s='Process'):
        self.pid = pid
        self.url = l[0]
        self.name = l[1][:-1]
        self.i = l[2]
        self.path = path0 + l[1]
        self.ph = Pr(pid, '%s - ' % self.name, s)
        self.s = s
        self.strict = strict

        if not os.path.isdir(self.path):
            os.makedirs(self.path)  # 创建文件夹

        if isinstance(self.i, int):
            self.ia = self.i
        else:
            self.ia = self.i = 1

    def save(self, ia, picurl, name='', path='', suf='jpg'):  # 保存
        if name == '':
            name = self.name
        if path == '':
            path = self.path

        ph = Pr(self.pid, '%s - ' % name, self.s)

        pic = req.get(picurl).content
        flie = path + str(ia) + '.' + suf
        with open(flie, 'wb') as fp:
            fp.write(pic)
        ph.pr('Downloaded %s to %s' % (picurl[7:], file), 'green')

    def done(self, ia, index, name=''):  # 完成提示
        i = self.i
        if name == '':
            name = self.name
        ph = Pr(self.pid, '%s - ' % name, self.s)
        if ia - i > 0:
            ph.pr('Done! Total pics: %d' % (ia - 1), 'succeed')
            ret = 1
        else:
            ph.pr('Failed to download from %s' % index[7:], 'error')
            ret = 0
        return ret

    def peppic(self):  # 人教社 处理图片页
        url = self.url
        ia = self.ia
        ph = self.ph

        try:
            urldivi = re.match(r'(http://.+/)(.+/)(\w+_)(\d+)(\.\w+)', url, re.I).groups()
        except:
            ph.pr('Illegal URL: %s' % url)
            return 0

        index = urldivi[0]
        pre = urldivi[0] + urldivi[1] + urldivi[2]
        suf = urldivi[4]
        change = int(urldivi[3])

        m = 0

        change += 5
        while m < 16:
            url = pre + str(change) + suf

            try:
                html = req.get(url).text
            except:
                ph.pr('Please check your network connection.', 'error')
                return 0
            rpic = re.compile(r'(<IMG .*?src="?\.?/)(W\d+?\.jpg)', re.I)
            picurl1 = rpic.search(html)
            if picurl1:
                picurl = index + picurl1.group(2)
                self.save(ia, picurl)
                ia += 1
                m = 0
            else:
                ph.pr('No matched pic at %s' % url[7:], 'yellow')
                m += 1

            change -= 1

        ret = self.done(ia, index)

        return ret

    def bnupcontents(self, name='', url='', path=''):  # 北师大社基教分社 处理目录页
        if name == '':
            name = self.name
        if url == '':
            url = self.url
        if path == '':
            path = self.path
        else:
            if not os.path.isdir(path):
                os.makedirs(path)  # 创建文件夹

        ia = self.ia
        ph = Pr(self.pid, '%s - ' % name, self.s)
        strict = self.strict
        index = 'http://gbjc.bnup.com/'

        try:
            contents = req.get(url).text
        except:
            ph.pr('Please check your network connection.', 'error')
            return 0

        coverurl = re.search(r'( src=["\']/?)(\w+/\w+/month_\d+/.+?\.jpg)(["\'])', contents, re.I)

        if strict == 0:
            rpage = r'( \s*?href=["\']/?)(edur\w+\.php\?.{5,50}=list&.{5,45}\d+)(["\'])'
            contenturls = []
        else:
            rpage = r'( \s*?href=["\']/?)(edur\w+\.php\?.{5,50}=list&.{5,45}\d+)(["\'].{5,55}bold)'
            contenturls = re.findall(
                r'( \s*?href=["\']/?)(edur\w+\.php\?.{5,50}=(?:list&|show&).{5,45}\d+)(["\'].{5,55}margin)',
                contents, re.I)
        pageurls = re.findall(rpage, contents, re.I)
        # 封面 URL & 图片页 List

        if coverurl:
            cover = index + coverurl.group(2)  # 封面
            self.save('#Cover', cover, name, path)

        allurl = []
        if pageurls or contenturls:
            contenturls.extend(pageurls)
            count = len(contenturls)
            rpic = re.compile(r'(\w{1,5}=["\']/?)(data/upload/\w+.{7,35}\.jpg)(["\'])', re.I)
            rpicname = re.compile(r'(/.+/)([a-z0-9]+)(_?.*?)(\.jpg)', re.I)
            ph.pr('Matching pics in %d page(s), ' % count, 'yellow', 'it may take a few minutes before downloading.', 'red')

            for i, pageurl in enumerate(contenturls):  # 依次检查图片页
                pageurl = index + pageurl[1]
                ph.pr('Matching pics at %s' % pageurl[7:], 'yellow', '    %d/%d' % (i+1, count), 'cyan')
                html = req.get(pageurl).text
                picurls = rpic.findall(html)

                if picurls:
                    for picurl in picurls:  # 匹配图片页中全部图片
                        allurl.append(index + picurl[1])
                    ph.pr('Matched %d pic(s) at %s' % (len(picurls), pageurl[7:]), 'cyan')

                else:
                    ph.pr('No matched pic at %s' % pageurl[7:], 'yellow')

        else:
            ph.pr('Matched nothing at %s' % url[7:], 'error')
            return 0

        if allurl:
            allurls = list(set(allurl))  # 去重
            allurls.sort(key=allurl.index)  # 排序
            ph.pr('Total matched pic(s):%d' % len(allurls), 'magenta')
            for picurl in allurls:
                picname = rpicname.search(picurl).group(2)
                self.save(picname, picurl, name, path)  # 然而实际上北师大社基教分社有些图片页顺序不对，以原名储存为好orz
                ia += 1
        else:
            ph.pr('Matched nothing at %s' % url[7:], 'error')
            return 0

        ret = self.done(ia, url, name)

        return ret

    def bnuppic(self):  # 北师大社基教分社 处理图片 URL
        url = self.url
        ia = self.ia
        ph = self.ph

        if re.match(r'(\w+://.+/month_.+/)(.+?\.jpg)', url, re.I):
            ph.pr('Irregular pic URL (you may use a URL of contents instead): %s' % url[7:], 'error')  # 无法推导的图片网址
        else:
            try:
                picdivi = re.match(r'(\w+://.+/.+?)(\d+)(\.jpg)', url, re.I).groups()
            except:
                ph.pr('Illegal URL: %s' % url)
                return 0

            pre = picdivi[0]
            suf = picdivi[2]
            change = int(picdivi[1])

            m = 0
            change -= 5
            while m < 16:
                picurl = pre + str(change) + suf
                status = req.get(picurl).status_code
                if status == requests.codes.ok:
                    self.save(ia, picurl)
                    m = 0
                else:
                    m += 1
                change += 1
                ia += 1

        ret = self.done(ia, url)

        return ret

    def bnupbooks(self): # 北师大社基教分社 处理书目页
        url = self.url
        ph = self.ph
        index = 'http://gbjc.bnup.com/'

        try:
            bookcontents = req.get(url).content.decode('utf-8')
            ph.pr('Matching book(s) at %s' % url[7:], 'cyan')
        except:
            ph.pr('Please check your network connection.', 'error')
            return 0

        rbook = re.findall(
            ur'(<a href=["\']/?)(reso\w+\.php\?classid=.{10,60})(["\'].{0,20}?>)((?:[一-龥]|\w| ){2,20})(<)',
            bookcontents, re.I)

        print rbook, bookcontents, isinstance(bookcontents, unicode)
        if rbook:
            books={}
            for book in rbook:
                books[book[3]] = book[1]

            ret = count = 0
            if books:
                count = len(books)
                ph.pr('Total matched book(s):%d' % count, 'magenta')
                for name in books:
                    url = index + books[name]
                    path = self.path + name + '\\'
                    ret += self.bnupcontents(name, url, path)

                self.ia = self.i

        else:
            ph.pr('Matched nothing at %s' % url[7:], 'error')
            return 0

        return [ret, count]

    def get(self):
        url = self.url
        ph = self.ph
        rpep = re.search(r'pep\.com\.cn', url, re.I)
        rbnup = re.search(r'bnup\.com', url, re.I)
        rbnupcontents = re.search(r'resourcetype.+classid', url, re.I)

        ret = count = 0

        ph.pr('Downloading from %s' % url[7:], 'magenta')

        if rpep:
            ret = self.peppic()
        elif rbnup:
            if url.endswith(r'.jpg'):
                ret = self.bnuppic()
            elif rbnupcontents:
                ret = self.bnupcontents()
            else:
                reta = self.bnupbooks()
                ret = reta[0]
                count = reta[1]

        else:
            ph.pr('This URL has not been supported yet: %s' % url[7:], 'error')

        return [ret, count]


# ==========多进程=========
def mul(pid, totalp, path0, l):
    rec = 0
    list = l[pid::totalp]
    for a in list:
        spider = Spider(pid, path0, a)
        rec += spider.get()
    return rec

Pr = Prep.Pr

# ==========主程序==========
if __name__ == "__main__":
    try:
        print Prep.ansi.set_title('TextBook Downloader - Alpha')  # 窗口标题
    finally:
        print 'TextBook Downloader - Alpha'

    f0 = Pr(0, '', 'Main   ')
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    path0 = cf.get('Config', 'Path')
    strict = cf.getint('Config', 'Strict')
    try:
        totalp = cf.getint('Config', 'ProcessNum')
    except:
        totalp = 0

    if totalp == 0:
        totalp = multiprocessing.cpu_count()

    if not path0.endswith('\\'):
        path0 += '\\'  # 加上反斜杠

    with open('list.ini') as f:
        list0 = f.readlines()  # 读取列表
    l = Prep.prepare(list0)  # 处理列表
    count = len(l)  # 计数

    if totalp > count:
        totalp = count

    f0.pr('Total URL(s): %d' % count)
    f0.pr('Total process(es): %d' % totalp)
    f0.pr(r'Save to: %s ' % path0.encode('string-escape'))

    rec = 0
    if totalp == 1:  # 单进程
        for a in l:
            spider = Spider(1, path0, a, strict, 'SingleP')
            reca = spider.get()
            rec += reca[0]
            recc = reca[1]
            if recc > 0:
                count += recc - 1

    else:  # 多进程
        totalp = 1
        multiprocessing.freeze_support()
        pool = multiprocessing.Pool(totalp)
        recs = []

        for pid in xrange(totalp):
            recp = pool.apply_async(mul, (pid, totalp, path0, l))
            recs.append(recp)

        pool.close()
        pool.join()

        for recp in recs:
            rec += recp.get()

    if rec == count:
        s = 'Succeeded in downloading all books!'
        color = 'succeed'
    elif rec == 0:
        s = 'Failed to download all books!'
        color = 'error'
    else:
        s = 'Neither success nor failure.'
        color = 'notice'

    f0.pr(s, color)
    f0.pr('Finished.', color)
    f0.pr('Succeeded: %d' % rec, color)
    f0.pr('Failed: %d' % (count - rec), color)
