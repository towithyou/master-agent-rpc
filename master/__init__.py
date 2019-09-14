from .connectmanage import ConnectManage
from config.conf import SERVER_URL
from utils import get_logger
logger = get_logger(__name__, 'master.log')

class Master:

    def __init__(self, url=SERVER_URL):
        self.cm = ConnectManage(url)

    def start(self):
        logger.info('master start...')
        self.cm.start()

    def shutdown(self):
        logger.info('master stop...')
        self.cm.shutdown()

