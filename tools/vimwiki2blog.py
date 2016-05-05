#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import optparse
from wiki2blog import *
from genpages import *
from util import *
import ftp
import filecmp
import shutil as sh
import json


if __name__ == '__main__':

    usage = '根据vimwiki的结果,修改并生成blog所需相关文件 \n%prog -h for help'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-c","--config-file",dest="cfg",default='~/.config/vimwikiblog/config.json',help="config file. default is ~/.config/vimwikiblog/config.json",metavar="FILE")
    parser.add_option("-u",action="store_true",dest="uploadonly",help="don't generate blog, only upload files in blog_tmp")
    parser.add_option("--upall",action="store_true",dest="uploadall",help="upload all files")
    (options,args )= parser.parse_args()

    print('config file:',options.cfg)
    with open(os.path.expanduser(options.cfg)) as f:
        j = json.load(f)

    gentpl = j['basic']['gentpl']
    wiki_dir = j['basic']['wiki']
    html_dir = j['basic']['html']
    blog_dir = j['basic']['blog']
    blog_tmp = j['basic']['blog_tmp']
    uploads = j['upload']

    changed = []

    if options.uploadonly:
        # 上传blog_tmp的内容
        if os.path.exists(blog_tmp):
            adds=[]
            for root,dirs,files in os.walk(blog_tmp):
                for name in files:
                    f = os.path.relpath(os.path.join(root,name),blog_tmp)
                    adds.append(f)
            # 提交更改到远程
            uploaded = False
            for up in uploads:
                if up['enable']:
                    uploaded = True
                    if up['type'] == 'ftp':
                        print('uploading to %s ...' % (up['host']))
                        ftp.update(up,blog_tmp,adds)
            # 删除blog_tmp
            if uploaded:
                print('removing:', blog_tmp)
                sh.rmtree(blog_tmp, ignore_errors=True)
        sys.exit(0)

    # 准备文件夹
    if not os.path.exists(blog_dir):
        os.makedirs(blog_dir)
    if not blog_tmp:
        blog_tmp = blog_dir
    else:
        if os.path.exists(blog_tmp):
            # 获取未提交的更改
            for root,dirs,files in os.walk(blog_tmp):
                for file in files:
                    if file.endswith('html'):
                        changed.append(os.path.relpath(os.path.join(root,file),blog_tmp))
            # 删除文件夹
            print('removing:', blog_tmp)
            sh.rmtree(blog_tmp, ignore_errors=True)
        os.makedirs(blog_tmp)
    print('dirs:',wiki_dir,html_dir,blog_dir,blog_tmp)

    # 获取有效html(有对应wiki文件的)
    print('find files...')
    wiki = {}
    for root,dirs,files in os.walk(wiki_dir):
        for f in files:
            #if not f.startswith('love_') and not root.endswith('private'):
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
    genpages(gentpl,html,attrs,html_dir,blog_tmp)

    # 转换页面适应blog
    print('convert htmls...')
    for k,v in html.items():
        print('  ',k,v)
        wiki2blog(v,attrs,html_dir,blog_tmp)

    if blog_dir != blog_tmp:
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
        changed += adds+diffs

        # 更新blog_dir
        for name in changed:
            dir = os.path.split(name)[0]
            if dir:
                dir = os.path.join(blog_dir,dir)
                if not os.path.exists(dir):
                    os.makedirs(dir)
            sh.copyfile(os.path.join(blog_tmp,name),os.path.join(blog_dir,name))
        for name in rms:
            file = os.path.join(blog_dir,name)
            print('removing:', file)
            re_clean(file) # 删除文件 并递归清空空文件夹
        os.makedirs(blog_dir,exist_ok=True) # 如果连blog_dir都被删了就补回来

        # 清理blog_tmp
        if not options.uploadall:
            for root,dirs,files in os.walk(blog_tmp):
                for file in files:
                    name = os.path.relpath(os.path.join(root,file),blog_tmp)
                    if name not in changed:
                        re_clean(os.path.join(blog_tmp,name))

        if changed or options.uploadall:
            # 提交更改到远程
            uploaded = False
            for up in uploads:
                if up['enable']:
                    uploaded = True
                    if up['type'] == 'ftp':
                        print('uploading to %s ...' % (up['host']))
                        ftp.update(up,blog_tmp,new if options.uploadall else changed,rms)
            # 删除blog_tmp
            if uploaded:
                print('removing:', blog_tmp)
                sh.rmtree(blog_tmp, ignore_errors=True)

