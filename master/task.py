
from common.state import *

class Task:
    '''任务分装类， 任务就是类的一个个实例'''
    def __init__(self, id, script, targets, timeout, parallel=5, fail_count=2,
                 fail_rate=30):
        self.id = id
        self.script = script
        self.timeout = timeout

        self.targets = targets # 选择任务执行的机器的id 存储agent的id
        self.state = WAITING

        self.parallel = parallel # 并发控制
        self.fail_count = fail_count # 有两个失败的就说明此任务失败
        self.fail_rate = fail_rate # 失败率

    def __repr__(self):
        return "<Task {}>".format(self.id)