import os
from datetime import datetime
from traceback import format_exc

import pygame


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class State(object):
    def __init__(self, activeApp=None, colors=None, icons=None, controller=None, eventQueue=None,
                 notificationQueue=None, functionbar=None, font=None, tFont=None, gui=None, appList=None,
                 keyboard=None):
        import pyos.gui
        from pyos.gui.colorpalette import ColorPalette
        from pyos.gui.eventqueue import EventQueue
        from pyos.gui.font import Font
        from pyos.gui.icons import Icons


        from pyos.notificationqueue import NotificationQueue
        from pyos.threading import Controller

        self.activeApplication = activeApp
        self.colorPalette = colors
        self.icons = icons
        self.threadController = controller
        self.eventQueue = eventQueue
        self.notificationQueue = notificationQueue
        self.functionBar = functionbar
        self.font = font
        self.typingFont = tFont
        self.appList = appList
        self.keyboard = keyboard
        self.recentAppSwitcher = None
        if gui is None:
            self.gui = pyos.gui.core()
        if colors is None:
            self.colorPalette = ColorPalette()
        if icons is None:
            self.icons = Icons()
        if controller is None:
            self.threadController = Controller()
        if eventQueue is None:
            self.eventQueue = EventQueue()
        if notificationQueue is None:
            self.notificationQueue = NotificationQueue()
        if font is None:
            self.font = Font()
        if tFont is None:
            self.typingFont = Font("res/RobotoMono-Regular.ttf")

    def getActiveApplication(self):
        return self.activeApplication

    def getColorPalette(self):
        return self.colorPalette

    def getIcons(self):
        return self.icons

    def getThreadController(self):
        return self.threadController

    def getEventQueue(self):
        return self.eventQueue

    def getNotificationQueue(self):
        return self.notificationQueue

    def getFont(self):
        return self.font

    def getTypingFont(self):
        return self.typingFont

    def getGUI(self):
        return self.gui

    def getScreen(self):
        return self.gui.getScreen();

    def getApplicationList(self):
        from pyos.application import ApplicationList, Application
        if self.appList is None: self.appList = ApplicationList()
        return self.appList

    def getFunctionBar(self):
        from pyos.gui.functionbar import FunctionBar
        if self.functionBar is None: self.functionBar = FunctionBar()
        return self.functionBar

    def getKeyboard(self):
        return self.keyboard

    def setActiveApplication(self, app):
        self.activeApplication = app

    def setColorPalette(self, colors):
        self.colorPalette = colors

    def setIcons(self, icons):
        self.icons = icons

    def setThreadController(self, controller):
        self.threadController = controller

    def setEventQueue(self, queue):
        self.eventQueue = queue

    def setNotificationQueue(self, queue):
        self.notificationQueue = queue

    def setFunctionBar(self, bar):
        self.functionBar = bar

    def setFont(self, font):
        self.font = font

    def setTypingFont(self, tfont):
        self.typingFont = tfont

    def setGUI(self, gui):
        self.gui = gui

    def setApplicationList(self, appList):
        self.appList = appList

    def setKeyboard(self, keyboard):
        self.keyboard = keyboard

    @staticmethod
    def getState():
        return  State.instance()

    @staticmethod
    def exit():
        state = State.instance()
        state.getThreadController().stopAllThreads()
        pygame.quit()
        os._exit(1)

    @staticmethod
    def rescue():
        state = State.instance()
        from pyos.application import Application
        rFnt = pygame.font.Font(None, 16)
        rClock = pygame.time.Clock()
        state.getNotificationQueue().clear()
        state.getEventQueue().clear()
        print "Recovery menu entered."
        while True:
            rClock.tick(10)
            state.getScreen().fill([0, 0, 0])
            pygame.draw.rect(state.getScreen(), [200, 200, 200], [0, 0, 280, 80])
            state.getScreen().blit(rFnt.render("Return to Python OS", 1, [20, 20, 20]), [40, 35])
            pygame.draw.rect(state.getScreen(), [20, 200, 20], [0, 80, 280, 80])
            state.getScreen().blit(rFnt.render("Stop all apps and return", 1, [20, 20, 20]), [40, 115])
            pygame.draw.rect(state.getScreen(), [20, 20, 200], [0, 160, 280, 80])
            state.getScreen().blit(rFnt.render("Stop current app and return", 1, [20, 20, 20]), [40, 195])
            pygame.draw.rect(state.getScreen(), [200, 20, 20], [0, 240, 280, 80])
            state.getScreen().blit(rFnt.render("Exit completely", 1, [20, 20, 20]), [40, 275])
            pygame.display.flip()
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT or evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
                    print "Quit signal detected."
                    try:
                        state.exit()
                    except:
                        pygame.quit()
                        exit()
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    if evt.pos[1] >= 80:
                        if evt.pos[1] >= 160:
                            if evt.pos[1] >= 240:
                                print "Exiting."
                                try:
                                    state.exit()
                                except:
                                    pygame.quit()
                                    exit()
                            else:
                                print "Stopping current app"
                                try:
                                    Application.fullCloseCurrent()
                                except:
                                    print "Regular stop failed!"
                                    Application.setActiveApp(state.getApplicationList().getApp("home"))
                                return
                        else:
                            print "Closing all active applications"
                            for a in state.getApplicationList().activeApplications:
                                try:
                                    a.deactivate()
                                except:
                                    print "The app " + str(a.name) + " failed to deactivate!"
                                    state.getApplicationList().activeApplications.remove(a)
                            state.getApplicationList().getApp("home").activate()
                            return
                    else:
                        print "Returning to Python OS."
                        return

    @staticmethod
    def error_recovery(message="Unknown", data=None):
        print message
        state = State.instance()
        state.getScreen().fill([200, 100, 100])
        rf = pygame.font.Font(None, 24)
        sf = pygame.font.Font(None, 18)
        state.getScreen().blit(rf.render("Failure detected.", 1, (200, 200, 200)), [20, 20])
        f = open("temp/last_error.txt", "w")
        txt = "Python OS 6 Error Report\nTIME: " + str(datetime.now())
        txt += "\n\nOpen Applications: " + (str([a.name for a in
                                                 state.getApplicationList().activeApplications]) if data != "NoAppDump" else "Not Yet Initialized")
        txt += "\nMessage: " + message
        txt += "\nAdditional Data:\n"
        txt += str(data)
        txt += "\n\nTraceback:\n"
        txt += format_exc()
        f.write(txt)
        f.close()
        state.getScreen().blit(sf.render("Traceback saved.", 1, (200, 200, 200)), [20, 80])
        state.getScreen().blit(sf.render("Location: temp/last_error.txt", 1, (200, 200, 200)), [20, 100])
        state.getScreen().blit(sf.render("Message:", 1, (200, 200, 200)), [20, 140])
        state.getScreen().blit(sf.render(message, 1, (200, 200, 200)), [20, 160])
        pygame.draw.rect(state.getScreen(), [200, 200, 200], [0, 280, 240, 40])
        state.getScreen().blit(sf.render("Return to Python OS", 1, (20, 20, 20)), [20, 292])
        pygame.draw.rect(state.getScreen(), [50, 50, 50], [0, 240, 240, 40])
        state.getScreen().blit(sf.render("Open Recovery Menu", 1, (200, 200, 200)), [20, 252])
        rClock = pygame.time.Clock()
        pygame.display.flip()
        while True:
            rClock.tick(10)
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT or evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
                    try:
                        state.exit()
                    except:
                        pygame.quit()
                        exit()
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    if evt.pos[1] >= 280:
                        return
                    elif evt.pos[1] >= 240:
                        state.rescue()
                        return

    @staticmethod
    def main():
        from pyos.gui.intermediateupdateevent import IntermediateUpdateEvent
        from pyos.gui.longclickevent import LongClickEvent
        from pyos.application import Application#
        state = State.instance()
        while True:
            # Limit FPS
            state.getGUI().timer.tick(state.getGUI().update_interval)
            # Update event queue
            state.getEventQueue().check()
            # Refresh main thread controller
            state.getThreadController().run()
            # Paint UI
            if state.getActiveApplication() is not None:
                try:
                    state.getActiveApplication().ui.render()
                except:
                    State.error_recovery("UI error.", "FPS: " + str(state.getGUI().update_interval))
                    Application.fullCloseCurrent()
            state.getFunctionBar().render()
            if state.getKeyboard() is not None and state.getKeyboard().active:
                state.getKeyboard().render(state.getScreen())

            state.getGUI().refresh()
            # Check Events
            latestEvent = state.getEventQueue().getLatestComplete()
            if latestEvent is not None:
                clickedChild = None
                if state.getKeyboard() is not None and state.getKeyboard().active:
                    if latestEvent.pos[1] < state.getKeyboard().baseContainer.computedPosition[1]:
                        if state.getActiveApplication().ui.getClickedChild(
                                latestEvent) == state.getKeyboard().textEntryField:
                            state.getKeyboard().textEntryField.onClick()
                        else:
                            state.getKeyboard().deactivate()
                        continue
                    clickedChild = state.getKeyboard().baseContainer.getClickedChild(latestEvent)
                    if clickedChild is None:
                        clickedChild = state.getActiveApplication().ui.getClickedChild(latestEvent)
                    if clickedChild is None and state.getKeyboard().textEntryField.computedPosition == [0,
                                                                                                        0] and state.getKeyboard().textEntryField.checkClick(
                        latestEvent):
                        clickedChild = state.getKeyboard().textEntryField
                else:
                    if latestEvent.pos[1] < state.getGUI().height - 40:
                        if state.getActiveApplication() is not None:
                            clickedChild = state.getActiveApplication().ui.getClickedChild(latestEvent)
                    else:
                        clickedChild = state.getFunctionBar().container.getClickedChild(latestEvent)
                if clickedChild is not None:
                    try:
                        if isinstance(latestEvent, LongClickEvent):
                            clickedChild.onLongClick()
                        else:
                            if isinstance(latestEvent, IntermediateUpdateEvent):
                                clickedChild.onIntermediateUpdate()
                            else:
                                clickedChild.onClick()
                    except:
                        State.instance().error_recovery("Event execution error", "Click event: " + str(latestEvent))

    @staticmethod
    def state_shell():
        # For debugging purposes only. Do not use in actual code!
        print "Python OS 6 State Shell. Type \"exit\" to quit."
        user_input = raw_input("S> ")
        while user_input != "exit":
            if not user_input.startswith("state.") and user_input.find("Static") == -1:
                if user_input.startswith("."):
                    user_input = "state" + user_input
                else:
                    user_input = "state." + user_input
            print eval(user_input, {"state": State, "Static": State})
            user_input = raw_input("S> ")
        State.instance().exit(True)
