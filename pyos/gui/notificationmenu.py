from pyos.state import State
from pyos.gui.button import Button
from pyos.gui.listscrollablecontainer import ListScrollableContainer
from pyos.gui.overlay import Overlay
from pyos.gui.text import Text


class NotificationMenu(Overlay):
    def __init__(self):
        super(NotificationMenu, self).__init__(("20%", "25%"), width="80%", height="75%", color=(20, 20, 20, 200))
        self.text = Text((1, 1), "Notifications", (200, 200, 200), 18)
        self.clearAllBtn = Button((self.width-50, 0), "Clear", (200, 200, 200), (20, 20, 20), width=50, height=20, onClick=self.clearAll)
        self.nContainer = ListScrollableContainer((0, 20), width="80%", height=self.height-20, transparent=True, margin=5)
        self.addChild(self.text)
        self.addChild(self.clearAllBtn)
        self.addChild(self.nContainer)
        self.refresh()

    def refresh(self):
        self.nContainer.clearChildren()
        for notification in State.instance().getNotificationQueue().notifications:
            self.nContainer.addChild(notification.getContainer())

    def display(self):
        self.refresh()
        State.instance().getNotificationQueue().new = False
        State.instance().getFunctionBar().clock_text.color = State.instance().getColorPalette().getColor("accent")
        super(NotificationMenu, self).display()

    def clearAll(self):
        State.instance().getNotificationQueue().clear()
        self.refresh()