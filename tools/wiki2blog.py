#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import sys
from outlink import *

blog_dir = './blog'

def dealcatandtag(file, outdir=None):
    '''
    给分类和tag添加链接
    <strong>内是时间
    <em> 是分类,<code>是tag
    '''

    global blog_dir
    if outdir != None:
        blog_dir = outdir
    outfile = os.path.join(blog_dir, os.path.split(file)[1])
    fin=open(file,'r')
    fout=open(outfile,'w')
    s=fin.read()
    p=r'<div class="content">.*?<div class="span8">(.*?)(<h[^2]|<div class="toc">)'
    s=re.search(p,s,re.DOTALL).group(1)
    # TODO 给分类和tag加上链接
    s=re.sub(r'(<a href=".+?//.+?")(>)',r'\1 target="_blank">',s)
    fout.write(s)
    fin.close()
    fout.close()

def addprevandnext(file, outdir=None):
    pass

def wiki2blog(file):
    print(blog_dir)

    #外链新标签打开
    makelinkout(file, blog_dir)

    #move tag, category, time and so on to right
    #dealcatandtag(file, blog_dir)

    #添加上下篇
    #addprevandnext(file, blog_dir)


if __name__ == '__main__':
    wiki2blog(sys.argv[1])

