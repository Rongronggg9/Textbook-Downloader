#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from colorama import init, Fore, Back, ansi  # 第三方库

init(autoreset=True, strip=False)


class Co(object):
    """
    Colorize stdout.
    "There’s no RGB lighting."
    """

    def red(self, s):
        return Fore.LIGHTRED_EX + s + Fore.RESET

    def green(self, s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET

    def yellow(self, s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET

    def blue(self, s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET  # 可读性orz

    def magenta(self, s):
        return Fore.LIGHTMAGENTA_EX + s + Fore.RESET

    def cyan(self, s):
        return Fore.LIGHTCYAN_EX + s + Fore.RESET

    def white(self, s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET

    def black(self, s):
        return Fore.BLACK + s + Fore.RESET

    def succeed(self, s):
        return Fore.LIGHTWHITE_EX + Back.GREEN + s + Fore.RESET + Back.RESET

    def error(self, s):
        return Fore.LIGHTWHITE_EX + Back.RED + s + Fore.RESET + Back.RESET

    def notice(self, s):
        return Fore.LIGHTWHITE_EX + Back.YELLOW + s + Fore.RESET + Back.RESET

    def p0(self, s):
        return Fore.BLACK + Back.LIGHTWHITE_EX + s + Fore.RESET + Back.RESET

    def p1(self, s):
        return Fore.LIGHTWHITE_EX + Back.GREEN + s + Fore.RESET + Back.RESET

    def p2(self, s):
        return Fore.LIGHTWHITE_EX + Back.BLUE + s + Fore.RESET + Back.RESET

    def p3(self, s):
        return Fore.LIGHTWHITE_EX + Back.MAGENTA + s + Fore.RESET + Back.RESET

    def p4(self, s):
        return Fore.LIGHTWHITE_EX + Back.YELLOW + s + Fore.RESET + Back.RESET

    def p5(self, s):
        return Fore.LIGHTWHITE_EX + Back.CYAN + s + Fore.RESET + Back.RESET

    def p6(self, s):
        return Fore.LIGHTWHITE_EX + Back.RED + s + Fore.RESET + Back.RESET

    def p7(self, s):
        return Fore.LIGHTWHITE_EX + Back.LIGHTBLUE_EX + s + Fore.RESET + Back.RESET

    def p8(self, s):
        return Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + s + Fore.RESET + Back.RESET

    def px(self, s):
        return Fore.BLACK + Back.LIGHTCYAN_EX + s + Fore.RESET + Back.RESET  # 进程太多啦→_→


class Pr(object):
    """
    Make stdout easier.
    'Be filled with convenience.'
    """

    def __init__(self, p, name='', s='Process'):  # 用多线程还是多进程好呢……  ←反正还没有咯……
        self.s = s + ' ' + str(p)
        self.p = p
        self.name = name

    def pr(self, *s):
        name = self.name
        # out = eval("co.p%d('%s') + co.white(' : ')" % (self.p, self.s))

        out = ' '
        for i in xrange(0, len(s), 2):
            if i + 1 < len(s):
                q = s[i + 1]
            else:
                q = 'white'
            if i >= 2:
                name = ''
            out += eval("co.%s('%s%s')" % (q, name, s[i]))

        out = out.decode('utf-8', 'ignore')  # 中文并不是个好主意x

        print out
        # print type(out)


def prepare(list0):
    """
    Convert an irregular list to a regular one.
    "You are so lazy."
    """
    radd = re.compile(r'\w+\.\w+/\w+')  # 网址
    rpat = re.compile(r'(^\d+$)|(\w+\.\w+/\w+)')  # 目录 (反义)
    l, q, bnum = [], 'n', 1

    for a, b in enumerate(list0):
        b = b.strip()

        if b == '' or b.startswith('#') or b.startswith(';'):  # [跳过空行和注释]
            continue
        elif radd.search(b):  # [当前为网址，设为 a]
            if not b.startswith('http'):  # 补上网址前缀
                b = 'http://' + b
            if q == 'abc' or q == 'acb' or q == 'n':  # 上一个已完成
                l.append(b)
            elif q == 'ab':  # 缺少数字
                l.extend(['', b])
            elif q == 'ac':  # 缺少目录
                l.insert(len(l) - 1, 'Book%s/' % str(bnum))
                l.append(b)
                bnum += 1
            elif q == 'a':  # 客官你好吝啬哦
                l.extend(['Book%s/' % str(bnum), '', b])
                bnum += 1
            q = 'a'
            continue

        elif q == 'n':  # 忽略文件开头的不跟随网址的非法行
            print 'List - Line %d is illegal: \n%s' % (a + 1, b)
            continue
        elif not rpat.search(b):  # [当前为目录，加上 b]
            if not b.endswith('/'):
                b += '/'  # 加上反斜杠
            q += 'b'
        elif b.isdigit():  # [当前为数字，加上 c]
            q += 'c'
        else:
            print 'List - Line %d is illegal: \n%s' % (a + 1, b)
            continue

        if q == 'ab':  # 网址付，当前为目录
            l.append(b)
        elif q == 'ac' or q == 'abc':  # 网址付/网址目录付，当前为数字
            l.append(int(b))
        elif q == 'acb':  # 网址数字付，当前为目录
            l.insert(len(l) - 1, b)
        elif q == 'abb' or q == 'acc':  # 客官你好贪心哦
            q = q[:-1]
            print 'List - Line %d is illegal: \n%s' % (a + 1, b)
        else:
            q = q[:-1]
            print 'List - Line %d is illegal: \n%s' % (a + 1, b)

    if q == 'ab':  # 缺少数字
        l.append(1)
    elif q == 'ac':  # 缺少目录
        l.insert(len(l) - 1, 'Book%s/' % str(bnum))
    elif q == 'a':  # 客官你好吝啬哦
        l.extend(['Book%s/' % str(bnum), ''])

    list = []
    for i in xrange(0, len(l), 3):
        list.append([l[i], l[i + 1], l[i + 2]])

    return list


co = Co()
