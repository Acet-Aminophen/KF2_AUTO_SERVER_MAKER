02_Config
=============

This document describes the files in the Config directory to run the KF2 ASM.

1. config.cfg, It has the following structure.
```
DISCORD_SERVER_ID = 
DISCORD_REQUEST_CHANNEL_ID = 
BOT_TOKEN = 
BOT_ID = 
DEV_IDS = []

GCE_ID = 
GCE_PW = /kf2_asm_config/key
GCE_PR = 
# The KF2 ASM recognizes the two below in real time.
SNAPSHOT_NAME = 
OS_IMAGE_NAME = 

SERVER_EXPIRE_TERM_SEC=10800
SERVER_REQUEST_DURATION_SEC=60
REFRESH_SEC=60
SERVER_BLOCK_PERSONAL_REQUEST_SEC=21600
WARNING_SERVER_EXPIRED_SEC=3600
SERVER_ADDITIONAL_TIME_SEC=3600

PROJECT_ABSOLUTE_PATH=/kf2_asm/
CONF_FILE_SERVER_IP=
CONF_FILE_SERVER_PORT=
CONF_FILE_SERVER_USER=
CONF_FILE_SERVER_PWD=
CONF_FILE_PATH_DEFAULT_GAME=game_config/DefaultGame.ini
CONF_DIRECTORY_PATH_TEMP_DEFAULT_GAME=game_config/temp/
```

2. key, The GCP project key, and it has the following structure. You can get more infos in [here.](https://libcloud.readthedocs.io/en/stable/compute/drivers/gce.html)
```
{
  "type": "",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": ""
}
```