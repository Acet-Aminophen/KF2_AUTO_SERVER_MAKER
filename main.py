from shutil import copyfile
from BasicPackage.basic_func import *
import gce_connector
import discord
import logging
import logging.config
import random
import threading
import os
from typing import List, Dict
from strings import *

logging.config.fileConfig("logging.cfg")
config_path = "/kf2_asm_config/config.cfg"

CONF_FILE_SERVER_IP = get_config(config_path, "CONF_FILE_SERVER_IP")
CONF_FILE_SERVER_PORT = get_config(config_path, "CONF_FILE_SERVER_PORT")
CONF_FILE_SERVER_USER = get_config(config_path, "CONF_FILE_SERVER_USER")
CONF_FILE_SERVER_PWD = get_config(config_path, "CONF_FILE_SERVER_PWD")
CONF_FILE_PATH_DEFAULT_GAME = get_config(config_path, "CONF_FILE_PATH_DEFAULT_GAME")
CONF_DIRECTORY_PATH_TEMP_DEFAULT_GAME = get_config(config_path, "CONF_DIRECTORY_PATH_TEMP_DEFAULT_GAME")
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
SERVER_EXPIRE_TERM_SEC = int(get_config(config_path, "SERVER_EXPIRE_TERM_SEC"))
SERVER_REQUEST_DURATION_SEC = int(get_config(config_path, "SERVER_REQUEST_DURATION_SEC"))
REFRESH_SEC = int(get_config(config_path, "REFRESH_SEC"))
SERVER_BLOCK_PERSONAL_REQUEST_SEC = int(get_config(config_path, "SERVER_BLOCK_PERSONAL_REQUEST_SEC"))

gce_driver = gce_connector.get_driver(GCE_ID, GCE_PW, GCE_PR)
intents = discord.Intents.all()
client = discord.Client(intents=intents)

user_dic = {}
flag_server_creating: bool = False
server_list: List[Kf2Server] = []
server_dic: Dict[str, Kf2Server] = {}
latest_server_created: int = 0

logging.info(STR_LOG_SPLITTER)
logging.info(STR_LOG_BOOTING)
logging.info(STR_LOG_PID + str(os.getpid()))


def get_hour_from_sec(sec: int):
    return round(sec / 3600, 1)


def alert(content: str):
    global client
    global DEV_ID_LIST
    for id_is in DEV_ID_LIST:
        client.loop.create_task(send_dm(id_is, content))


def chk_status():
    global server_list
    global gce_driver
    global latest_server_created
    global client
    global SERVER_EXPIRE_TERM_SEC
    global REFRESH_SEC

    locker = threading.Lock()
    locker.acquire()

    # 복사본으로 진행하여 remove를 하게함
    for server in server_list[:]:
        created_time: int = server.created_time
        expired_term_sec: int = server.expired_term_sec
        if created_time + expired_term_sec < int(time.time()):
            logging.info(STR_LOG_DESTROY_SERVER + server.uuid)
            gce_driver.destroy_node(server.gcp_node)
            client.loop.create_task(send_dm(server.author_discord_id, STR_ANNOUNCE_REQUESTED_SERVER_TIMEOUT))
            server_list.remove(server)
            del server_dic[server.uid]

    locker.release()
    threading.Timer(REFRESH_SEC, chk_status).start()


def get_config_path(uuid: str):
    global CONF_DIRECTORY_PATH_TEMP_DEFAULT_GAME

    temp_conf_location = CONF_DIRECTORY_PATH_TEMP_DEFAULT_GAME + uuid + "/"
    temp_conf_location_default_game = temp_conf_location + "DefaultGame.ini"
    return temp_conf_location, temp_conf_location_default_game


def apply_game_config(uid: str, pwd: str, uuid: str) -> str:
    global CONF_FILE_PATH_DEFAULT_GAME

    temp_conf_location, temp_conf_location_default_game = get_config_path(
        uuid)
    make_directory(temp_conf_location)
    copyfile(CONF_FILE_PATH_DEFAULT_GAME, temp_conf_location_default_game)
    server_name = STR_SYS_SERVER_NAME_STARTS_WITH + uid

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
    return temp_conf_location_default_game


def get_init_sequence(temp_conf_location_default_game: str):
    global CONF_FILE_SERVER_IP
    global CONF_FILE_SERVER_PORT
    global CONF_FILE_SERVER_USER
    global CONF_FILE_SERVER_PWD
    global PROJECT_ABSOLUTE_PATH

    order_list = ["#! /bin/bash", "sudo mkdir /orgserver", "sudo mount -o discard,defaults /dev/sdb /orgserver", "sudo apt update", "sudo apt install sshpass", "sudo sshpass -p '" + CONF_FILE_SERVER_PWD + "' scp -P " + CONF_FILE_SERVER_PORT + " -o StrictHostKeyChecking=no " + CONF_FILE_SERVER_USER + "@" + CONF_FILE_SERVER_IP + ":" + PROJECT_ABSOLUTE_PATH + temp_conf_location_default_game + " /orgserver/KFGame/Config/DefaultGame.ini", "cd /", "./orgserver/Binaries/Win64/KFGameSteamServer.bin.x86_64 kf-bioticslab"]

    start_up_str = ""
    for order in order_list:
        start_up_str += order + "\n"

    return start_up_str


def start_gcp_server(message_author_id: str) -> Kf2Server:
    global gce_driver
    global config_path
    global SERVER_EXPIRE_TERM_SEC

    server_uid = "r" + str(random.randrange(1, 10000))
    server_pwd = str(random.randrange(1, 10000))
    # for saving a server conf file
    server_uuid = get_uuid()

    temp_conf_location_default_game = apply_game_config(server_uid, server_pwd, server_uuid)
    metadata = {
        'items': [
            {
                'key': 'startup-script',
                'value': get_init_sequence(temp_conf_location_default_game)
            }
        ]
    }
    volume_name = "vol-" + server_uid
    node_name = "nod-" + server_uid
    vol = gce_driver.create_volume(size=30, name=volume_name, location="asia-northeast3-a",
                                   snapshot=get_config(config_path, "SNAPSHOT_NAME"))
    node = gce_driver.create_node(name=node_name, size="e2-medium", image=get_config(config_path, "OS_IMAGE_NAME"), location="asia-northeast3-a",
                                  ex_disk_size=10, ex_metadata=metadata)
    gce_driver.attach_volume(node, vol, ex_mode="READ_WRITE", ex_auto_delete=True)

    kf2_server = Kf2Server(server_uid, server_pwd, server_uuid, SERVER_EXPIRE_TERM_SEC, message_author_id, node)
    logging.info(STR_LOG_REQUESTED_SERVER_STARTED + str(kf2_server))

    return kf2_server


@client.event
async def on_ready():
    logging.info(STR_LOG_ANNOUNCE_BOT_ONLINE)
    alert(STR_LOG_ANNOUNCE_BOT_ONLINE)


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
    except Exception as e:
        print(str(e))
    return


async def send_channel_message(id_is, content: str):
    try:
        location_to_send = client.get_channel(int(id_is))
        await location_to_send.send(content)
    except Exception as e:
        print(str(e))
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
    global latest_server_created
    global flag_server_creating

    locker = threading.Lock()
    locker.acquire()

    flag_server_creating = True

    kf2_server = start_gcp_server(str(message.author.id))
    server_list.append(kf2_server)
    server_dic[kf2_server.uid] = kf2_server
    latest_server_created = kf2_server.created_time

    flag_server_creating = False

    msg = get_str_announce_requested_server_starts(kf2_server)
    alert(msg)
    client.loop.create_task(send_dm(message.author.id, msg))

    locker.release()


async def route_server_request(message):
    global flag_server_creating
    global latest_server_created
    global user_dic
    global SERVER_BLOCK_PERSONAL_REQUEST_SEC
    global SERVER_REQUEST_DURATION_SEC

    author: int = message.author.id
    user_requested_time = user_dic.get(str(author), 0)

    if flag_server_creating:
        await send_channel_message(message.channel.id, STR_ANNOUNCE_REQUEST_REJECTED_REASON_SERVER_CREATING)
        return

    if user_requested_time + SERVER_BLOCK_PERSONAL_REQUEST_SEC > int(time.time()):
        await send_channel_message(message.channel.id, STR_ANNOUNCE_REQUEST_REJECTED_REASON_PERSONAL_TIME_TERM)
        return

    user_dic[str(author)] = int(time.time())
    await send_channel_message(message.channel.id, STR_ANNOUNCE_PREPARING_SERVER)
    threading.Thread(target=start_server, args=(message,)).start()


async def route_message(message):
    # 채널 메세지 아니면 종료
    if not is_on_the_channel(message):
        return
    content: str = str(message.content)
    if content == STR_SYS_SERVER_REQUEST_FLAG:
        await route_server_request(message)
    else:
        return


threading.Timer(0, chk_status).start()
client.run(BOT_TOKEN)
