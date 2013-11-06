#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import sys


def makelinkout(s):
    '''使http,https,mailto等外部链接在新页面打开'''
    s=re.sub(r'(<a href=".+?//.+?")(>)',r'\1 target="_blank">',s)
    return s


if __name__ == '__main__':
    blog_dir = './blog'
    file=sys.argv[1]
    fin=open(file,'r')
    s=fin.read()
    fin.close()

    s = makelinkout(s)

    outfile = os.path.join(blog_dir, os.path.split(file)[1])
    fout=open(outfile,'w')
    fout.write(s)
    fout.close()
