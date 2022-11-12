03_Docker
=============

This document describes the Docker environment for KF2 ASM

1. The Dockerfile has the following structure. You can find the original image in the footnote.<sup>[[1]](#footnote_1)</sup>
```
# VERSION : 2
# docker build --build-arg USERID=userid -t kf2asm:r2 .

FROM ubu:r9

ARG USERID

RUN cat /password | sudo -S pip3 install apache-libcloud==3.6.1
RUN cat /password | sudo -S pip3 install discord==2.0.0
RUN cat /password | sudo -S pip3 install cryptography==38.0.3
RUN cat /password | sudo -S printf "cat /password | sudo -S service ssh start\nexport LC_ALL=ko_KR.UTF-8\n\n\necho \"SUCCESSFULLY STARTED\"\n\ncat /password | sudo -S rm -rf /kf2_asm\ncat /password | sudo -S git clone https://github.com/Acet-Aminophen/KF2_AUTO_SERVER_MAKER.git /kf2_asm\ncd /kf2_asm\ncat /password | sudo -S python3 -u /kf2_asm/main.py\n" > starter.sh
```

2. Based on the created image, Execute using the following example.
```
# You must set the config directory path's destination as /kf2_asm_config in the container.
docker run -d --name kf2asm -p 8460:22 --restart=always -v /home/changeme/kf2_asm_config:/kf2_asm_config kf2asm:r2
```

<a name="footnote_1">[1]</a>: https://github.com/Acet-Aminophen/Dockerfiles/blob/main/ubu.txt