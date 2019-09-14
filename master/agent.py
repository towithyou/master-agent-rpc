
import datetime
from common.state import *


class Agent:
    '''客户端注册的信息需要封装， 提供一个信息存储的类， 数据存储在类的实例中'''
    def __init__(self, id, hostname, ip):
        self.id = id
        self.hostname = hostname
        self.ip = ip
        self.regtime = datetime.datetime.now() # 服务器生出注册时间
        self.state = WAITING # 可以在注册的时候把状态带上
        self.outputs = {} # 每个agent执行任务的信息和结果
        # 如果遍历任务和结果从这里面拿
        # {task_id:{code:0, ret:'result'}} 需要放到redis中

        self.lastupdatetime = None


    def __repr__(self):
        return "<Agent {} {}>".format(self.id, self.outputs)

