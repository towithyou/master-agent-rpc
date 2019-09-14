import uuid
from .agent import Agent
from .task import Task
from common.state import *
from utils import get_logger

logger = get_logger(__name__, 'master.log')

class Storage:

    '''负责agents, tasks 的存储， 必要时实现持久化'''

    def __init__(self):
        self.agents = {} # 注册的agents
        self.tasks = {} # 任务的字典


    def reg(self, id, hostname, ip):
        if id not in self.agents.keys():
            self.agents[id] = Agent(id, hostname, ip)
        else:
            agent = self.agents[id]
            agent.id = id
            agent.hosname = hostname
            agent.ip = ip


    def heartbeat(self, id, hostname, ip): # id, timestamp
        if id not in self.agents.keys():
            self.agents[id] = Agent(id, hostname, ip)
        else:
            agent = self.agents[id]
            agent.id = id
            agent.hosname = hostname
            agent.ip = ip
            # agent.lastupdatetime = ts # 这里频繁跟新，一定要用redis, 设定过期时间，
            # 如果 redis 清除了这个key 说明agent 已经挂了，没有发心跳了


    def add_task(self, task:dict):
        id = uuid.uuid4().hex # 这里用服务端的id， 客户端不能传递， 注意base64 编码
        t = Task(id, **task)
        # t.targets = ['agent_id1', 'agent_id2'] 关联哪个agent来处理
        t.targets = { agent_id:self.agents[agent_id] for agent_id in t.targets}
        # 越来越大会 后期肯定要交给redis来做
        # 加入任务列表
        self.tasks[t.id] = t
        return t.id


    def iter_tasks(self, states={WAITING, RUNNING}):
        # for task in self.tasks.values():
        #     if task.state in {WAITING, RUNNING}:
        #         yield task
        yield from (task for task in self.tasks.values() if task.state in states)


    def get_task_by_agentid(self, agent_id):
        for task in self.iter_tasks():
            if agent_id in task.targets.keys(): # 此agent是可以执行这个任务的
                agent = self.agents[agent_id]

                if task.id not in agent.outputs: # 判断表示没有领取过
                    agent.outputs[task.id] = None # 第一次拿任务，做个标记。表示领过任务了 真实生产中查询数据库，redis
                    # 可以加判断，判断当前任务的状态时候空闲
                    task.state = RUNNING # 改task 状态，表示 要running 了
                    agent.state = RUNNING # 改agent 状态，表示agent 要工作了
                # else:
                #     pass # 任务已经领取过了，什么都不需要做了
                    return task.id, task.script, task.timeout

    def result(self, msg:dict):
        agent_id = msg['id']
        agent = self.agents[agent_id]

        agent.outputs[msg['task_id']] = {
            'code': msg['code'],
            'output': msg['output']
        }

        agent.state = WAITING

    def get_agents(self):
        return {agent_id: [self.agents[agent_id].hostname] for agent_id in self.agents.keys()}


