#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

def re_clean(f):
    '''
    删除文件或文件夹 若删除后母文件夹为空 则删除母文件夹 递归执行
    '''
    try:
        if os.path.isfile(f):
            os.remove(f)
        elif os.path.isdir(f):
            os.rmdir(f)
        dir = os.path.split(f)[0]
        if not os.listdir(dir):
            re_clean(dir)
    except:
        pass
