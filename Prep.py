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

    def t0(self, s):
        return Fore.BLACK + Back.LIGHTWHITE_EX + s + Fore.RESET + Back.RESET

    def t1(self, s):
        return Fore.LIGHTWHITE_EX + Back.GREEN + s + Fore.RESET + Back.RESET

    def t2(self, s):
        return Fore.LIGHTWHITE_EX + Back.BLUE + s + Fore.RESET + Back.RESET

    def t3(self, s):
        return Fore.LIGHTWHITE_EX + Back.MAGENTA + s + Fore.RESET + Back.RESET

    def t4(self, s):
        return Fore.LIGHTWHITE_EX + Back.YELLOW + s + Fore.RESET + Back.RESET

    def t5(self, s):
        return Fore.LIGHTWHITE_EX + Back.CYAN + s + Fore.RESET + Back.RESET

    def t6(self, s):
        return Fore.LIGHTWHITE_EX + Back.RED + s + Fore.RESET + Back.RESET

    def t7(self, s):
        return Fore.LIGHTWHITE_EX + Back.LIGHTBLUE_EX + s + Fore.RESET + Back.RESET

    def t8(self, s):
        return Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX + s + Fore.RESET + Back.RESET

    def tx(self, s):
        return Fore.BLACK + Back.LIGHTCYAN_EX + s + Fore.RESET + Back.RESET  # 进程太多啦→_→


class Pr(object):
    """
    Make stdout easier.
    'Be filled with convenience.'
    """
    def __init__(self, t, name='', s='Thread'):  # 用多线程还是多进程好呢……  ←反正还没有咯……
        self.s = s + ' ' + str(t)
        self.t = t
        self.name = name

    def pr(self, *s):
        out = eval("co.t%d('%s') + co.white(' : ')" % (self.t, self.s))

        for i in xrange(0, len(s), 2):
            if i + 1 < len(s):
                q = s[i + 1]
            else:
                q = 'white'
            out += eval("co.%s('%s%s')" % (q, self.name, s[i]))

        print out


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

        if b == '':  # [跳过空行]
            continue
        elif radd.search(b):  # [当前为网址，设为 a]
            if not b.startswith('http://'):  # 补上网址前缀
                b = 'http://' + b
            if q == 'abc' or q == 'acb' or q == 'n':  # 上一个已完成
                l.append(b)
            elif q == 'ab':  # 缺少数字
                l.extend(['', b])
            elif q == 'ac':  # 缺少目录
                l.insert(len(l) - 1, 'Book' + str(bnum))
                l.append(b)
                bnum += 1
            elif q == 'a':  # 客官你好吝啬哦
                l.extend(['Book' + str(bnum), '', b])
                bnum += 1
            q = 'a'
            continue

        elif q == 'n':  # 忽略文件开头的不跟随网址的非法行
            print 'List - Line %d is illegal: \n%s' % (a + 1, b)
            continue
        elif not rpat.search(b):  # [当前为目录，加上 b]
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
            l.insert(len(l)-1, b)
        elif q == 'abb' or q == 'acc':  # 客官你好贪心哦
            q = q[:-1]
            print 'List - Line %d is illegal: \n%s' % (a + 1, b)
        else:
            q = q[:-1]
            print 'List - Line %d is illegal: \n%s' % (a + 1, b)

    if q == 'ab':  # 缺少数字
        l.append(1)
    elif q == 'ac':  # 缺少目录
        l.insert(len(l)-1, 'Book' + str(bnum))
    elif q == 'a':  # 客官你好吝啬哦
        l.extend(['Book' + str(bnum), ''])

    return l

co = Co()
