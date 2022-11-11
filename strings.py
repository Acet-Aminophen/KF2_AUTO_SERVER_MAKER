STR_SPLITTER = "--------------------------------------------------------------"
STR_PID = "PID : "
STR_BOOTING = "SERVER IS BOOTING..."
STR_BOT_ONLINE = "KF2 SAM BOT ONLINE"
STR_SERVER_NAME_STARTS_WITH = "KF2SAM|"
STR_SERVER_REQUEST_FLAG = "서버요청"
STR_ANNOUNCE_REQUESTED_SERVER_TIMEOUT = "요청하셨던 서버의 유효시간이 지나 종료되었습니다."
STR_ANNOUNCE_REQUEST_REJECTED_REASON_SERVER_CREATING = "서버 생성 불허.\n현재 이전 요청자 분의 서버를 생성 중입니다."
STR_ANNOUNCE_REQUEST_REJECTED_REASON_PERSONAL_TIME_TERM = "서버 생성 불허.\n최근 서버를 신청한지 6시간 이내입니다."
STR_ANNOUNCE_PREPARING_SERVER = "서버 생성 허가 완료.\n서버 생성 수립 중...\n수립이 완료되면 DM을 보내드리며 이 과정은 5분 정도 걸립니다."


def get_str_announce_requested_server_starts(dic: dict):
    return "서버 초기화 완료.\n서버 부팅 시작됨.\n대략 3분 후 서버 브라우저에서 아래와 같은 사항으로 확인 가능합니다.\n\n서버 이름 : " + dic.get(
        "server_name") + "\n서버 비밀번호 : " + dic.get("password") + "\n서버 관리 웹페이지 : http://" + dic.get(
        "ip") + ":8080/" + "\n서버 관리 웹페이지 ID : admin\n서버 관리 웹페이지 PW : " + dic.get("password")
