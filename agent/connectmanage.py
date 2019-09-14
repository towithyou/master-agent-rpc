import zerorpc
from threading import Event, Thread
from config.conf import SERVER_URL, INTERVAL
from utils import get_logger
from .message import Message
from .executor import Executor
from common.state import *
logger = get_logger(__name__, 'agent.log')


class ConnectManage:

    def __init__(self, url=SERVER_URL):
        self.url = url
        self.event = Event()
        self.client = zerorpc.Client()
        self.msg = Message()

        self.executor = Executor()
        self.__result = None
        self.state = WAITING


    def __exec(self, task):
        task_id, script, timeout = task # 如果base64 要注意解码
        # result = self.executor.run(script, timeout) # code, text 脚本执行结果
        code, text= self.executor.run(script, timeout) # code, text 脚本执行结果
        # self.client.result()  rpc服务的result接口，有大问题， 因为rpc 不能跑在线程中
        # 解决用异步的操作方式，拿 未来对象 大材小用
        self.__result = task_id, code, text
        self.state = SUCCESSFUL if code == 0 else FAILED
        # 判断 code 是否为 0 表示任务执行的结果是否成功

    def start(self, interval=INTERVAL):
        # 间隔 1 秒重连
        while not self.event.wait(1):
            try:
                self.client.connect(self.url)
                # 如果连接成功， 则向master 发注册信息
                self.client.reg(self.msg.reg())

                while not self.event.wait(interval): # 下面一直发心跳信息
                    self.client.heartbeat(self.msg.heartbeat())
                     # 这里 self.client.heartbeat 中 reg 方法是master要实现的方法, 这是zerorpc 的要求
                    logger.info('send heartbeat')

                    if self.state in {SUCCESSFUL, FAILED}: # 说明任务已经做完了
                        ack = self.client.result(self.msg.result(*self.__result))  # rpc服务的result接口
                        logger.info('{}'.format(self.__result))
                        self.__result = None
                        self.state = WAITING

                    # 领任务 同步执行，可以改成异步执行
                    if self.state == WAITING:
                        task = self.client.pull_task(self.msg.id)
                        if task: # 判断是否拿到了任务 可能为None
                            self.state = RUNNING
                            Thread(target=self.__exec, args=(task, )).start()

                    # 这里也可以放到消息队列中

            except Exception as e:
                print(e, 'error')
                logger.error(e)

    def shutdown(self):
        self.event.set()
        self.client.close()