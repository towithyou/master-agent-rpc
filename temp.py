import logging
from logging.handlers import RotatingFileHandler

import subprocess
import os


def get_log(level=logging.INFO, logname='log1'):
    logger = logging.getLogger(logname)
    logger.setLevel(level)  # 日志级别
    logger.propagate = False  # 传播

    # handle = logging.FileHandler('a.log') # 原始没有日志滚动
    handle = RotatingFileHandler('a.log', maxBytes=10 * 1024, backupCount=5, encoding='utf-8')
    handle.setLevel(level)  # handler 初始日志级别

    fmt = logging.Formatter("**** %(message)s ****")
    handle.setFormatter(fmt)  # 为 handler 设置输出格式

    logger.addHandler(handle)
    return logger


# def proc_test():
#     proc = subprocess.Popen('dir'.split(), shell=True, stdout=subprocess.PIPE,
#                             stderr=subprocess.PIPE
#                             )

def tmp():
    import paramiko

    client = paramiko.SSHClient()

    # 如果known_hosts 没有登录信息会报错，不让登录
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # keyfile = r'C:/Users/DuanHaiquan/.ssh/id_rsa'
    # key = paramiko.RSAKey.from_private_key_file(keyfile)

    # ssh-keygen.exe -m PEM -t rsa # -m 指定生成秘钥的格式 PEM(RSA) -t 创建的密钥类型 必须用这种创建，否则会报错
    # client.connect('192.168.214.147', 22, 'root', '123123') # 公钥已传送
    # client.connect('192.168.214.147', 22, 'root', key_filename=r'C:/Users/DuanHaiquan/.ssh/id_rsa') 不好使
    client.connect('192.168.214.147', 22, 'root')
    # stdin, stdout, stderr = client.exec_command('ifconfig')
    # print(stdout.read())
    # print(stderr.read())
    client.close()

# import platform
# print (platform.system())
# print(__file__)
# print(os.path.split(__file__)[1])
# print(os.path.splitext(os.path.split(__file__)[1])[0])

import sys
# print(sys.path)
# sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
import socket

# print(socket.gethostname())

import netifaces

import ipaddress
# print (netifaces.interfaces())

def fn():
    for iface in netifaces.interfaces():
        x = netifaces.ifaddresses(iface)
        ipv4s = x.get(2, [])
        if ipv4s:
            for ipv4 in ipv4s:
                ip = ipaddress.ip_address(ipv4.get('addr'))
                # print(1, ip.version)
                # print(2, ip.is_global)
                # print(3, ip.is_link_local) # win 中没用
                # print(4, ip.is_loopback)  # 回环
                # print(5, ip.is_multicast) # 组播
                # print(6, ip.is_private)
                # print(7, ip.is_reserved) #保留
                # print(8, ip.is_site_local)
                # print(9, ip.is_unspecified)
                if ip.version != 4:
                    continue
                if ip.is_link_local:
                    continue
                if ip.is_loopback:
                    continue
                if ip.is_multicast:
                    continue
                if ip.is_reserved:
                    continue

                print(ip)

import zerorpc

class HelloRPC(object):
    def hello(self, name):
        return "Hello, %s" % name

# s = zerorpc.Server(HelloRPC())
# s.bind("tcp://0.0.0.0:9999")
# s.run()

# 



