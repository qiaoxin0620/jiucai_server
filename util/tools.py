# -*- coding:utf-8 -*-
import json
import os
import random
import subprocess
import time
import uuid
# import winreg
import zipfile
from pathlib import Path
from re import search, sub
from shutil import rmtree
from zipfile import ZipFile
import datetime
from base64 import b64encode
import pytz
from config import base_path
from util.logger import log

def get_exe_from_port(port):
    """获取端口号第一条进程的可执行文件路径
    :param port: 端口号
    :return: 可执行文件的绝对路径
    """
    from os import popen

    pid = get_pid_from_port(port)
    if not pid:
        return
    else:
        file_lst = popen(f'wmic process where processid={pid} get executablepath').read().split('\n')
        return file_lst[2].strip() if len(file_lst) > 2 else None


def get_pid_from_port(port):
    """获取端口号第一条进程的pid
    :param port: 端口号
    :return: 进程id
    """
    from platform import system
    if system().lower() != 'windows' or port is None:
        return None

    from os import popen
    from time import perf_counter

    try:  # 避免Anaconda中可能产生的报错
        process = popen(f'netstat -ano |findstr {port}').read().split('\n')[0]

        t = perf_counter()
        while not process and perf_counter() - t < 5:
            process = popen(f'netstat -ano |findstr {port}').read().split('\n')[0]

        return process.split(' ')[-1] or None

    except Exception:
        return None

def kill_process(pid):
    cmd = ["taskkill","-f","-pid",str(pid)]
    subprocess.Popen(cmd,shell=True)

def get_usable_path(path):
    """检查文件或文件夹是否有重名，并返回可以使用的路径
    :param path: 文件或文件夹路径
    :return: 可用的路径，Path对象
    """
    path = Path(path)
    parent = path.parent
    path = parent / make_valid_name(path.name)
    name = path.stem if path.is_file() else path.name
    ext = path.suffix if path.is_file() else ''

    first_time = True

    while path.exists():
        r = search(r'(.*)_(\d+)$', name)

        if not r or (r and first_time):
            src_name, num = name, '1'
        else:
            src_name, num = r.group(1), int(r.group(2)) + 1

        name = f'{src_name}_{num}'
        path = parent / f'{name}{ext}'
        first_time = None

    return path


def make_valid_name(full_name):
    """获取有效的文件名
    :param full_name: 文件名
    :return: 可用的文件名
    """
    # ----------------去除前后空格----------------
    full_name = full_name.strip()

    # ----------------使总长度不大于255个字符（一个汉字是2个字符）----------------
    r = search(r'(.*)(\.[^.]+$)', full_name)  # 拆分文件名和后缀名
    if r:
        name, ext = r.group(1), r.group(2)
        ext_long = len(ext)
    else:
        name, ext = full_name, ''
        ext_long = 0

    while get_long(name) > 255 - ext_long:
        name = name[:-1]

    full_name = f'{name}{ext}'

    # ----------------去除不允许存在的字符----------------
    return sub(r'[<>/\\|:*?\n]', '', full_name)


def get_long(txt):
    """返回字符串中字符个数（一个汉字是2个字符）
    :param txt: 字符串
    :return: 字符个数
    """
    txt_len = len(txt)
    return int((len(txt.encode('utf-8')) - txt_len) / 2 + txt_len)


def port_is_using(ip, port):
    """检查端口是否被占用
    :param ip: 浏览器地址
    :param port: 浏览器端口
    :return: bool
    """
    from socket import socket, AF_INET, SOCK_STREAM
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(.1)
    result = s.connect_ex((ip, int(port)))
    s.close()
    return result == 0


def clean_folder(folder_path, ignore=None):
    """清空一个文件夹，除了ignore里的文件和文件夹
    :param folder_path: 要清空的文件夹路径
    :param ignore: 忽略列表
    :return: None
    """
    ignore = [] if not ignore else ignore
    p = Path(folder_path)

    for f in p.iterdir():
        if f.name not in ignore:
            if f.is_file():
                f.unlink()
            elif f.is_dir():
                rmtree(f, True)

def GetBase64Data(filename):
    with open(filename,"rb") as fr:
        content = fr.read()
    if len(content) > 0:
        base64_body = b64encode(content)
        return base64_body
    else:
        return ""

def WriteFile(filename,data):
    with open(filename,"w",encoding="utf-8") as fw:
        fw.write(data)

def GetRandomPort():
    while True:
        port = random.randint(9300,9500)
        result = port_is_using("127.0.0.1",port)
        if not result:
            return port
        else:
            continue

def unzip(zip_path, to_path):
    """解压下载的chromedriver.zip文件"""
    if not zip_path:
        return

    with ZipFile(zip_path, 'r') as f:
        return [f.extract(f.namelist()[0], path=to_path)]


def get_current_time(strFormat="%Y-%m-%d %H:%M:%S"):
    time_now = datetime.datetime.now()
    current_time = time_now.strftime(strFormat)
    return current_time

def DiffTime(s):
    current_now = datetime.datetime.now()
    if s == "-1" or s == "0":
        age_time = current_now + datetime.timedelta(days=int(s))
    else:
        age_time = current_now + datetime.timedelta(days=int(s) + 1)
    return age_time.strftime("%Y-%m-%d"),current_now.strftime("%Y-%m-%d")

def GenerateTime(s,result):
    start_time = ""
    end_time = ""
    if s == "custom":
        start_time,end_time = result
    elif s == "-1":
        start_time,end_time = DiffTime(s)
        end_time = start_time
    else:
        start_time,end_time = DiffTime(s)
    return start_time,end_time

def getTimeStrAgo(startTimeStr,endTimeStr):
    timeL = []
    startTime = datetime.datetime.strptime(startTimeStr, "%Y-%m-%d")
    endTime = datetime.datetime.strptime(endTimeStr, "%Y-%m-%d")
    days = (endTime - startTime).days + 1
    for i in range(days):
        t = (endTime - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        timeL.append(t)
    return timeL[::-1]


def makeDir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def ReadFileData(filename):
    if os.path.exists(filename):
        with open(filename,"r",encoding="utf-8") as fr:
            data = fr.read()
            return data
    else:
        return -1

def FileExists(path):
    if os.path.exists(path):
        return True
    else:
        return False


def push_png_to_oss(filename):
    """
        推送图片到oss，然后删除本地图片
    :param filename:
    :return:
    """
    return "image:" + filename

'''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

def TimeStrToTimeStamp():
    pass

'''获取文件的大小,结果保留两位小数，单位为MB'''
def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)


'''获取文件的访问时间'''
def get_FileAccessTime(filePath):
    t = os.path.getatime(filePath)
    return TimeStampToTime(t)


'''获取文件的创建时间'''
def get_FileCreateTime(filePath):
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)


'''获取文件的修改时间'''
def get_FileModifyTime(filePath):
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)

'''获取文件的修改时间'''
def get_FileModifyTimeStamp(filePath):
    t = os.path.getmtime(filePath)
    return t



def File2Zip(zip_file_name,file_names):
    """ 将多个文件夹中文件压缩存储为zip
    :param zip_file_name:   /root/Document/test.zip
    :param file_names:      ['/root/user/doc/test.txt', ...]
    :return:
    """
    # 读取写入方式 ZipFile requires mode 'r', 'w', 'x', or 'a'
    # 压缩方式  ZIP_STORED： 存储； ZIP_DEFLATED： 压缩存储
    with zipfile.ZipFile(zip_file_name, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for fn in file_names:
            parent_path, name = os.path.split(fn)
            # zipfile 内置提供的将文件压缩存储在.zip文件中， arcname即zip文件中存入文件的名称
            # 给予的归档名为 arcname (默认情况下将与 filename 一致，但是不带驱动器盘符并会移除开头的路径分隔符)
            zf.write(fn, arcname=name)
            # 等价于以下两行代码
            # 切换目录， 直接将文件写入。不切换目录，则会在压缩文件中创建文件的整个路径
            # os.chdir(parent_path)
            # zf.write(name)
    b64body = GetBase64Data(zip_file_name)
    os.remove(zip_file_name)
    return b64body



def RunRpaTask(data,uuid):
    """
        使用命令行运行rpa任务
    :param exe:
    :param debug_port:
    :return:
    """
    task_exe = base_path + "/task-client.exe"
    taskbs64 = b64encode(json.dumps(data).encode("utf-8"))
    cmd = [task_exe.replace("\\","/"),str(taskbs64,'utf-8'),uuid]
    log.info(f"启动rpa任务 {' '.join(cmd)}")
    subprocess.Popen(cmd,shell=True)

# def GetBrowserExePath(data):
#     """
#         获取飞跨浏览器可执行文件的目录
#     :return:
#     """
#     Key1 = ""
#     Key2 = ""
#     browser_type = data.get("browser_type","feikua")
#     if browser_type.lower() == "feikua":
#         Key1 = "FeikuaBrowser"
#         Key2 = r"FeikuaBrowser\shell\open\command"
#         try:
#             key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, Key1)
#             # 获取注册表该位置的所有键值
#             exe_path = winreg.EnumValue(key,0)
#             exe_path = exe_path[1].replace('"',"")
#             log.info(f"注册列表浏览器执行路径:{exe_path}")
#             return exe_path
#         except Exception as e:
#             try:
#                 key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, Key2)
#                 exe_path = winreg.EnumValue(key,0)
#                 exe_path = exe_path[1].replace('"%1"',"").replace('"',"")
#                 log.info(f"注册列表浏览器执行路径:{exe_path}")
#                 return exe_path
#             except Exception as e:
#                 log.info(f"用户没有安装飞跨浏览器客户端")
#                 return ""
#     if browser_type.lower() == "chrome":
#         Key1 = r"ChromeHTML\shell\open\command"
#         try:
#             key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, Key1)
#             # 获取注册表该位置的所有键值
#             exe_path = winreg.EnumValue(key,0)
#             exe_path = exe_path[1].split(' --')[0].replace('"',"")
#             log.info(f"注册列表浏览器执行路径:{exe_path}")
#             return exe_path
#         except Exception as e:
#             key = "chrome.exe"
#             return key

if __name__ == '__main__':
    pass
    # port_is_using("127.0.0.1",4345)
    # result = port_is_using("127.0.0.1",7784)
    # print(result)
    # result = []
    # start,end = GenerateTime("-30",result)
    # print(start)
    # print(end)
    # print(get_current_time())
    # print(getTimeStrAgo("2023-05-01","2023-05-08"))
    # print(DiffTime("-7"))
    # jd = {"Action":"task_deliver","Data":{"taskUUID":"bvJ0ZW8jYJ4GdaV9L5","storeData":{"token":"--rpa=1 --test-site=1--token=MWI0MkJWWUZWZ1ZXQlZZRlZsTWRGeFZCQ1VjRGFnOVJSQTlSQmxZWlJFQVZVQlJxRDFGRUQxNEVWZ1ZLRnhOR0EwYzVSaE5YT1Z3Q0Yxd0ZHdw==","param":[],"storeplatform_url":"https://ys.endata.cn/DataMarket/BoxOffice","info":{"id":730,"name":"Test-012844","platform_data":{"id":1,"name":"亚马逊"},"site_data":{"id":1,"name":"美国"}}},"closeBroTime":200,"rpaScript":"4d0967756fbcb9b5cf0430f1f4559b43"},"Msg":""}
    # task_client = get_task_param1(jd,"1943d38b24e1b73969ed76ff9c2080a1")
    # zip_file_name = r"C:\Users\Administrator\Desktop\FeikuaBrowser\Test-012844730\Test-012844730.zip"
    # filename = [
    #     r"C:\Users\Administrator\Desktop\FeikuaBrowser\Test-012844730\1.xlsx",
    #     r"C:\Users\Administrator\Desktop\FeikuaBrowser\Test-012844730\2.xlsx",
    #     r"C:\Users\Administrator\Desktop\FeikuaBrowser\Test-012844730\3.xlsx",
    #     r"C:\Users\Administrator\Desktop\FeikuaBrowser\Test-012844730\4.xlsx"
    # ]
    # b64_body = File2Zip(zip_file_name,filename)
    # u = UploadDataBase()
    # u.MakeSuccessData(b64_body,task_client,4,"zip")
    # u.UploadData()
