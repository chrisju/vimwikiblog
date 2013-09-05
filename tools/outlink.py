#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import sys

blog_dir = './blog'

def makelinkout(file, outdir=None):
    '''使http,https,mailto等外部链接在新页面打开'''
    global blog_dir
    if outdir != None:
        blog_dir = outdir
    outfile = os.path.join(blog_dir, os.path.split(file)[1])
    fin=open(file,'r')
    fout=open(outfile,'w')
    s=fin.read()
    s=re.sub(r'(<a href=".+?//.+?")(>)',r'\1 target="_blank">',s)
    fout.write(s)
    fin.close()
    fout.close()


if __name__ == '__main__':
    makelinkout(sys.argv[1])
