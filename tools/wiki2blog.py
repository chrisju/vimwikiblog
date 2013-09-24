#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import sys
from outlink import *

blog_dir = './blog'

def isvimwikibloghead(s):

    # 每行都只会是以下几种情况
    p=r'(^<strong>.+?</strong>$)|(^<em>.+?</em>$)|(^<code>.+?</code>$)'
    for line in s.splitlines():
        if not re.search(p,line.strip()):
            return False
    # 日期必须有,分类不能大于一个
    if len(re.findall(r'<strong>(.+?)</strong>',s)) != 1 or len(re.findall(r'<em>(.+?)</em>',s)) > 1:
        return False
    return True

def dealcatandtag(file, outdir=None, attrs=None):
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
    sout=''
    p=r'(^.*?<h2.*?>)(.+?)(</h2>.*?)'
    p=p+r'(<p>\s*)(.+?)(\s*<div class="toc">|\s*<h)(.+?)$'
    m=re.search(p,s,re.DOTALL)
    if m:
        s2=m.group(5).strip()
        if isvimwikibloghead(s2):
            sout = m.group(1)+m.group(2)+m.group(3)+m.group(4)
            # 重写文章属性栏 给分类和tag加上链接
            # TODO 传入分类和tag的统计数据
            sout = sout + '<ul class="tag_box inline">\n'
            p=r'<strong>(.+?)</strong>'
            if re.search(p,s2):
                timestr=re.search(p,s2).group(1)
                sout = sout + str.format('<li>{0}</li>\n',timestr)
            p=r'<em>(.+?)</em>'
            if re.search(p,s2):
                cat=re.search(p,s2).group(1)
                num = 0
                if attrs:
                    for wiki,attr in attrs.items():
                        if cat == attr.cat:
                            num = num + 1
                sout = sout + str.format('<li><a href="Categories.html#{0}">{0} <span>{1}</span></a></li>\n',cat,num)
            p=r'<code>(.+?)</code>'
            tags = re.findall(p,s2)
            for tag in tags:
                num = 0
                if attrs:
                    for wiki,attr in attrs.items():
                        if tag in attr.tags:
                            num = num + 1
                sout = sout + str.format('<li><a href="Tags.html#{0}">{0} <span>{1}</span></a></li>\n',tag,num)
            sout = sout + '</ul>\n'
            sout = sout + m.group(6)+m.group(7)
    if not sout:
        sout = s
    fout.write(sout)
    fin.close()
    fout.close()

def addprevandnext(file, outdir=None):
    pass

def wiki2blog(file,attrs=None):
    print(blog_dir)

    #外链新标签打开
    makelinkout(file, blog_dir)

    #修饰tag, category, time
    dealcatandtag(file, blog_dir, attrs)

    #添加上下篇
    #addprevandnext(file, blog_dir)


if __name__ == '__main__':
    wiki2blog(sys.argv[1])

