#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import getopt
from wiki2blog import *
from genpages import *

wiki_dir = './wiki'
html_dir = './html'
blog_dir = './blog'

def usage():
    print('根据vimwiki的结果,修改并生成blog所需相关文件')
    print('usage:')
    print(sys.argv[0]+' [-w wikidir] [-i htmldir] [-o blogdir]')


if __name__ == '__main__':

    try:
        opts,args = getopt.getopt(sys.argv[1:], "w:i:o:")
        for opt,arg in opts:
            if opt == '-w':
                wiki_dir = arg
            elif opt == '-i':
                html_dir = arg
            elif opt == '-o':
                blog_dir = arg
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    wiki_dir = os.path.abspath(wiki_dir)
    html_dir = os.path.abspath(html_dir)
    blog_dir = os.path.abspath(blog_dir)
    print('dirs:',wiki_dir,html_dir,blog_dir)

    # 获取有效html(有对应wiki文件的)
    print('find files...')
    wiki = {}
    for root,dirs,files in os.walk(wiki_dir):
        for f in files:
            if not f.startswith('love_') and not root.endswith('private'):
                a = os.path.splitext(f)
                if a[1] == '.wiki':
                    path = os.path.join(root, f)
                    wiki[a[0]] = path
    html = {}
    for root,dirs,files in os.walk(html_dir):
        for f in files:
            a = os.path.splitext(f)
            # 只保存有对应wiki的html
            if a[1] == '.html' and a[0] in wiki:
                path = os.path.join(root, f)
                print('  ',a[0],path)
                html[a[0]] = path
    # 净化wiki,去除没有对应html的wiki文件
    tmp = {}
    for k,v in wiki.items():
        if k in html:
            print('  ',k,v)
            tmp[k]=v
    wiki = tmp

    # 获取文章属性(时间,分类,tag)
    print('get file attrs...')
    attrs=getattrs(wiki)

    # 生成tag,分类,存档页面
    print('generate pages...')
    genpages(html,attrs,html_dir,blog_dir)

    # 转换页面适应blog
    print('convert htmls...')
    for k,v in html.items():
        print('  ',k,v)
        wiki2blog(v,attrs,html_dir,blog_dir)

