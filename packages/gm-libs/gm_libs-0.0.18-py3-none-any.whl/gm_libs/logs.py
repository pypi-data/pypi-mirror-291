# coding=utf-8
from __future__ import print_function, absolute_import
from datetime import datetime
import random
import os
from shutil import copyfile

from gm.api import *

_gm_libs_logs = {
    "dir_path": "",
    "snapshot": "",
}


# 获取日志地址
def l_get_log_path():
    global _gm_libs_logs
    strategy_dir = os.path.basename(os.path.normpath(os.getcwd()))

    if _gm_libs_logs["dir_path"] == "":
        parent_path = r"C:\Users\Public\gm_libs"
        strategy_path = r"C:\Users\Public\gm_libs\%s" % strategy_dir
        _gm_libs_logs["dir_path"] = r"{}\{}\{}".format(parent_path, strategy_dir,
            datetime.today().strftime('%Y-%m-%d %H.%M.%S ') + "%s" % random.randint(1000000, 9999999)
        )
        if not os.path.exists(parent_path):
            os.mkdir(parent_path)
        if not os.path.exists(strategy_path):
            os.mkdir(strategy_path)
        if not os.path.exists(_gm_libs_logs["dir_path"]):
            os.mkdir(_gm_libs_logs["dir_path"])

    return _gm_libs_logs["dir_path"]


# 日志输出且保存
def log_all(level: str, info: str, source: str = "common"):
    log(level=level, msg=info, source=source)
    text = "【{}】 {}".format(level, info)
    print(text)
    append(text, source)


# 日志不输出仅保存
def log_save(level: str, info: str, source: str = "common"):
    log(level=level, msg=info, source=source)
    text = "【{}】 {}".format(level, info)
    append(text, source)


# 复制文件到日志文件夹
def l_copy_file_to_log(filepath: str, filename: str):
    copyfile(filepath, l_get_log_path() + "\\" + filename)


# 追加信息到日志文件
def append(text: str, source: str = ""):
    global _gm_libs_logs
    all_path = l_get_log_path()

    if source not in _gm_libs_logs:
        _gm_libs_logs[source] = True
        log_file = open(r"{}\{}.log".format(all_path, source), "w+", encoding="utf-8")
    else:
        log_file = open(r"{}\{}.log".format(all_path, source), "a", encoding="utf-8")

    log_file.writelines("{}\n".format(text))
    log_file.close()
