import pygame

from pyos.application import Application
from pyos.gui import GUI
from pyos.state import State


class Notification(object):
    def __init__(self, title, text, **data):
        self.title = title
        self.text = text
        self.active = True
        self.source = data.get("source", None)
        self.image = data.get("image", None)
        if self.source is not None:
            self.onSelectedMethod = data.get("onSelected", self.source.activate)
        else:
            self.onSelectedMethod = data.get("onSelected", Application.dummy)
        self.onSelectedData = data.get("onSelectedData", ())

    def onSelected(self):
        self.clear()
        State.instance.getFunctionBar().toggleNotificationMenu()
        self.onSelectedMethod(*self.onSelectedData)

    def clear(self):
        self.active = False
        State.instance.getNotificationQueue().sweep()
        State.instance.getFunctionBar().notificationMenu.refresh()

    def getContainer(self, c_width=200, c_height=40):
        cont = GUI.Container((0, 0), width=c_width, height=c_height, transparent=True, onClick=self.onSelected,
                             onLongClick=self.clear)
        if self.image is not None:
            try:
                self.image.setPosition([0, 0])
                cont.addChild(self.image)
            except:
                if isinstance(self.image, pygame.Surface):
                    self.image = GUI.Image((0, 0), surface=self.image, onClick=self.onSelected)
                else:
                    self.image = GUI.Image((0, 0), path=self.image, onClick=self.onSelected)
        else:
            self.image = GUI.Image((0, 0), surface=State.instance.getIcons().getLoadedIcon("unknown"), onClick=self.onSelected,
                                   onLongClick=self.clear)
        rtitle = GUI.Text((41, 0), self.title, (200, 200, 200), 20, onClick=self.onSelected, onLongClick=self.clear)
        rtxt = GUI.Text((41, 24), self.text, (200, 200, 200), 14, onClick=self.onSelected, onLongClick=self.clear)
        cont.addChild(self.image)
        cont.addChild(rtitle)
        cont.addChild(rtxt)
        return cont


class PermanentNotification(Notification):
    def clear(self):
        pass

    def forceClear(self):
        super(PermanentNotification, self).clear()


class NotificationQueue(object):
    def __init__(self):
        self.notifications = []
        self.new = False

    def sweep(self):
        for notification in self.notifications:
            if not notification.active:
                self.notifications.remove(notification)

    def push(self, notification):
        self.notifications.insert(0, notification)
        self.new = True

    def clear(self):
        self.notifications = []