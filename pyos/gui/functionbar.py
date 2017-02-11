from datetime import datetime

from pyos.gui.notificationmenu import NotificationMenu
from pyos.gui.recentappswitcher import RecentAppSwitcher
from pyos.state import State
from pyos.application import Application
from pyos.gui.container import Container
from pyos.gui.image import Image
from pyos.gui.text import Text




class FunctionBar(object):
    def __init__(self):
        self.container = Container((0, State.instance().getGUI().height-40), background=State.instance().getColorPalette().getColor("background"), width=State.instance().getGUI().width, height=40)
        self.launcherApp = State.instance().getApplicationList().getApp("launcher")
        self.notificationMenu = NotificationMenu()
        self.recentAppSwitcher = RecentAppSwitcher()
        self.menu_button = Image((0, 0), surface=State.instance().getIcons().getLoadedIcon("menu"), onClick=self.activateLauncher, onLongClick=Application.fullCloseCurrent)
        self.app_title_text = Text((42, 8), "Python OS 6", State.instance().getColorPalette().getColor("item"), 20, onClick=self.toggleRecentAppSwitcher)
        self.clock_text = Text((State.instance().getGUI().width-45, 8), self.formatTime(), State.instance().getColorPalette().getColor("accent"), 20, onClick=self.toggleNotificationMenu, onLongClick=State.instance().rescue) #Add Onclick Menu
        self.container.addChild(self.menu_button)
        self.container.addChild(self.app_title_text)
        self.container.addChild(self.clock_text)

    def formatTime(self):
        time = str(datetime.now())
        if time.startswith("0"): time = time[1:]
        return time[time.find(" ")+1:time.find(":", time.find(":")+1)]

    def render(self):
        if State.instance().getNotificationQueue().new:
            self.clock_text.color = (255, 59, 59)
        self.clock_text.text = self.formatTime()
        self.clock_text.refresh()
        self.container.render(State.instance().getScreen())

    def activateLauncher(self):
        if State.instance().getActiveApplication() != self.launcherApp:
            self.launcherApp.activate()
        else:
            Application.fullCloseCurrent()

    def toggleNotificationMenu(self):
        if self.notificationMenu.displayed:
            self.notificationMenu.hide()
            return
        else:
            self.notificationMenu.display()

    def toggleRecentAppSwitcher(self):
        if self.recentAppSwitcher.displayed:
            self.recentAppSwitcher.hide()
            return
        else:
            self.recentAppSwitcher.display()
