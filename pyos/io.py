import json


def readFile(path):
    f = open(path, "rU")
    lines = []
    for line in f.readlines():
        lines.append(line.rstrip())
    f.close()
    return lines


def readJSON(path, default={}):
    try:
        f = open(path, "rU")
        jsd = json.loads(str(unicode(f.read(), errors="ignore")))
        f.close()
        return jsd
    except:
        return default