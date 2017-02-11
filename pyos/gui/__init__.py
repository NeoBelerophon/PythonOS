import __builtin__
import os
import pygame
from pyos.state import State

settings = {}
DEFAULT = 0xada


class core(object):
    def __init__(self):
        self.orientation = 0 # 0 for portrait, 1 for landscape
        self.timer = None
        self.update_interval = settings.get("target_fps", 30)
        pygame.init()
        try:
            pygame.display.set_icon(pygame.image.load("res/icons/menu.png"))
        except:
            pass
        if __import__("sys").platform == "linux2" and os.path.exists("/etc/pyos"):
            pygame.mouse.set_visible(False)
            info = pygame.display.Info()
            self.width = info.current_w
            self.height = info.current_h
            self.screen = pygame.display.set_mode((info.current_w, info.current_h))
        else:
            self.screen = pygame.display.set_mode((settings.get("screen_size", {"width":240}).get("width"),
                                              settings.get("screen_size", {"height":320}).get("height")), pygame.HWACCEL)
            self.width = self.screen.get_width()
            self.height = self.screen.get_height()
        try:
            self.screen.blit(pygame.image.load("res/splash2.png"), [0, 0])
        except:
            self.screen.blit(pygame.font.Font(None, 20).render("Loading Python OS 6...", 1, (200, 200, 200)), [5, 5])
        pygame.display.flip()
        __builtin__.screen = self.screen
        globals()["screen"] = self.screen
        self.timer = pygame.time.Clock()
        pygame.display.set_caption("PyOS 6")

    def orient(self):
        from pyos.state import State
        self.orientation = 0 if self.orientation == 1 else 1
        bk = self.width
        self.width = self.height
        self.height = bk
        self.screen = pygame.display.set_mode((self.width, self.height))
        for app in State.instance().getApplicationList().getApplicationList():
            app.ui.refresh()
        State.rescue()

    def repaint(self):
        from pyos.state import State
        self.screen.fill(State.instance().getColorPalette().getColor("background"))

    def refresh(self):
        pygame.display.flip()

    def getScreen(self):
        return self.screen

    def monitorFPS(self):
        real = round(self.timer.get_fps())
        if real >= self.update_interval and self.update_interval < 30:
            self.update_interval += 1
        else:
            if self.update_interval > 10:
                self.update_interval -= 1

    def displayStandbyText(self, text="Stand by...", size=20, color=(20,20,20), bgcolor=(100, 100, 200)):
        pygame.draw.rect(self.screen, bgcolor, [0, ((State.instance().getGUI().height - 40)/2) - size, State.instance().getGUI().width, 2*size])
        self.screen.blit(State.instance().getFont().get(size).render(text, 1, color), (5, ((State.instance().getGUI().height - 40)/2) - size+(size/4)))
        pygame.display.flip()


    @staticmethod
    def getCenteredCoordinates(component, larger):
        return [(larger.computedWidth / 2) - (component.computedWidth / 2), (larger.computedHeight / 2) - (component.computedHeight / 2)]

