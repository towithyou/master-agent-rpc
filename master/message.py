from utils import get_logger
from .storage import Storage

logger = get_logger(__name__, 'master.log')

class Message:
    '''暴露给客户端的传消息的接口'''
    def __init__(self):
        self.store = Storage()

    def reg(self, msg:dict):
        logger.warning('reg {}'.format(msg))
        self.store.reg(msg['id'], msg['hostname'], msg['ips'])
        ts = msg['timestamp'] # 时间校验
        return 'reg {}'.format(msg)

    def heartbeat(self, msg):
        logger.warning('hb {}'.format('ok'))
        self.store.heartbeat(msg['id'], msg['hostname'], msg['ips'])
        return 'hb {}'.format(msg)

    def add_task(self, task:dict): # 添加任务 http: json => webserver-> master => dict
        return self.store.add_task(task)
        # return '' # 返回一个task id

    def pull_task(self, agent_id): # 客户拉取任务
        # task_id, script, timeout = self.store.get_task_by_agentid(agent_id)
        return self.store.get_task_by_agentid(agent_id)

    def result(self, msg:dict):
        self.store.result(msg)
        return 'ack result'

    def agents(self):
        return self.store.get_agents()