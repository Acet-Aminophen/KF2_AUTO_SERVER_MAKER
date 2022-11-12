04_Snapshot
=============

This document describes changing the GCP Snapshot when the KF2 server is updated.

1. Create an instance of the following specifications with an additional 30GB disk.
```
e2-medium
Ubuntu 20.04
asia-northeast3(서울)
10GB
```

2. Create a connection using SSH, and install Steam CMD in the following procedure.<sup>[[1]](#footnote_1)</sup>

```
# You can copy and paste.
sudo apt update
sudo add-apt-repository multiverse
sudo apt install software-properties-common
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install lib32gcc-s1 steamcmd
```

3. Format and mount an additional disk.<sup>[[2]](#footnote_2)</sup>
```
# Check the disk
sudo lsblk
# Formatting
sudo mkfs.ext4 -m 0 -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/sdb
```
```
# Mounting
sudo mkdir -p /home/steam/server
sudo mount -o discard,defaults /dev/sdb /home/steam/server
sudo chmod a+w /home/steam/server
```

4. Install a server using Steam CMD.
```
steamcmd
force_install_dir /home/steam/server
login anonymous
app_update 232130 validate
quit
```

5. Modify the following files.
```
# Enable WebAdmin
# /home/steam/server/KFGame/Config/DefaultWeb.ini
# [IpDrv.WebServer]
bEnabled=true
```
```
# Disable Kidnapping
# /home/steam/server/KFGame/Config/DefaultEngine.ini
# [Engine.GameEngine]
bUsedForTakeover=FALSE
```

6. Download '/home/steam/server/KFGame/Config/DefaultGame.ini' file.<sup>[[3]](#footnote_3)</sup>

7. Save the disk as a snapshot.




<a name="footnote_1">[1]</a>: Source : https://wiki.killingfloor2.com/index.php?title=Dedicated_Server_(Killing_Floor_2), https://developer.valvesoftware.com/wiki/SteamCMD#Downloading_SteamCMD

<a name="footnote_2">[2] </a>: Source : https://cloud.google.com/compute/docs/disks/add-persistent-disk?hl=ko

<a name="footnote_3">[3] </a>: It will be used when KF2 ASM makes the server name and password.
