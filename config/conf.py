import os
import platform

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = os.path.join(BASE_DIR, 'logs')

Platform_system = platform.system()

AGENT_DIR = r'E:/Pycharm_code/webchat'

SERVER_URL = "tcp://127.0.0.1:8080"

INTERVAL = 1




if __name__ == '__main__':
    print(BASE_DIR)
    print(LOG_DIR)
    # from .utils import get_logger
