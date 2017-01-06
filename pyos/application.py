import json
import os
from importlib import import_module
from shutil import rmtree
from zipfile import ZipFile

from pyos.io import readJSON

from pyos.immersionUI import ImmersionUI
from pyos.datastore import DataStore
from pyos.gui import GUI
from pyos.state import State
from pyos.threading import Thread


class Application(object):
    @staticmethod
    def dummy(*args, **kwargs):
        pass

    @staticmethod
    def getListings():
        return readJSON("apps/apps.json")

    @staticmethod
    def chainRefreshCurrent():
        if State.instance.getActiveApplication() is not None:
            State.instance.getActiveApplication().chainRefresh()

    @staticmethod
    def setActiveApp(app="prev"):
        if app == "prev":
            app = State.instance.getApplicationList().getMostRecentActive()
        State.instance.setActiveApplication(app)
        State.instance.getFunctionBar().app_title_text.setText(State.instance.getActiveApplication().title)
        State.instance.getGUI().repaint()
        State.instance.getApplicationList().pushActiveApp(app)

    @staticmethod
    def fullCloseApp(app):
        app.deactivate(False)
        State.instance.getApplicationList().getMostRecentActive().activate(fromFullClose=True)

    @staticmethod
    def fullCloseCurrent():
        if State.instance.getActiveApplication().name != "home":
            Application.fullCloseApp(State.instance.getActiveApplication())

    @staticmethod
    def removeListing(location):
        alist = Application.getListings()
        try:
            del alist[location]
        except:
            print "The application listing for " + location + " could not be removed."
        listingsfile = open("apps/apps.json", "w")
        json.dump(alist, listingsfile)
        listingsfile.close()

    @staticmethod
    def install(packageloc):
        package = ZipFile(packageloc, "r")
        package.extract("app.json", "temp/")
        app_info = readJSON("temp/app.json")
        app_name = str(app_info.get("name"))
        if app_name not in State.instance.getApplicationList().applications.keys():
            os.mkdir(os.path.join("apps/", app_name))
        else:
            print "Upgrading " + app_name
        package.extractall(os.path.join("apps/", app_name))
        package.close()
        alist = Application.getListings()
        alist[os.path.join("apps/", app_name)] = app_name
        listingsfile = open("apps/apps.json", "w")
        json.dump(alist, listingsfile)
        listingsfile.close()
        return app_name

    @staticmethod
    def registerDebugAppAsk():
        State.instance.getApplicationList().getApp("files").getModule().FolderPicker((10, 10), width=220, height=260,
                                                                            onSelect=Application.registerDebugApp,
                                                                            startFolder="apps/").display()

    @staticmethod
    def registerDebugApp(path):
        app_info = readJSON(os.path.join(path, "app.json"))
        app_name = str(app_info.get("name"))
        alist = Application.getListings()
        alist[os.path.join("apps/", app_name)] = app_name
        listingsfile = open("apps/apps.json", "w")
        json.dump(alist, listingsfile)
        listingsfile.close()
        State.instance.getApplicationList().reloadList()
        GUI.OKDialog("Registered", "The application from " + path + " has been registered on the system.").display()

    def __init__(self, location):
        self.parameters = {}
        self.location = location
        app_data = readJSON(os.path.join(location, "app.json").replace("\\", "/"))
        self.name = str(app_data.get("name"))
        self.title = str(app_data.get("title", self.name))
        self.version = float(app_data.get("version", 0.0))
        self.author = str(app_data.get("author", "No Author"))
        self.module = import_module("apps." + str(app_data.get("module", self.name)), "apps")
        self.module.state = State.instance
        self.file = None
        try:
            self.mainMethod = getattr(self.module, str(app_data.get("main")))
        except:
            self.mainMethod = Application.dummy
        try:
            self.parameters = app_data.get("more")
        except:
            pass
        self.description = app_data.get("description", "No Description.")
        # Immersion check
        if "immersive" in self.parameters:
            self.immersionUI = ImmersionUI(self)
        else:
            self.immersionUI = None
        # check for and load event handlers
        self.evtHandlers = {}
        if "onStart" in self.parameters:
            self.evtHandlers["onStartReal"] = self.parameters["onStart"]
        self.evtHandlers["onStart"] = [self.onStart, ()]
        if "onStop" in self.parameters: self.evtHandlers["onStop"] = getattr(self.module, self.parameters["onStop"])
        if "onPause" in self.parameters: self.evtHandlers["onPause"] = getattr(self.module, self.parameters["onPause"])
        if "onResume" in self.parameters: self.evtHandlers["onResume"] = getattr(self.module,
                                                                                 self.parameters["onResume"])
        if "onCustom" in self.parameters: self.evtHandlers["onCustom"] = getattr(self.module,
                                                                                 self.parameters["onCustom"])
        if "onOSLaunch" in self.parameters: self.evtHandlers["onOSLaunch"] = getattr(self.module,
                                                                                     self.parameters["onOSLaunch"])
        self.thread = Thread(self.mainMethod, **self.evtHandlers)
        self.ui = GUI.AppContainer(self)
        self.dataStore = DataStore(self)
        self.thread = Thread(self.mainMethod, **self.evtHandlers)

    def getModule(self):
        return self.module

    def chainRefresh(self):
        self.ui.refresh()

    def onStart(self):
        self.loadColorScheme()
        if "onStartReal" in self.evtHandlers and not self.evtHandlers.get("onStartBlock", False): getattr(self.module,
                                                                                                          self.evtHandlers[
                                                                                                              "onStartReal"])(
            State.instance, self)
        if self.evtHandlers.get("onStartBlock", False):
            self.evtHandlers["onStartBlock"] = False

    def loadColorScheme(self):
        if "colorScheme" in self.parameters:
            State.instance.getColorPalette().setScheme(self.parameters["colorScheme"])
        else:
            State.instance.getColorPalette().setScheme()
        self.ui.backgroundColor = State.instance.getColorPalette().getColor("background")
        self.ui.refresh()

    def activate(self, **data):
        try:
            if data.get("noOnStart", False):
                self.evtHandlers["onStartBlock"] = True
            if State.instance.getActiveApplication() == self: return
            if State.instance.getApplicationList().getMostRecentActive() != None and not data.get("fromFullClose", False):
                State.instance.getApplicationList().getMostRecentActive().deactivate()
            Application.setActiveApp(self)
            self.loadColorScheme()
            if self.thread in State.instance.getThreadController().threads:
                self.thread.setPause(False)
            else:
                if self.thread.stop:
                    self.thread = Thread(self.mainMethod, **self.evtHandlers)
                State.instance.getThreadController().addThread(self.thread)
        except:
            State.error_recovery("Application init error.", "App name: " + self.name)

    def getIcon(self):
        if "icon" in self.parameters:
            if self.parameters["icon"] == None:
                return False
            return State.instance.getIcons().getLoadedIcon(self.parameters["icon"], self.location)
        else:
            return State.instance.getIcons().getLoadedIcon("unknown")

    def deactivate(self, pause=True):
        if "persist" in self.parameters:
            if self.parameters["persist"] == False:
                pause = False
        if pause:
            self.thread.setPause(True)
        else:
            self.ui.clearChildren()
            self.thread.setStop()
            State.instance.getApplicationList().closeApp(self)
        State.instance.getColorPalette().setScheme()

    def uninstall(self):
        rmtree(self.location, True)
        Application.removeListing(self.location)


class ApplicationList(object):
    def __init__(self):
        self.applications = {}
        self.activeApplications = []
        applist = Application.getListings()
        for key in dict(applist).keys():
            try:
                self.applications[applist.get(key)] = Application(key)
            except:
                State.error_recovery("App init error: " + key, "NoAppDump")

    def getApp(self, name):
        if name in self.applications:
            return self.applications[name]
        else:
            return None

    def getApplicationList(self):
        return self.applications.values()

    def getApplicationNames(self):
        return self.applications.keys()

    def pushActiveApp(self, app):
        if app not in self.activeApplications:
            self.activeApplications.insert(0, app)
        else:
            self.switchLast(app)

    def closeApp(self, app=None):
        if app is None:
            if len(self.activeApplications) > 1:
                return self.activeApplications.pop(0)
        self.activeApplications.remove(app)

    def switchLast(self, app):
        if app is None:
            return
        self.activeApplications = [self.activeApplications.pop(
            self.activeApplications.index(app))] + self.activeApplications

    def getMostRecentActive(self):
        if len(self.activeApplications) > 0:
            return self.activeApplications[0]

    def getPreviousActive(self):
        if len(self.activeApplications) > 1:
            return self.activeApplications[1]

    def reloadList(self):
        applist = Application.getListings()
        for key in dict(applist).keys():
            try:
                if (applist.get(key) not in self.applications.keys()) and not State.instance.getActiveApplication().name == key:
                    self.applications[applist.get(key)] = Application(key)
            except:
                State.error_recovery("App init error: " + key, "NoAppDump")
        for key in self.applications.keys():
            if key not in applist.values():
                del self.applications[key]