from .connectmanage import ConnectManage
from utils import get_logger
logger = get_logger(__name__, 'agent.log')

class Agent:
    def __init__(self):
        self.cm = ConnectManage()

    def start(self):
        logger.info('agent up')
        self.cm.start() # 阻塞中

    def shutdown(self):
        # 开一个线程，接收用户的停止。也可以按现在的方案
        self.cm.shutdown()