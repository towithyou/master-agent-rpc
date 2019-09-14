import os
import uuid
import socket
import datetime
import netifaces
import ipaddress
from config.conf import AGENT_DIR

# master 和 agent 通信之间的消息

class Message:
    def __init__(self, uidfile:str=os.path.join(AGENT_DIR, 'agt')): # 把每个agent的uuid 存放在服务器上的一个文件中
        self.id = ''
        # 判断文件是否存在
        if os.path.exists(uidfile):
            with open(uidfile, mode='r', encoding='utf-8') as f:
                id = f.readline().strip()
                if len(id) == 32:
                    self.id = id

        if not self.id: # 如果没有获得id 则说明第一次，需要写入
            with open(uidfile, mode='w', encoding='utf-8') as f:
                self.id = uuid.uuid4().hex
                f.write(self.id)

    def _get_addrs(self):
        ips = []
        for iface in netifaces.interfaces():
            x = netifaces.ifaddresses(iface)
            ipv4s = x.get(2, [])
            if ipv4s:
                for ipv4 in ipv4s:
                    ip = ipaddress.ip_address(ipv4.get('addr'))

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
                    ips.append(str(ip))
        return ips

    def reg(self):
        return {
            'id': self.id,
            'hostname': socket.gethostname(),
            'timestamp': datetime.datetime.now().timestamp(),
            'ips': self._get_addrs()
        }

    def heartbeat(self):
        return {
            'msg': 'heartbeat',
            'id': self.id,
            'hostname': socket.gethostname(),
            'timestamp': datetime.datetime.now().timestamp(),
            'ips': self._get_addrs()
        }

    def result(self, task_id, code, text):
        return {
            'id': self.id,
            'task_id': task_id,
            'code': code,
            'output': text
        }


if __name__ == '__main__':
    mes = Message()
    print (mes.reg())