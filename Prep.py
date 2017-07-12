#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from colorama import init, Fore, Back, ansi  # 第三方库

init(autoreset=True, strip=False)


class Co(object):
    """
    Colorize stdout.
    "It’s not RGB lighting."
    """
    def red(self, s):
        return Back.RESET + Fore.LIGHTRED_EX + s + Fore.RESET

    def green(self, s):
        return Back.RESET + Fore.LIGHTGREEN_EX + s + Fore.RESET

    def yellow(self, s):
        return Back.RESET + Fore.LIGHTYELLOW_EX + s + Fore.RESET

    def blue(self, s):
        return Back.RESET + Fore.LIGHTBLUE_EX + s + Fore.RESET  # 可读性orz

    def magenta(self, s):
        return Back.RESET + Fore.LIGHTMAGENTA_EX + s + Fore.RESET

    def cyan(self, s):
        return Back.RESET + Fore.LIGHTCYAN_EX + s + Fore.RESET

    def white(self, s):
        return Back.RESET + Fore.LIGHTWHITE_EX + s + Fore.RESET

    def black(self, s):
        return Back.RESET + Fore.BLACK + s + Fore.RESET

    def done(self, s):
        return Fore.BLACK + Back.LIGHTGREEN_EX + s + Fore.RESET + Back.RESET

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


def prepare(list0):
    """
    Convert a nonstandard list to a standard one.
    "You are so lazy."
    """
    radd = re.compile(r'\w+\.\w+/\w+')  # 网址
    rpat = re.compile(r'(^\d+$)|(\w+\.\w+/\w+)')  # 目录 (反义)
    l, q, bnum = [], 'n', 1

    for a, b in enumerate(list0):
        b = b.replace('\n', '').strip()
        if radd.search(b):  # [当前为网址，设为 a]
            if q == 'abc' or q == 'acb' or q == 'n':  # 上一个已完成
                l.append(b)
            elif q == 'ab':  # 缺少数字
                l.extend([1, b])
            elif q == 'ac':  # 缺少目录
                l.insert(len(l) - 1, 'Book' + str(bnum))
                l.append(b)
                bnum += 1
            elif q == 'a':  # 客官你好吝啬哦
                l.extend(['Book' + str(bnum), 1, b])
                bnum += 1
            q = 'a'
            continue

        if q == 'n':  # 忽略文件开头的不跟随网址的无意义行
            print 'List : Line %d is illegal.' % (a + 1)
            continue

        if b == '':  # [空行]
            continue
        elif not rpat.search(b):  # [当前为目录，加上 b]
            q += 'b'
        elif b.isdigit():  # [当前为数字，加上 c]
            q += 'c'
        else:
            print 'List : Line %d is illegal.' % (a + 1)
            continue

        if q == 'ab':  # 网址付，当前为目录
            l.append(b)
        elif q == 'ac' or q == 'abc':  # 网址付/网址目录付，当前为数字
            l.append(int(b))
        elif q == 'acb':  # 网址数字付，当前为目录
            l.insert(len(l)-1, b)
        elif q == 'abb' or q == 'acc':
            q = q[:-1]
        else:
            print 'List : Line %d is illegal.' % (a + 1)

    if q == 'ab':  # 缺少数字
        l.append(1)
    elif q == 'ac':  # 缺少数字
        l.insert(len(l)-1, 'Book' + str(bnum))
    elif q == 'a':  # 客官你好吝啬哦
        l.extend(['Book' + str(bnum), 1])

    return l
