#!/usr/bin/env python
# coding=utf-8
# author:zhouxia
# date:2018-07-24
import subprocess
import os

RC = '\033[1;31m'
GC = '\033[1;32m'
EC = '\033[0m'


def auth_tran(ip, password):
    # 授信操作
    import pexpect
    # ip = sys.argv[1]
    # password = sys.argv[2]
    expect_list = ['(yes/no)', 'password:']

    p = pexpect.spawn('ssh-copy-id %s' % ip)
    try:
        while True:
            idx = p.expect(expect_list)
            # print p.before + expect_list[idx],
            if idx == 0:
                # print "yes"
                p.sendline('yes')
            elif idx == 1:
                # print password
                p.sendline(password)
    except pexpect.TIMEOUT:
        # print >> sys.stderr, 'timeout'
        print(RC + ip + ' 授信异常，请手动授信' + EC)
    except pexpect.EOF:
        # print p.before
        # print >> sys.stderr, '<the end>'
        print(GC + ip + ' 授信完成' + EC)


def check_auth():
    # ip = sys.argv[1]
    # password = sys.argv[2]
    """
        检查本地公私钥文件，授信操作
        如有：直接将本地公钥授信
        如无：生成新的公私钥，再进行授信
    """

    host = open("host_list.txt")
    line = host.readline()
    homePath = os.environ['HOME']

    if not os.path.exists(homePath + '/.ssh/id_rsa.pub'):
        # print (RC + '本地已存在公私钥文件，准备授信操作...' + EC)
        print ('开始生成本地公私钥文件...')
        status = subprocess.call("/usr/bin/ssh-keygen -t rsa -f ~/.ssh/id_rsa -P ''", shell=True)
        if status == 0:
            print(GC + '本地公私钥文件生成完成' + EC + '，准备授信操作...')
            while line:
                if line == "":
                    continue
                hostlist = line.split(' ')
                ipaddr = hostlist[0]
                passwd = hostlist[1]
                auth_tran(ipaddr, passwd)
                line = host.readline()

    else:
        print ('本地已存在公私钥文件，准备授信操作...')
        while line:
            if line == "":
                continue
            hostlist = line.split(' ')
            ipaddr = hostlist[0]
            passwd = hostlist[1]
            auth_tran(ipaddr, passwd)
            line = host.readline()


check_auth()