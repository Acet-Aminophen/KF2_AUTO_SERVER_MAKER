02_Config
=============

본 문서는 프로그램의 실행에 필요한 Config 폴더 속 파일들에 대해 서술한다.

1. config.cfg, 다음과 같은 구조를 가진다.
```
DISCORD_SERVER_ID = 
DISCORD_REQUEST_CHANNEL_ID = 
BOT_TOKEN = 
BOT_ID = 
DEV_IDS = []

GCE_ID = 
GCE_PW = /kf2_asm_config/key
GCE_PR = 
SNAPSHOT_NAME = 
OS_IMAGE_NAME = 

SERVER_EXPIRE_TERM_SEC=10800
SERVER_REQUEST_DURATION_SEC=600
REFRESH_SEC=60
SERVER_BLOCK_PERSONAL_REQUEST_SEC=21600

PROJECT_ABSOLUTE_PATH=/kf2_asm/
CONF_FILE_SERVER_IP=
CONF_FILE_SERVER_PORT=
CONF_FILE_SERVER_USER=
CONF_FILE_SERVER_PWD=
CONF_FILE_PATH_DEFAULT_GAME=game_config/DefaultGame.ini
CONF_DIRECTORY_PATH_TEMP_DEFAULT_GAME=game_config/temp/
```

2. key, GCP 프로젝트 키 문서로 다음과 같은 구조를 가진다.
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