import os
import os.path
import time
import datetime
import uuid


def get_uuid():
    return str(uuid.uuid4())


def get_now():
    date_now = str(datetime.datetime.now()).split(".")[0]
    time_now = str(time.time())
    return str(date_now + "," + time_now)


def get_time():
    time_now = str(time.time())
    return time_now


def get_config(filepath: str, key: str, splitChar="=", comments=None):
    if comments is None:
        comments = ["#", "//"]
    lines = load_str(filepath)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        is_comment = False
        for i in comments:
            if line.startswith(i):
                is_comment = True
        if is_comment:
            continue
        tkey, value = line.split(splitChar)
        tkey = tkey.strip()
        value = value.strip()
        if key == tkey:
            if value.startswith("[") and value.endswith("]"):
                value = value[1:-1]
                values = value.split(",")
                for index, val in enumerate(values):
                    val = val.strip()
                    values[index] = val
                return values
            else:
                return value


def make_directory(location: str):
    os.makedirs(location)


def load_str(location: str, is_list=True, encoding="utf8", new_line="\n"):
    str_list = []
    file = open(location, 'r', newline=new_line, encoding=encoding)
    str_list = file.read().splitlines()
    if is_list:
        return str_list
    else:
        sender = ""
        for ele in str_list:
            sender += ele + new_line
        return sender
