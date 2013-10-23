#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import optparse
from wiki2blog import *
from genpages import *
import ftp
import filecmp
import shutil as sh

wiki_dir = './wiki'
html_dir = './html'
blog_dir = './blog'
blog_tmp = './blog_tmp'

def usage():
    print('根据vimwiki的结果,修改并生成blog所需相关文件')
    print('usage:')
    print(sys.argv[0]+' [-w wikidir] [-i htmldir] [-o blogdir]')

if __name__ == '__main__':

    usage = '根据vimwiki的结果,修改并生成blog所需相关文件 \n%prog -h for help'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-w","--wiki",dest="wiki",default=wiki_dir,help="wiki dir. default:"+wiki_dir,metavar="PATH")
    parser.add_option("-i","--html",dest="html",default=html_dir,help="wiki output dir, has origin html. default:"+html_dir,metavar="PATH")
    parser.add_option("-o","--out",dest="blog",default=blog_dir,help="blog files output dir. default:"+blog_dir,metavar="PATH")
    parser.add_option("","--tmp",dest="blog_tmp",default=blog_tmp,help="changed blog files dir. default:"+blog_tmp,metavar="PATH")
    parser.add_option("-u","",action="store_true",dest="upload",default=False,help="upload to server. need set parameters in ftp.py")
    parser.add_option("","--notmp",action="store_true",dest="notmp",default=False,help="not use tmp dir, will not figer out changed files and can't upload")
    (options,args )= parser.parse_args()

    wiki_dir = os.path.abspath(options.wiki)
    html_dir = os.path.abspath(options.html)
    blog_dir = os.path.abspath(options.blog)
    blog_tmp = os.path.abspath(options.blog_tmp)
    if not os.path.exists(blog_dir):
        os.makedirs(blog_dir)
    if options.notmp:
        blog_tmp = blog_dir
    else:
        if os.path.exists(blog_tmp):
            sys.exit(str.format('tmp dir "{0}" exist! pelease remove it manually.',blog_tmp))
        else:
            os.makedirs(blog_tmp)
    print('dirs:',wiki_dir,html_dir,blog_dir,blog_tmp)

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
    genpages(html,attrs,html_dir,blog_tmp)

    # 转换页面适应blog
    print('convert htmls...')
    for k,v in html.items():
        print('  ',k,v)
        wiki2blog(v,attrs,html_dir,blog_tmp)

    if not options.notmp:
        # 比较与原始blog的差别
        diffs=[]
        adds=[]
        rms=[]
        old=[]
        new=[]
        for root,dirs,files in os.walk(blog_dir):
            for file in files:
                if file.endswith('html'):
                    old.append(os.path.relpath(os.path.join(root,file),blog_dir))
        for root,dirs,files in os.walk(blog_tmp):
            for file in files:
                if file.endswith('html'):
                    new.append(os.path.relpath(os.path.join(root,file),blog_tmp))
        for f in new:
            oldf = os.path.join(blog_dir,f)
            if not os.path.exists(oldf):
                adds.append(f)
            else:
                newf = os.path.join(blog_tmp,f)
                if not filecmp.cmp(oldf,newf,False):
                    diffs.append(f)
        for f in old:
            newf = os.path.join(blog_tmp,f)
            if not os.path.exists(newf):
                rms.append(f)
        print('新增:',adds)
        print('更改:',diffs)
        print('删除:',rms)
        changed = adds+diffs

        # 更新blog_dir
        for name in changed:
            dir = os.path.split(name)[0]
            if dir:
                dir = os.path.join(blog_dir,dir)
                if not os.path.exists(dir):
                    os.makedirs(dir)
            sh.copyfile(os.path.join(blog_tmp,name),os.path.join(blog_dir,name))
        for name in rms:
            print('removing:', name)
            os.remove(os.path.join(blog_dir,name))
            # TODO 清理空文件夹

        # 清理blog_tmp
        for root,dirs,files in os.walk(blog_tmp):
            for file in files:
                name = os.path.relpath(os.path.join(root,file),blog_tmp)
                if name not in changed:
                    os.remove(os.path.join(blog_tmp,name))

        if options.upload:
            # 提交更改到远程
            print('uploading...')
            ftp.update(blog_tmp,adds+diffs,rms)
            # 删除blog_tmp
            print('removing:', blog_tmp)
            os.system('rm -rf '+ blog_tmp)

