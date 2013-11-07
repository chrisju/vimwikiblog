#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ftplib import FTP
import socket
import os,sys


def re_clean(ftp,f):
    '''
    删除文件或文件夹 若删除后母文件夹为空 则删除母文件夹 递归执行
    '''
    try:
        ftp.delete(f)
    except:
        pass
    try:
        ftp.rmd(f)
    except:
        pass
    dir = os.path.split(f)[0]
    if dir:
        n = len(tuple(ftp.mlsd(path=dir)))
        if n == 0:
            re_clean(ftp,dir)

def update(server,root,adds,rms=[]):
    '''
    更新到服务器
    adds: 上传的文件列表
    rms: 删除的文件列表
    '''

    ftp = FTP()
    timeout = 20
    socket.setdefaulttimeout(timeout)
    ftp.set_pasv(True)
    ftp.connect(server['host'], server['port'])
    ftp.login(server['user'],server['pwd'])
    ftp.cwd(server['remote_dir'])

    for name in adds:
        dir = os.path.split(name)[0]
        if dir:
            ftp.mkd(dir)
        with open(os.path.join(root,name),'rb') as f:
            print('uploading %s...' % (name))
            ftp.storbinary('STOR %s' % name, f)
    for name in rms:
        re_clean(ftp,name)

    ftp.close()


server={
        "host":"192.168.0.245",
        "port": 21,
        "remote_dir": "/misc",
        "user":"sa",
        "pwd":"sa"
        }
if __name__ == '__main__':

    update(server,'/mnt/DATA/tmp',['hosts'],['t/adb.log'])
