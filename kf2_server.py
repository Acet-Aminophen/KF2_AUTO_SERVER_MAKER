import time
from libcloud.compute.base import Node

class Kf2Server:
    def __init__(self, uid: str, pwd: str, uuid: str, expired_term_sec: int, gcp_node: Node):
        self.uid = uid
        self.pwd = pwd
        self.uuid = uuid
        self.expired_term_sec = expired_term_sec
        self.gcp_node: gcp_node
        self.created_time = int(time.time())
        self.ip = gcp_node.public_ips[0]
