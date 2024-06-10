import os


def get_info_dsn():
    try:
        file = open(os.sys.path[0] + '\\dsn.rc', 'r')
        dsn = {}
        for line in file:
            k, v = line.strip().split('=')
            dsn[k.strip()] = v.strip()
        file.close()
        return dsn
    except:
        file = open(os.sys.path[0] + '//dsn.rc', 'r')
        dsn = {}
        for line in file:
            k, v = line.strip().split('=')
            dsn[k.strip()] = v.strip()
        file.close()
        return dsn