from kf2_server import Kf2Server
import time

STR_LOG_SPLITTER = "--------------------------------------------------------------"
STR_LOG_PID = "PID : "
STR_LOG_BOOTING = "BOOTING..."
STR_LOG_ANNOUNCE_BOT_ONLINE = "KF2 ASM BOT ONLINE"
STR_LOG_REQUESTED_SERVER_STARTED = "SERVER STARTED : "
STR_LOG_DESTROY_SERVER = "DESTROYED SERVER'S UUID : "
STR_SYS_SERVER_NAME_STARTS_WITH = "KF2ASM | "
STR_SYS_SERVER_REQUEST_FLAG = "서버요청"
STR_SYS_SERVER_REQUEST_ADDITIONAL_TIME_FLAG = "연장요청"
STR_ANNOUNCE_REQUESTED_SERVER_TIMEOUT = "요청하셨던 서버가 유효 시간이 지나 종료되었습니다."
STR_ANNOUNCE_REQUEST_REJECTED_REASON_SERVER_CREATING = "서버 생성 불허.\n현재 이전 요청자 분의 서버를 생성 중입니다."
STR_ANNOUNCE_REQUEST_REJECTED_REASON_PERSONAL_TIME_TERM = "서버 생성 불허.\n최근 서버를 신청한지 6시간 이내입니다."
STR_ANNOUNCE_PREPARING_SERVER = "서버 생성 허가 완료.\n서버 생성 수립 중...\n수립이 완료되면 DM을 보내드리며 이 과정은 5분 정도 걸립니다."
STR_ANNOUNCE_WARNING_SERVER_EXPIRED_SOON = "서버 만료까지 1시간 남았습니다.\n'연장요청' 입력 시 1시간이 추가됩니다."
STR_ANNOUNCE_ADDITIONAL_TIME_ADDED = "연장 완료."
STR_ANNOUNCE_WARNING_NO_SERVER = "현재 활성화된 서버가 없습니다."
STR_ANNOUNCE_WARNING_NOT_POSSIBLE_TIME = "시간 연장은 만료 1시간 전부터 가능합니다."


def get_str_announce_requested_server_starts(kf2_server: Kf2Server):
    return "서버 초기화 완료.\n서버 부팅 시작됨.\n대략 3분 후 서버 브라우저에서 아래와 같은 사항으로 확인 가능합니다.\n\n서버 이름 : " + STR_SYS_SERVER_NAME_STARTS_WITH + kf2_server.uid + "\n서버 비밀번호 : " + kf2_server.pwd + "\n서버 관리 웹페이지 : http://" + kf2_server.ip + ":8080/" + "\n서버 관리 웹페이지 ID : admin\n서버 관리 웹페이지 PW : " + kf2_server.pwd

def get_str_announce_request_rejected_reason_server_just_created(latest_created_time: int, server_request_duration_sec: int):
    remained_time = latest_created_time + server_request_duration_sec - int(time.time())
    return "서버 생성 불허.\n이전 요청에 따라 서버를 생성한 지 얼마 되지 않았습니다.\n" + str(remained_time) + "초 이후 다시 요청해주세요."
