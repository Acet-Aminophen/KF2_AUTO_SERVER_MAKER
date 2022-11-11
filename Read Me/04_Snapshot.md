02_Snapshot
=============

본 문서는 KF2 서버가 업데이트되었을 때 GCP Snapshot을 바꾸는 방법을 서술한다.  

1. 아래와 같은 사양의 인스턴스를 만들되, 30GB의 추가 디스크를 생성한다.  
```
e2-medium
Ubuntu 20.04
asia-northeast3(서울)
10GB
```

2. SSH로 접근 후 다음과 같은 절차로 Steam CMD를 설치한다.<sup>[[1]](#footnote_1)</sup>

```
# 전체 복사 붙여넣기 가능
sudo apt update
sudo add-apt-repository multiverse
sudo apt install software-properties-common
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install lib32gcc-s1 steamcmd
```

3. 추가 디스크를 초기화 및 마운트한다.<sup>[[2]](#footnote_2)</sup>
```
# 디스크 확인
sudo lsblk
# 초기화
sudo mkfs.ext4 -m 0 -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/sdb
```
```
# 마운트
sudo mkdir -p /home/steam/server
sudo mount -o discard,defaults /dev/sdb /home/steam/server
sudo chmod a+w /home/steam/server
```

4. Steam CMD로 서버를 설치한다.
```
steamcmd
force_install_dir /home/steam/server
login anonymous
app_update 232130 validate
quit
```

5. 다음의 파일을 지시와 같이 수정한다.
```
# 웹 어드민 활성화
# /home/steam/server/KFGame/Config/DefaultWeb.ini
# [IpDrv.WebServer]
bEnabled=true
```
```
# 서버 강탈 비활성화
# /home/steam/server/KFGame/Config/DefaultEngine.ini
# [Engine.GameEngine]
bUsedForTakeover=FALSE
```

6. '/home/steam/server/KFGame/Config/DefaultGame.ini' 파일을 다운로드한다.<sup>[[3]](#footnote_3)</sup>

7. 디스크를 스냅샷으로 저장한다.




<a name="footnote_1">[1]</a>: 출처 : https://wiki.killingfloor2.com/index.php?title=Dedicated_Server_(Killing_Floor_2), https://developer.valvesoftware.com/wiki/SteamCMD#Downloading_SteamCMD

<a name="footnote_2">[2] </a>: 출처 : https://cloud.google.com/compute/docs/disks/add-persistent-disk?hl=ko

<a name="footnote_3">[3] </a>: KF2 ASM에서 이름, 비밀번호를 만들 때 사용