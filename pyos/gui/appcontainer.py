from pyos.gui.container import Container
from pyos.state import State

class AppContainer(Container):
    def __init__(self, application):
        self.application = application
        self.dialogs = []
        self.dialogScreenFreezes = []
        self.dialogComponentsFreezes = []
        self.scaleX = 1.0
        self.scaleY = 1.0
        if self.application.parameters.get("resize", False):
            dW = float(self.application.parameters.get("size", {"width": 240}).get("width"))
            dH = float(self.application.parameters.get("size", {"height": 320}).get("height"))
            self.scaleX = (State.instance().getGUI().width / dW)
            self.scaleY = (State.instance().getGUI().height / dH)
            super(AppContainer, self).__init__((0, 0), width=State.instance().getScreen().get_width(), height=State.instance().getScreen().get_height()-40,
                                                   resizable=True, fixedSize=True)
        else:
            super(AppContainer, self).__init__((0, 0), width=State.instance().getScreen().get_width(), height=State.instance().getScreen().get_height()-40,
                                                   resizable=False, fixedSize=True)

    def setDialog(self, dialog):
        self.dialogs.insert(0, dialog)
        self.dialogComponentsFreezes.insert(0, self.childComponents[:])
        self.dialogScreenFreezes.insert(0, self.surface.copy())
        self.addChild(dialog.baseContainer)

    def clearDialog(self):
        self.dialogs.pop(0)
        self.childComponents = self.dialogComponentsFreezes[0]
        self.dialogComponentsFreezes.pop(0)
        self.dialogScreenFreezes.pop(0)

    def render(self):
        if self.dialogs == []:
            super(AppContainer, self).render(self.surface)
        else:
            self.surface.blit(self.dialogScreenFreezes[0], (0, 0))
            self.dialogs[0].baseContainer.render(self.surface)
        State.instance().getScreen().blit(self.surface, self.position)

    def refresh(self):
        self.width = State.instance().getScreen().get_width()
        self.height = State.instance().getScreen().get_height() - 40
        if self.application.parameters.get("resize", False):
            dW = float(self.application.parameters.get("size", {"width": 240}).get("width"))
            dH = float(self.application.parameters.get("size", {"height": 320}).get("height"))
            self.scaleX = 1.0 * (State.instance().getGUI().width / dW)
            self.scaleY = 1.0 * (State.instance().getGUI().height / dH)
        #super(GUI.AppContainer, self).refresh()