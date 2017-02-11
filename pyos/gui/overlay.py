from pyos.gui.container import Container
from pyos.state import State


class Overlay(object):
    def __init__(self, position, **data):
        self.position = list(position)
        self.displayed = False
        self.width = int(int(data.get("width").rstrip("%")) * (State.instance().getActiveApplication().ui.width/100.0)) if type(data.get("width")) == str else data.get("width", State.instance().getGUI().width)
        self.height = int(int(data.get("height").rstrip("%")) * (State.instance().getActiveApplication().ui.height/100.0)) if type(data.get("height")) == str else data.get("height", State.instance().getGUI().height-40)
        self.color = data.get("color", State.instance().getColorPalette().getColor("background"))
        self.baseContainer = Container((0, 0), width=State.instance().getGUI().width, height=State.instance().getActiveApplication().ui.height, color=(0, 0, 0, 0), onClick=self.hide)
        self.container = data.get("container", Container(self.position[:], width=self.width, height=self.height, color=self.color))
        self.baseContainer.addChild(self.container)
        self.application = State.instance().getActiveApplication()

    def display(self):
        self.application = State.instance().getActiveApplication()
        self.application.ui.setDialog(self)
        self.displayed = True

    def hide(self):
        self.application.ui.clearDialog()
        self.application.ui.refresh()
        self.displayed = False

    def addChild(self, child):
        self.container.addChild(child)