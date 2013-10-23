#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ftplib import FTP
import socket
import os

host='192.168.0.245'
port = 21
remote_dir = '/misc'
user='sa'
pwd='sa'


def update(root,adds,rms=[]):
    '''
    更新到服务器
    adds: 上传的文件列表
    rms: 删除的文件列表
    '''

    ftp = FTP()
    timeout = 20
    socket.setdefaulttimeout(timeout)
    ftp.set_pasv(True)
    ftp.connect(host, port)
    ftp.login(user,pwd)
    ftp.cwd(remote_dir)

    for name in adds:
        dir = os.path.split(name)[0]
        if dir:
            ftp.mkd(dir)
        with open(os.path.join(root,name),'rb') as f:
            ftp.storbinary('STOR %s' % name, f)
    for name in rms:
        try:
            ftp.delete(name)
            # TODO 清理空文件夹
        except:
            print(str.format('delete {0} failed.',name))

    ftp.close()


if __name__ == '__main__':

    update('/mnt/DATA/tmp',['hosts'],['abc'])
