

class ImmersionUI(object):
    def __init__(self, app):
        self.application = app
        self.method = getattr(self.application.module, self.application.parameters["immersive"])
        self.onExit = None

    def launch(self, resp):
        if resp == "Yes":
            self.method(*(self, screen))
            if self.onExit is not None:
                self.onExit()

    def start(self, onExit=None):
        self.onExit = onExit
        GUI.YNDialog("Fullscreen",
                     "The application " + self.application.title + " is requesting total control of the UI. Launch?",
                     self.launch).display()