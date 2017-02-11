from pyos.application import Application
from pyos.gui.button import Button
from pyos.gui.container import Container
from pyos.gui.dialog import YNDialog
from pyos.gui.image import Image
from pyos.gui.overlay import Overlay
from pyos.gui.pagedcontainer import PagedContainer
from pyos.gui.text import Text
from pyos.state import State
import pyos.gui as gui

class RecentAppSwitcher(Overlay):
    def __init__(self):
        super(RecentAppSwitcher, self).__init__((0, State.instance().getScreen().get_height()-100), height=60)
        self.container.border = 1
        self.container.borderColor = State.instance().getColorPalette().getColor("item")

    def populate(self):
        self.container.clearChildren()
        self.recent_pages = PagedContainer((20, 0), width=self.width-40, height=60, hideControls=True)
        self.recent_pages.addPage(self.recent_pages.generatePage())
        self.btnLeft = Button((0, 0), "<", State.instance().getColorPalette().getColor("accent"), State.instance().getColorPalette().getColor("item"), 20, width=20, height=60,
                                  onClick=self.recent_pages.pageLeft)
        self.btnRight = Button((self.width-20, 0), ">", State.instance().getColorPalette().getColor("accent"), State.instance().getColorPalette().getColor("item"), 20, width=20, height=60,
                                  onClick=self.recent_pages.pageRight)
        per_app = (self.width-40)/4
        current = 0
        for app in State.instance().getApplicationList().activeApplications:
            if app != State.instance().getActiveApplication() and app.parameters.get("persist", True) and app.name != "home":
                if current >= 4:
                    current = 0
                    self.recent_pages.addPage(self.recent_pages.generatePage())
                cont = Container((per_app*current, 0), transparent=True, width=per_app, height=self.height, border=1, borderColor=State.instance().getColorPalette().getColor("item"),
                                     onClick=self.activate, onClickData=(app,), onLongClick=self.closeAsk, onLongClickData=(app,))
                cont.SKIP_CHILD_CHECK = True
                icon = app.getIcon()
                if not icon: icon = State.instance().getIcons().getLoadedIcon("unknown")
                img = Image((0, 5), surface=icon)
                img.position[0] = gui.core.getCenteredCoordinates(img, cont)[0]
                name = Text((0, 45), app.title, State.instance().getColorPalette().getColor("item"), 10)
                name.position[0] = gui.core.getCenteredCoordinates(name, cont)[0]
                cont.addChild(img)
                cont.addChild(name)
                self.recent_pages.addChild(cont)
                current += 1
        if len(self.recent_pages.getPage(0).childComponents) == 0:
            notxt = Text((0, 0), "No Recent Apps", State.instance().getColorPalette().getColor("item"), 16)
            notxt.position = gui.core.getCenteredCoordinates(notxt, self.recent_pages.getPage(0))
            self.recent_pages.addChild(notxt)
        self.recent_pages.goToPage()
        self.addChild(self.recent_pages)
        self.addChild(self.btnLeft)
        self.addChild(self.btnRight)

    def display(self):
        self.populate()
        super(RecentAppSwitcher, self).display()

    def activate(self, app):
        self.hide()
        app.activate()

    def closeAsk(self, app):
        YNDialog("Close", "Are you sure you want to close the app "+app.title+"?", self.close, (app,)).display()

    def close(self, app, resp):
        if resp == "Yes":
            app.deactivate(False)
            self.hide()
            if State.instance().getActiveApplication() == State.instance().getApplicationList().getApp("launcher"):
                Application.fullCloseCurrent()
