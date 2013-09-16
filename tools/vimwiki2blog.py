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
        opts,args = getopt.getopt(sys.argv[1:], "io")
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

    print(wiki_dir)
    print(html_dir)
    print(blog_dir)

    #遍历.wiki生成的html
    wiki = {}
    for root,dirs,files in os.walk(wiki_dir):
        for f in files:
            a = os.path.splitext(f)
            if a[1] == '.wiki':
                print(a[0])
                path = os.path.join(root, f)
                wiki[a[0]] = path
    html = {}
    for root,dirs,files in os.walk(html_dir):
        for f in files:
            a = os.path.splitext(f)
            if a[1] == '.html' and wiki.has_key(a[0]):
                path = os.path.join(root, f)
                html[a[0]] = path

    for k,v in html.items():
        print(k,v)
        wiki2blog(v)

    #生成tag,分类,存档页面
    genpages(html)

