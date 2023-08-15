import os


def connect_adsl():
    try:
        cmd_string = 'rasdial 宽带连接 059593100351 765484'
        os.system(cmd_string)
    except:
        pass