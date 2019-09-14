import zerorpc
from .message import Message
# from config.conf import SERVER_URL


class ConnectManage:
    def __init__(self, url):
        self.server = zerorpc.Server(Message())
        self.server.bind(url)

    def start(self):
        self.server.run()

    def shutdown(self):
        self.server.close()