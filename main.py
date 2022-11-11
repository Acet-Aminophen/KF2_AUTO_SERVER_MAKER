from shutil import copyfile
from BasicPackage.basic_func import *
import gce_connector
import discord
import logging
import logging.config
import time
import random
import threading
import os
from strings import *

logging.config.fileConfig("logging.cfg")
config_path = "config/config.cfg"

CONF_FILE_SERVER_IP = get_config(config_path, "CONF_FILE_SERVER_IP")
CONF_FILE_SERVER_PORT = get_config(config_path, "CONF_FILE_SERVER_PORT")
CONF_FILE_SERVER_USER = get_config(config_path, "CONF_FILE_SERVER_USER")
CONF_FILE_SERVER_PWD = get_config(config_path, "CONF_FILE_SERVER_PWD")
CONF_FILE_PATH_DEFAULT_GAME = get_config(config_path, "CONF_FILE_PATH_DEFAULT_GAME")
PROJECT_ABSOLUTE_PATH = get_config(config_path, "PROJECT_ABSOLUTE_PATH")

DISCORD_SERVER_ID: int = int(get_config(config_path, "DISCORD_SERVER_ID"))
DISCORD_REQUEST_CHANNEL_ID = int(get_config(config_path, "DISCORD_REQUEST_CHANNEL_ID"))
BOT_TOKEN = get_config(config_path, "BOT_TOKEN")
BOT_ID = int(get_config(config_path, "BOT_ID"))
TMP_DEV_IDS = get_config(config_path, "DEV_IDS")
DEV_ID_LIST = []
for i in TMP_DEV_IDS:
    DEV_ID_LIST.append(int(i))
GCE_ID = get_config(config_path, "GCE_ID")
GCE_PW = get_config(config_path, "GCE_PW")
GCE_PR = get_config(config_path, "GCE_PR")
SERVER_EXPIRE_SEC = int(get_config(config_path, "SERVER_EXPIRE_SEC"))
SERVER_REQUEST_DURATION_SEC = int(get_config(config_path, "SERVER_REQUEST_DURATION_SEC"))
REFRESH_SEC = int(get_config(config_path, "REFRESH_SEC"))
SERVER_BLOCK_REQUEST_SEC = int(get_config(config_path, "SERVER_BLOCK_REQUEST_SEC"))

gce_driver = gce_connector.get_driver(GCE_ID, GCE_PW, GCE_PR)
intents = discord.Intents.all()
client = discord.Client(intents=intents)

user_dic = {}
flag_server_creating: bool = False
server_list: list = []
latest_server_created: int = int(time.time()) - 10800

logging.info(STR_SPLITTER)
logging.info(STR_BOOTING)
logging.info(STR_PID + str(os.getpid()))


def get_init_sequence():
    global CONF_FILE_SERVER_IP
    global CONF_FILE_SERVER_PORT
    global CONF_FILE_SERVER_USER
    global CONF_FILE_SERVER_PWD
    global PROJECT_ABSOLUTE_PATH

    order_list = ["#! /bin/bash", "sudo mkdir /orgserver", "sudo mount -o discard,defaults /dev/sdb /orgserver",
                  "sudo apt update", "sudo apt install sshpass",
                  "sudo sshpass -p '" + CONF_FILE_SERVER_PWD + "' scp -P " + CONF_FILE_SERVER_PORT + " -o StrictHostKeyChecking=no " + CONF_FILE_SERVER_USER + "@" + CONF_FILE_SERVER_IP + ":" + PROJECT_ABSOLUTE_PATH + CONF_FILE_PATH_DEFAULT_GAME + " /orgserver/KFGame/Config/DefaultGame.ini",
                  "cd /", "./orgserver/Binaries/Win64/KFGameSteamServer.bin.x86_64 kf-bioticslab"]

    start_up_str = ""
    for order in order_list:
        start_up_str += order + "\n"

    return start_up_str


def get_hour_from_sec(sec: int):
    return round(sec / 3600, 1)


def alert(content: str):
    global client
    global DEV_ID_LIST
    for id_is in DEV_ID_LIST:
        client.loop.create_task(send_dm(id, content))


def chk_status():
    locker = threading.Lock()
    locker.acquire()
    global server_list
    global gce_driver
    global latest_server_created
    global client
    global SERVER_EXPIRE_SEC
    global REFRESH_SEC
    logging.info("Server List ↓")
    logging.info(server_list)
    logging.info("Latest Created ↓")
    logging.info(latest_server_created)
    # 복사본으로 진행하여 remove를 하게함
    for i in server_list[:]:
        created_time: int = i.get("created_time")
        expired_time: int = i.get("expired_time")
        if created_time + expired_time < int(time.time()):
            logging.info("Destroy node ↓")
            logging.info(i)
            gce_driver.destroy_node(i.get("node"))
            message_from = i.get("message_from")
            client.loop.create_task(send_dm(message_from, STR_ANNOUNCE_REQUESTED_SERVER_TIMEOUT))
            server_list.remove(i)
    locker.release()
    threading.Timer(REFRESH_SEC, chk_status).start()


def get_config_path(uuid: str):
    temp_conf_location = "game_config/temp/" + uuid + "/"
    temp_conf_location_default_game = temp_conf_location + "DefaultGame.ini"
    return temp_conf_location, temp_conf_location_default_game


def chg_game_config(name: str, pwd: str, uuid: str):
    global CONF_FILE_PATH_DEFAULT_GAME

    temp_conf_location, temp_conf_location_default_game = get_config_path(
        uuid)
    make_directory(temp_conf_location)
    copyfile(CONF_FILE_PATH_DEFAULT_GAME, temp_conf_location_default_game)
    server_name = STR_SERVER_NAME_STARTS_WITH + name

    str_org = ""
    reader = open(temp_conf_location_default_game, 'r', encoding="utf-8")
    while True:
        line = reader.readline()
        if not line:
            break
        if "ServerName=" in line:
            line = "ServerName=" + server_name + "\n"
        if "AdminPassword=" in line:
            if pwd != "":
                line = "AdminPassword=" + pwd + "\n"
            else:
                line = "AdminPassword=" + "\n"
        if "GamePassword=" in line:
            if pwd != "":
                line = "GamePassword=" + pwd + "\n"
            else:
                line = "GamePassword=" + "\n"
        str_org += line
    reader.close()
    writer = open(temp_conf_location_default_game, 'w', encoding="utf-8")
    writer.write(str_org)
    writer.close()
    return server_name


def start_gcp_server(name: str, pwd: str):
    global gce_driver
    global SERVER_EXPIRE_SEC

    uuid = get_uuid()
    server_name = chg_game_config(name, pwd, uuid)
    metadata = {
        'items': [
            {
                'key': 'startup-script',
                'value': get_init_sequence()
            }
        ]
    }
    volume_name = "vol-" + name
    node_name = "nod-" + name
    vol = gce_driver.create_volume(size=30, name=volume_name, location="asia-northeast3-a",
                                   snapshot="kf2-server-origin-snp-220710")
    node = gce_driver.create_node(name=node_name, size="e2-medium", image="ubuntu-18", location="asia-northeast3-a",
                                  ex_disk_size=10, ex_metadata=metadata)
    gce_driver.attach_volume(node, vol, ex_mode="READ_WRITE", ex_auto_delete=True)
    time_now = int(time.time())
    return {"name": name, "password": pwd, "server_name": server_name, "node_name": node_name,
            "volume_name": volume_name,
            "created_time": time_now, "expired_time": SERVER_EXPIRE_SEC, "ip": node.public_ips[0], "node": node}


@client.event
async def on_ready():
    logging.info(STR_BOT_ONLINE)
    alert(STR_BOT_ONLINE)


@client.event
async def on_message(message):
    logging.info([str(message.created_at), str(message.author.id), str(message.guild.id) if message.guild else "",
                  str(message.channel.id) if message.guild else "", str(message.content) if message.content else ""])
    if not message.content:
        return
    # 내용 없을 경우 종료
    await route_message(message)


async def send_dm(id_is, content: str):
    try:
        location_to_send = client.get_user(int(id_is))
        await location_to_send.send(content)
    except:
        pass
    return


async def send_channel_message(id_is, content: str):
    try:
        location_to_send = client.get_channel(int(id_is))
        await location_to_send.send(content)
    except:
        pass
    return


def is_on_the_channel(message):
    global DISCORD_REQUEST_CHANNEL_ID
    if not message.channel:
        return False
    if message.channel.id == DISCORD_REQUEST_CHANNEL_ID:
        return True
    else:
        return False


def start_server(message):
    locker = threading.Lock()
    locker.acquire()
    global latest_server_created
    global flag_server_creating
    flag_server_creating = True
    server_name = "r" + str(random.randrange(1, 10000))
    server_pwd = str(random.randrange(1, 10000))
    dic = start_gcp_server(server_name, server_pwd)
    dic["message_from"] = message.author.id
    server_list.append(dic)
    latest_server_created = int(time.time())
    flag_server_creating = False
    msg = get_str_announce_requested_server_starts(dic)
    alert(msg)
    client.loop.create_task(send_dm(message.author.id, msg))
    locker.release()


async def route_server_request(message):
    global flag_server_creating
    global latest_server_created
    global user_dic
    global SERVER_BLOCK_REQUEST_SEC
    global SERVER_REQUEST_DURATION_SEC

    author: int = message.author.id
    user_requested_time = user_dic.get(str(author), 0)
    if user_requested_time + SERVER_BLOCK_REQUEST_SEC > int(time.time()):
        await send_channel_message(message.channel.id, STR_ANNOUNCE_REQUEST_REJECTED_REASON_TIME_TERM)
        return

    user_dic[str(author)] = int(time.time())
    await send_channel_message(message.channel.id, STR_ANNOUNCE_PREPARING_SERVER)
    threading.Thread(target=start_server, args=(message,)).start()


async def route_message(message):
    # 채널 메세지 아니면 종료
    if not is_on_the_channel(message):
        return
    content: str = str(message.content)
    if content == STR_SERVER_REQUEST_FLAG:
        await route_server_request(message)
    else:
        return


threading.Timer(0, chk_status).start()
client.run(BOT_TOKEN)
