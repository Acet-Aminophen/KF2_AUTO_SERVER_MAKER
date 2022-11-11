03_Docker
=============

본 문서는 프로그램 실행의 기반이 되는 Docker 환경에 대하여 서술한다.

1. Dockerfile은 다음과 같이 설계되며 원본 이미지는 각주를 참고한다.<sup>[[1]](#footnote_1)</sup>
```
# VERSION : 1
# docker build --build-arg USERID=userid -t kf2server:r1 .

FROM ubu:r9

ARG USERID

RUN cat /password | sudo -S pip3 install apache-libcloud==3.6.1
RUN cat /password | sudo -S pip3 install discord==2.0.0
RUN cat /password | sudo -S pip3 install cryptography==38.0.3
RUN cat /password | sudo -S printf "cat /password | sudo -S service ssh start\nexport LC_ALL=ko_KR.UTF-8\n\n\necho \"SUCCESSFULLY STARTED\"\n\ncat /password | sudo -S rm -rf /kf2_asm\ncat /password | sudo -S git clone https://github.com/Acet-Aminophen/KF2_AUTO_SERVER_MAKER.git /kf2_asm\ncd /kf2_asm\ncat /password | sudo -S python3 /kf2_asm/main.py\n" > starter.sh
```

2. 만들어진 이미지를 토대로 다음의 예시를 활용하여 실행한다.
```
# config 폴더의 경로는 무조건 컨테이너 내부 /kf2_asm_config로 맞추어져야 한다.
docker run -d --name kf2server -p 8460:22 -v /home/changeme/kf2_asm_config:/kf2_asm_config kf2server:r1
```

<a name="footnote_1">[1]</a>: https://github.com/Acet-Aminophen/Dockerfiles/blob/main/ubu.txt