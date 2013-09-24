#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import sys
import time

wiki_dir = './wiki'
blog_dir = './blog'
archivetpl = 'config/genpage.tpl'

class Attr:

    def __init__(self,time=None,cat=None,tags=None,title=None):

        self.time = time
        self.cat = cat
        self.tags = tags
        self.title = title


def isvimwikibloghead(s):

    # 每行都只会是以下几种情况
    p=r'(^\*.+?\*$)|(^_.+?_$)|(^`.+?`$)'
    for line in s.splitlines():
        if not re.search(p,line.strip()):
            return False
    # 日期必须有,分类不能大于一个
    if len(re.findall(r'\*(.+?)\*',s)) != 1 or len(re.findall(r'_(.+?)_',s)) > 1:
        return False
    return True


def getwikiattr(wikifile):

    a = Attr()
    fin=open(wikifile,'r')
    s=fin.read()
    fin.close()

    p=r'==\s+?(.+?)\s+?==\s*'
    if re.search(p,s):
        a.title=re.search(p,s).group(1)
    p = p + r'(.+?)(----|%toc|===)'
    m=re.search(p,s,re.DOTALL)
    if m:
        s=m.group(2)
        if isvimwikibloghead(s):
            p=r'\*(.+?)\*' # ==1
            if re.search(p,s):
                timestr=re.search(p,s).group(1)
                a.time=time.strptime(timestr,"%Y-%m-%d %H:%M:%S")
            p=r'_(.+?)_' # <=1
            if re.search(p,s):
                a.cat=re.search(p,s).group(1)
            p=r'`(.+?)`'
            a.tags=re.findall(p,s)
    if not a.time:
        a.time = time.gmtime(0)
    if not a.cat:
        a.cat = '未分类'
    if not a.title:
        a.title = os.path.splitext(wikifile)[0]
    return a


def savearchive(sar):

    global blog_dir
    global archivetpl
    infile = archivetpl
    outfile = os.path.join(blog_dir, 'Archive.html')
    fin=open(infile,'r')
    fout=open(outfile,'w')
    s=fin.read()
    s=re.sub('%title%','Archive',s)
    s=re.sub('%string%',sar,s)
    fout.write(s)
    fin.close()
    fout.close()

def savecat(sar):

    global blog_dir
    global archivetpl
    infile = archivetpl
    outfile = os.path.join(blog_dir, 'Categories.html')
    fin=open(infile,'r')
    fout=open(outfile,'w')
    s=fin.read()
    s=re.sub('%title%','Categories',s)
    s=re.sub('%string%',sar,s)
    fout.write(s)
    fin.close()
    fout.close()

def savetag(sar):

    global blog_dir
    global archivetpl
    infile = archivetpl
    outfile = os.path.join(blog_dir, 'Tags.html')
    fin=open(infile,'r')
    fout=open(outfile,'w')
    s=fin.read()
    s=re.sub('%title%','Tags',s)
    s=re.sub('%string%',sar,s)
    fout.write(s)
    fin.close()
    fout.close()


def getattrs(wikidict=None):
    attrs = {}
    if wikidict:
        for k,v in wikidict.items():
            attrs[k] = getwikiattr(v)
    else:
        for root,dirs,files in os.walk(wiki_dir):
            for f in files:
                a = os.path.splitext(f)
                if a[1] == '.wiki':
                    path = os.path.join(root, f)
                    attrs[a[0]] = getwikiattr(path)
    return attrs

def genpages(htmldict=None,attrs=None):
    '''
    生成首页
    生成存档页
    生成分类页
    生成tag页
    生成其它页
    注意: 开头需满足一定格式
    '''

    # 获取所有页面的时间,分类,tag数据
    if not attrs:
        attrs = getattrs()
    # 生成archive
    mons=['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月',]
    s=''
    dcat = {}
    for k,v in attrs.items():
        key=time.strftime("%Y-%m",v.time)
        if not dcat.get(key):
            dcat[key] = []
        dcat[key].append(k)
    oldyear=0
    for k,v in sorted(dcat.items(),reverse=True):
        print(k,len(v),v)
        tm = time.strptime(k,"%Y-%m")
        if oldyear != tm.tm_year:
            oldyear = tm.tm_year
            s = s + str.format('<h3>{0}</h3>\n', tm.tm_year)
        s = s + str.format('<h4>{0}</h4>\n', mons[tm.tm_mon - 1])
        s = s + '<ul>\n'
        v.sort(key=lambda p:attrs[p].time,reverse=True)
        for wiki in v:
            a=attrs[wiki]
            format = '<li><span>{0}</span> &raquo; <a href="{1}">{2}</a></li>\n'
            date = str.format('{0}年{1}月{2}日',a.time.tm_year,a.time.tm_mon,a.time.tm_mday)
            path = wiki+'.html'
            if htmldict:
                path = htmldict[wiki]
            title = a.title
            s = s + str.format(format, date, path, title)
        s = s + '</ul>\n'
    print(s)
    savearchive(s)

    # 生成分类
    s=''
    dcat = {}
    for k,v in attrs.items():
        if not dcat.get(v.cat):
            dcat[v.cat] = []
        dcat[v.cat].append(k)
    for k,v in sorted(dcat.items()):
        print(k,len(v),v)
        s = s + str.format('<h3 id="{0}">{0}</h3>\n', k)
        s = s + '<ul>\n'
        v.sort(key=lambda p:attrs[p].time,reverse=True)
        for wiki in v:
            a=attrs[wiki]
            format = '<li><span>{0}</span> &raquo; <a href="{1}">{2}</a></li>\n'
            date = str.format('{0}年{1}月{2}日',a.time.tm_year,a.time.tm_mon,a.time.tm_mday)
            path = wiki+'.html'
            if htmldict:
                path = htmldict[wiki]
            title = a.title
            s = s + str.format(format, date, path, title)
        s = s + '</ul>\n'
    print(s)
    savecat(s)

    # 生成Tag
    s=''
    dcat = {}
    for k,v in attrs.items():
        if v.tags:
            for tag in v.tags:
                if not dcat.get(tag):
                    dcat[tag] = []
                dcat[tag].append(k)
    for k,v in sorted(dcat.items()):
        print(k,len(v),v)
        s = s + str.format('<h3 id="{0}">{0}</h3>\n', k)
        s = s + '<ul>\n'
        v.sort(key=lambda p:attrs[p].time,reverse=True)
        for wiki in v:
            a=attrs[wiki]
            format = '<li><span>{0}</span> &raquo; <a href="{1}">{2}</a></li>\n'
            date = str.format('{0}年{1}月{2}日',a.time.tm_year,a.time.tm_mon,a.time.tm_mday)
            path = wiki+'.html'
            if htmldict:
                path = htmldict[wiki]
            title = a.title
            s = s + str.format(format, date, path, title)
        s = s + '</ul>\n'
    print(s)
    savetag(s)



if __name__ == '__main__':
    genpages()


