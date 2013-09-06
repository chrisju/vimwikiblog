#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import sys

blog_dir = './blog'

def rearrange(infile, outfile):
    '''使http,https,mailto等外部链接在新页面打开'''
    fin=open(file,'r')
    fout=open(outfile,'w')
    s=fin.read()

    p=r'<p>(.+?)</p>.*' # TODO 添加位置有效判断
    m=re.search(p,s,re.DOTALL)
    if m:
        ps=m.group()
        print(ps)

    fout.write(s)
    fin.close()
    fout.close()


if __name__ == '__main__':
    makelinkout(sys.argv[1])

