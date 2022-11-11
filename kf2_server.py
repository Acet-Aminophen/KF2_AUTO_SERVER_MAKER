import time
from libcloud.compute.base import Node


class Kf2Server:
    def __init__(self, uid: str, pwd: str, uuid: str, expired_term_sec: int, author_discord_id: str, gcp_node: Node):
        self.uid = uid
        self.pwd = pwd
        self.uuid = uuid
        self.expired_term_sec = expired_term_sec
        self.author_discord_id = author_discord_id
        self.gcp_node = gcp_node
        self.created_time = int(time.time())
        self.ip = gcp_node.public_ips[0]

    def __str__(self):
        # will be changed to DB
        return "UID : " + self.uid + ", PWD : " + self.pwd + ", UUID : " + self.uuid + ", EXPIRED_TIME_SEC : " + str(self.expired_term_sec) + ", AUTHOR'S DISCORD ID : " + self.author_discord_id + ", CREATED_TIME : " + str(self.created_time) + ", IP : " + self.ip
