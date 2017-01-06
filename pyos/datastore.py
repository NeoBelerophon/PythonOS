import json
import os


class DataStore(object):
    def __init__(self, app):
        self.application = app
        self.dsPath = os.path.join("res/", app.name + ".ds")
        self.data = []

    def getStore(self):
        if not os.path.exists(self.dsPath):
            wf = open(self.dsPath, "w")
            json.dump({"dsApp": self.application.name}, wf)
            wf.close()
        rf = open(self.dsPath, "rU")
        self.data = json.loads(str(unicode(rf.read(), errors="ignore")))
        rf.close()
        return self.data

    def saveStore(self):
        wf = open(self.dsPath, "w")
        json.dump(self.data, wf)
        wf.close()

    def get(self, key, default=None):
        return self.getStore().get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.saveStore()

    def __getitem__(self, itm):
        return self.get(itm)

    def __setitem__(self, key, val):
        self.set(key, val)