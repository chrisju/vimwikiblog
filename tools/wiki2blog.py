#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import time
import sys
from outlink import *


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

def dealcatandtag(s, attrs):
    '''
    给分类和tag添加链接
    <strong>内是时间
    <em> 是分类,<code>是tag
    '''

    sout=''
    p=r'(^.*?<h2.*?>)(.+?)(</h2>.*?)'
    p=p+r'(<p>\s*)(.+?)(\s*<div class="toc">|\s*<h)(.+?)$'
    m=re.search(p,s,re.DOTALL)
    if m:
        s2=m.group(5).strip()
        if isvimwikibloghead(s2):
            sout = m.group(1)+m.group(2)+m.group(3)+m.group(4)
            # 重写文章属性栏 给分类和tag加上链接
            sout = sout + '<ul class="tag_box inline">\n'
            # 不显示时间
            #p=r'<strong>(.+?)</strong>'
            #if re.search(p,s2):
            #    timestr=re.search(p,s2).group(1)
            #    sout = sout + str.format('<li><a href="Archive.html">{0}</a></li>\n',timestr.split()[0])
            p=r'<em>(.+?)</em>'
            if re.search(p,s2):
                cat=re.search(p,s2).group(1)
                num = 0
                if attrs:
                    for wiki,attr in attrs.items():
                        if attr and cat == attr.cat:
                            num = num + 1
                sout = sout + str.format('<li><a href="Categories.html#{0}">{0} <span>{1}</span></a></li>\n',cat,num)
            p=r'<code>(.+?)</code>'
            tags = re.findall(p,s2)
            for tag in tags:
                num = 0
                if attrs:
                    for wiki,attr in attrs.items():
                        if attr and tag in attr.tags:
                            num = num + 1
                sout = sout + str.format('<li><a href="Tags.html#{0}">{0} <span>{1}</span></a></li>\n',tag,num)
            sout = sout + '</ul>\n'
            sout = sout + m.group(6)+m.group(7)
    if not sout:
        sout = s
    return sout

def addprevandnext(name, s, attrs):
    sformat = '''
    <hr style="clear:both">
    <div class="pagination" style="float:left;">
      <ul>
        {0}
        <li><a href="Archive.html">Archive</a></li>
        {1}
      </ul>
    </div>
    <hr>'''
    format_prev='<li class="prev"><a href="{0}" title="上一篇: {1}">&larr; {1}</a></li>'
    format_next='<li class="next"><a href="{0}" title="下一篇: {1}">{1} &rarr;</a></li>'
    p=r'<!-- disqus -->'
    lastname = ''
    nextname = ''
    isnext = False
    if attrs:
        #print(name)
        for k,v in sorted(attrs.items(), key=lambda p:p[1].time if p[1] else time.gmtime(0)):
            if v:
                #print(k,v.title,v.time)
                if isnext:
                    nextname = k
                    break;
                if k == name:
                    isnext = True
                else:
                    lastname = k
    #print('prev&next:',lastname,nextname)
    #input()

    sprev = ''
    snext = ''
    if lastname:
        sprev = format_prev.format(lastname+'.html', attrs[lastname].title)
    if nextname:
        snext = format_next.format(nextname+'.html', attrs[nextname].title)

    news = sformat.format(sprev,snext)
    sout = re.sub(p,news,s,flags=re.DOTALL)
    return sout

def wiki2blog(file,attrs,indir,outdir):
    global html_dir
    global blog_dir
    html_dir = indir
    blog_dir = outdir
    fin=open(file,'r')
    s=fin.read()
    fin.close()

    #外链新标签打开
    s = makelinkout(s)

    print('wiki2blog:'+file)
    if not os.path.split(file)[1].startswith('const_'):

        #修饰tag, category, time
        s = dealcatandtag(s, attrs)

        # 添加上下篇
        name = os.path.splitext(os.path.basename(file))[0]
        s = addprevandnext(name, s, attrs)

    outfile = file.replace(html_dir,blog_dir)
    dir = os.path.split(outfile)[0]
    if not os.path.exists(dir):
        os.makedirs(dir)
    fout=open(outfile,'w')
    fout.write(s)
    fout.close()


if __name__ == '__main__':
    blog_dir = './blog'
    html_dir = './html'
    wiki2blog(sys.argv[1],None,html_dir,blog_tmp)

