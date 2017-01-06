import json
import os
from copy import deepcopy
from datetime import datetime

import __builtin__
import pygame

from pyos.state import State, screen
from pyos.application import Application


settings = {}
DEFAULT = 0xada

class GUI(object):
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
            screen = pygame.display.set_mode((info.current_w, info.current_h))
        else:
            screen = pygame.display.set_mode((settings.get("screen_size", {"width":240}).get("width"),
                                              settings.get("screen_size", {"height":320}).get("height")), pygame.HWACCEL)
            self.width = screen.get_width()
            self.height = screen.get_height()
        try:
            screen.blit(pygame.image.load("res/splash2.png"), [0, 0])
        except:
            screen.blit(pygame.font.Font(None, 20).render("Loading Python OS 6...", 1, (200, 200, 200)), [5, 5])
        pygame.display.flip()
        __builtin__.screen = screen
        globals()["screen"] = screen
        self.timer = pygame.time.Clock()
        pygame.display.set_caption("PyOS 6")

    def orient(self):
        global screen
        self.orientation = 0 if self.orientation == 1 else 1
        bk = self.width
        self.width = self.height
        self.height = bk
        screen = pygame.display.set_mode((self.width, self.height))
        for app in State.instance.getApplicationList().getApplicationList():
            app.ui.refresh()
        State.rescue()

    def repaint(self):
        screen.fill(State.instance.getColorPalette().getColor("background"))

    def refresh(self):
        pygame.display.flip()

    def getScreen(self):
        return screen

    def monitorFPS(self):
        real = round(self.timer.get_fps())
        if real >= self.update_interval and self.update_interval < 30:
            self.update_interval += 1
        else:
            if self.update_interval > 10:
                self.update_interval -= 1

    def displayStandbyText(self, text="Stand by...", size=20, color=(20,20,20), bgcolor=(100, 100, 200)):
        pygame.draw.rect(screen, bgcolor, [0, ((State.instance.getGUI().height - 40)/2) - size, State.instance.getGUI().width, 2*size])
        screen.blit(State.instance.getFont().get(size).render(text, 1, color), (5, ((State.instance.getGUI().height - 40)/2) - size+(size/4)))
        pygame.display.flip()

    @staticmethod
    def getCenteredCoordinates(component, larger):
        return [(larger.computedWidth / 2) - (component.computedWidth / 2), (larger.computedHeight / 2) - (component.computedHeight / 2)]

    class Font(object):
        def __init__(self, path="res/RobotoCondensed-Regular.ttf", minSize=10, maxSize=30):
            self.path = path
            curr_size = minSize
            self.sizes = {}
            self.ft_support = True
            self.ft_sizes = {}
            while curr_size <= maxSize:
                if self.ft_support:
                    try:
                        self.ft_sizes[curr_size] = pygame.freetype.Font(path, curr_size)
                    except:
                        self.ft_support = False
                self.sizes[curr_size] = pygame.font.Font(path, curr_size)
                curr_size += 1

        def get(self, size=14, ft=False):
            if ft and self.ft_support:
                if size not in self.ft_sizes:
                    self.ft_sizes[size] = pygame.freetype.Font(self.path, size)
                return self.ft_sizes[size]
            else:
                if size not in self.sizes:
                    self.sizes[size] = pygame.font.Font(self.path, size)
                return self.sizes[size]

    class Icons(object):
        def __init__(self):
            self.rootPath = "res/icons/"
            self.icons = {
                     "menu": "menu.png",
                     "unknown": "unknown.png",
                     "error": "error.png",
                     "warning": "warning.png",
                     "file": "file.png",
                     "folder": "folder.png",
                     "wifi": "wifi.png",
                     "python": "python.png",
                     "quit": "quit.png",
                     "copy": "files_copy.png",
                     "delete": "files_delete.png",
                     "goto": "files_goto.png",
                     "home_dir": "files_home.png",
                     "move": "files_move.png",
                     "select": "files_select.png",
                     "up": "files_up.png",
                     "back": "back.png",
                     "forward": "forward.png",
                     "search": "search.png",
                     "info": "info.png",
                     "open": "open.png",
                     "save": "save.png"
                     }

        def getIcons(self):
            return self.icons

        def getRootPath(self):
            return self.rootPath

        def getLoadedIcon(self, icon, folder=""):
            try:
                return pygame.image.load(os.path.join(self.rootPath, self.icons[icon]))
            except:
                if os.path.exists(icon):
                    return pygame.transform.scale(pygame.image.load(icon), (40, 40))
                if os.path.exists(os.path.join("res/icons/", icon)):
                    return pygame.transform.scale(pygame.image.load(os.path.join("res/icons/", icon)), (40, 40))
                if os.path.exists(os.path.join(folder, icon)):
                    return pygame.transform.scale(pygame.image.load(os.path.join(folder, icon)), (40, 40))
                return pygame.image.load(os.path.join(self.rootPath, self.icons["unknown"]))

        @staticmethod
        def loadFromFile(path):
            f = open(path, "rU")
            icondata = json.load(f)
            toreturn = GUI.Icons()
            for key in dict(icondata).keys():
                toreturn.icons[key] = icondata.get(key)
            f.close()
            return toreturn

    class ColorPalette(object):
        def __init__(self):
            self.palette = {
                       "normal": {
                                  "background": (200, 200, 200),
                                  "item": (20, 20, 20),
                                  "accent": (100, 100, 200),
                                  "warning": (250, 160, 45),
                                  "error": (250, 50, 50)
                                  },
                       "dark": {
                                "background": (50, 50, 50),
                                "item": (220, 220, 220),
                                "accent": (50, 50, 150),
                                "warning": (200, 110, 0),
                                "error": (200, 0, 0)
                                },
                       "light": {
                                 "background": (250, 250, 250),
                                 "item": (50, 50, 50),
                                 "accent": (150, 150, 250),
                                 "warning": (250, 210, 95),
                                 "error": (250, 100, 100)
                                 }
                       }
            self.scheme = "normal"

        def getPalette(self):
            return self.palette

        def getScheme(self):
            return self.scheme

        def getColor(self, item):
            if item.find(":") == -1:
                return self.palette[self.scheme][item]
            else:
                split = item.split(":")
                cadd = lambda c, d: (c[0]+d[0], c[1]+d[1], c[2]+d[2])
                if split[0] == "darker":
                    return max(cadd(self.getColor(split[1]), (-20, -20, -20)), (0, 0, 0))
                if split[0] == "dark":
                    return max(cadd(self.getColor(split[1]), (-40, -40, -40)), (0, 0, 0))
                if split[0] == "lighter":
                    return min(cadd(self.getColor(split[1]), (20, 20, 20)), (250, 250, 250))
                if split[0] == "light":
                    return min(cadd(self.getColor(split[1]), (40, 40, 40)), (250, 250, 250))
                if split[0] == "transparent":
                    return self.getColor(split[1]) + (int(split[2].rstrip("%"))/100,)

        def __getitem__(self, item):
            return self.getColor(item)

        def setScheme(self, scheme="normal"):
            self.scheme = scheme

        @staticmethod
        def loadFromFile(path):
            f = open(path, "rU")
            colordata = json.load(f)
            toreturn = GUI.ColorPalette()
            for key in dict(colordata).keys():
                toreturn.palette[key] = colordata.get(key)
            f.close()
            return toreturn

        @staticmethod
        def HTMLToRGB(colorstring):
            colorstring = colorstring.strip()
            if colorstring[0] == '#': colorstring = colorstring[1:]
            if len(colorstring) != 6:
                raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
            r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
            r, g, b = [int(n, 16) for n in (r, g, b)]
            return (r, g, b)

        @staticmethod
        def RGBToHTMLColor(rgb_tuple):
            hexcolor = '#%02x%02x%02x' % rgb_tuple
            return hexcolor

    class LongClickEvent(object):
        def __init__(self, mouseDown):
            self.mouseDown = mouseDown
            self.mouseDownTime = datetime.now()
            self.mouseUp = None
            self.mouseUpTime = None
            self.intermediatePoints = []
            self.pos = self.mouseDown.pos

        def intermediateUpdate(self, mouseMove):
            if self.mouseUp == None and (len(self.intermediatePoints) == 0 or mouseMove.pos != self.intermediatePoints[-1]):
                self.intermediatePoints.append(mouseMove.pos)

        def end(self, mouseUp):
            self.mouseUp = mouseUp
            self.mouseUpTime = datetime.now()
            self.pos = self.mouseUp.pos

        def getLatestUpdate(self):
            if len(self.intermediatePoints) == 0: return self.pos
            else: return self.intermediatePoints[len(self.intermediatePoints) - 1]

        def checkValidLongClick(self, time=300): #Checks timestamps against parameter (in milliseconds)
            delta = self.mouseUpTime - self.mouseDownTime
            return (delta.microseconds / 1000) >= time

    class IntermediateUpdateEvent(object):
        def __init__(self, pos, src):
            self.pos = pos
            self.sourceEvent = src

    class EventQueue(object):
        def __init__(self):
            self.events = []

        def check(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    State.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.events.append(GUI.LongClickEvent(event))
                if event.type == pygame.MOUSEMOTION and len(self.events) > 0 and isinstance(self.events[len(self.events)-1], GUI.LongClickEvent):
                    self.events[len(self.events)-1].intermediateUpdate(event)
                if event.type == pygame.MOUSEBUTTONUP and len(self.events) > 0 and isinstance(self.events[len(self.events)-1], GUI.LongClickEvent):
                    self.events[len(self.events)-1].end(event)
                    if not self.events[len(self.events)-1].checkValidLongClick():
                        self.events[len(self.events)-1] = self.events[len(self.events)-1].mouseUp

        def getLatest(self):
            if len(self.events) == 0: return None
            return self.events.pop()

        def removeEvent(self, ev):
            if ev in self.events:
                self.events.remove(ev)

        def getLatestComplete(self):
            if len(self.events) == 0: return None
            p = len(self.events) - 1
            while p >= 0:
                event = self.events[p]
                if isinstance(event, GUI.LongClickEvent):
                    if event.mouseUp != None:
                        return self.events.pop(p)
                    else:
                        return GUI.IntermediateUpdateEvent(self.events[len(self.events) - 1].getLatestUpdate(), self.events[len(self.events) - 1])
                else:
                    return self.events.pop(p)
                p -= 1

        def clear(self):
            self.events = []

    class Component(object):
        def __init__(self, position, **data):
            self.position = list(deepcopy(position))
            self.eventBindings = {}
            self.eventData = {}
            self.data = data
            self.surface = data.get("surface", None)
            self.border = 0
            self.borderColor = (0, 0, 0)
            self.resizable = data.get("resizable", False)
            self.originals = [list(deepcopy(position)),
                              data.get("width", data["surface"].get_width() if data.get("surface", False) != False else 0),
                              data.get("height", data["surface"].get_height() if data.get("surface", False) != False else 0)
                              ]
            self.width = self.originals[1]
            self.height = self.originals[2]
            self.computedWidth = 0
            self.computedHeight = 0
            self.computedPosition = [0, 0]
            self.rect = pygame.Rect(self.computedPosition, (self.computedWidth, self.computedHeight))
            self.setDimensions()
            self.eventBindings["onClick"] = data.get("onClick", None)
            self.eventBindings["onLongClick"] = data.get("onLongClick", None)
            self.eventBindings["onIntermediateUpdate"] = data.get("onIntermediateUpdate", None)
            self.eventData["onClick"] = data.get("onClickData", None)
            self.eventData["onIntermediateUpdate"] = data.get("onIntermediateUpdateData", None)
            self.eventData["onLongClick"] = data.get("onLongClickData", None)
            if "border" in data:
                self.border = int(data["border"])
                self.borderColor = data.get("borderColor", State.instance.getColorPalette().getColor("item"))
            self.innerClickCoordinates = (-1, -1)
            self.innerOffset = [0, 0]
            self.internalClickOverrides = {}

        def _percentToPix(self, value, scale):
            return int(int(value.rstrip("%")) * scale)

        def setDimensions(self):
            old_surface = self.surface.copy() if self.surface != None else None
            if self.data.get("fixedSize", False):
                self.computedWidth = self.data.get("width")
                self.computedHeight = self.data.get("height")
                self.rect = pygame.Rect(self.computedPosition, (self.computedWidth, self.computedHeight))
                self.surface = pygame.Surface((self.computedWidth, self.computedHeight), pygame.SRCALPHA)
                if old_surface != None: self.surface.blit(old_surface, (0, 0))
                return
            appc = State.instance.getActiveApplication().ui
            #Compute Position
            if type(self.position[0]) == str:
                self.computedPosition[0] = self._percentToPix(self.position[0], (State.instance.getActiveApplication().ui.width/100.0))
            else:
                if self.resizable:
                    self.computedPosition[0] = int(self.position[0] * appc.scaleX)
                else:
                    self.computedPosition[0] = int(self.position[0])
            if type(self.position[1]) == str:
                self.computedPosition[1] = self._percentToPix(self.position[1], (State.instance.getActiveApplication().ui.height/100.0))
            else:
                if self.resizable:
                    self.computedPosition[1] = int(self.position[1] * appc.scaleY)
                else:
                    self.computedPosition[1] = int(self.position[1])

            #Compute Width and Height
            if type(self.width) == str:
                self.computedWidth = self._percentToPix(self.width, (State.instance.getActiveApplication().ui.width/100.0))
            else:
                if self.resizable:
                    self.computedWidth = int(self.width * appc.scaleX)
                else:
                    self.computedWidth = int(self.width)
            if type(self.height) == str:
                self.computedHeight = self._percentToPix(self.height, (State.instance.getActiveApplication().ui.height/100.0))
            else:
                if self.resizable:
                    self.computedHeight = int(self.height * appc.scaleY)
                else:
                    self.computedHeight = int(self.height)

            #print "Computed to: " + str(self.computedPosition) + ", " + str(self.computedWidth) + "x" + str(self.computedHeight) + ", " + str(self.resizable)
            self.rect = pygame.Rect(self.computedPosition, (self.computedWidth, self.computedHeight))
            self.surface = pygame.Surface((self.computedWidth, self.computedHeight), pygame.SRCALPHA)
            if old_surface != None: self.surface.blit(old_surface, (0, 0))

        def onClick(self):
            if "onClick" in self.internalClickOverrides:
                self.internalClickOverrides["onClick"][0](*self.internalClickOverrides["onClick"][1])
            if self.eventBindings["onClick"]:
                if self.eventData["onClick"]:
                    self.eventBindings["onClick"](*self.eventData["onClick"])
                else:
                    self.eventBindings["onClick"]()

        def onLongClick(self):
            if "onLongClick" in self.internalClickOverrides:
                self.internalClickOverrides["onLongClick"][0](*self.internalClickOverrides["onLongClick"][1])
            if self.eventBindings["onLongClick"]:
                if self.eventData["onLongClick"]:
                    self.eventBindings["onLongClick"](*self.eventData["onLongClick"])
                else:
                    self.eventBindings["onLongClick"]()

        def onIntermediateUpdate(self):
            if "onIntermediateUpdate" in self.internalClickOverrides:
                self.internalClickOverrides["onIntermediateUpdate"][0](*self.internalClickOverrides["onIntermediateUpdate"][1])
            if self.eventBindings["onIntermediateUpdate"]:
                    if self.eventData["onIntermediateUpdate"]:
                        self.eventBindings["onIntermediateUpdate"](*self.eventData["onIntermediateUpdate"])
                    else:
                        self.eventBindings["onIntermediateUpdate"]()

        def setOnClick(self, mtd, data=()):
            self.eventBindings["onClick"] = mtd
            self.eventData["onClick"] = data

        def setOnLongClick(self, mtd, data=()):
            self.eventBindings["onLongClick"] = mtd
            self.eventData["onLong"] = data

        def setOnIntermediateUpdate(self, mtd, data=()):
            self.eventBindings["onIntermediateUpdate"] = mtd
            self.eventData["onIntermediateUpdate"] = data

        def render(self, largerSurface):
            recompute = False
            if self.position != self.originals[0]:
                self.originals[0] = list(deepcopy(self.position))
                recompute = True
            if self.width != self.originals[1]:
                self.originals[1] = self.width
                recompute = True
            if self.height != self.originals[2]:
                self.originals[2] = self.height
                recompute = True
            if recompute:
                self.setDimensions()
            if self.border > 0:
                pygame.draw.rect(self.surface, self.borderColor, [0, 0, self.computedWidth, self.computedHeight], self.border)
            if not self.surface.get_locked():
                largerSurface.blit(self.surface, self.computedPosition)

        def refresh(self):
            self.setDimensions()

        def getInnerClickCoordinates(self):
            return self.innerClickCoordinates

        def checkClick(self, mouseEvent, offsetX=0, offsetY=0):
            self.innerOffset = [offsetX, offsetY]
            adjusted = [mouseEvent.pos[0] - offsetX, mouseEvent.pos[1] - offsetY]
            if adjusted[0] < 0 or adjusted[1] < 0: return False
            if self.rect.collidepoint(adjusted):
                self.innerClickCoordinates = tuple(adjusted)
                if not isinstance(mouseEvent, GUI.IntermediateUpdateEvent):
                    self.data["lastEvent"] = mouseEvent
                return True
            return False

        def setPosition(self, pos):
            self.position = list(pos)[:]
            self.refresh()

        def setSurface(self, new_surface, override_dimensions=False):
            if new_surface.get_width() != self.computedWidth or new_surface.get_height() != self.computedHeight:
                if override_dimensions:
                    self.width = new_surface.get_width()
                    self.height = new_surface.get_height()
                else:
                    new_surface = pygame.transform.scale(new_surface, (self.computedWidth, self.computedHeight))
            self.surface = new_surface

        @staticmethod
        def default(*items):
            if len(items)%2 != 0: return items
            values = []
            p = 0
            while p < len(items):
                values.append(items[p+1] if items[p] == DEFAULT else items[p])
                p += 2
            return tuple(values)

    class Container(Component):
        def __init__(self, position, **data):
            super(GUI.Container, self).__init__(position, **data)
            self.transparent = False
            self.backgroundColor = (0, 0, 0)
            self.childComponents = []
            self.SKIP_CHILD_CHECK = False
            self.transparent = data.get("transparent", False)
            self.backgroundColor = data.get("color", State.instance.getColorPalette().getColor("background"))
            if "children" in data: self.childComponents = data["children"]

        def addChild(self, component):
            if self.resizable and "resizeble" not in component.data:
                component.resizable = True
                component.refresh()
            self.childComponents.append(component)

        def addChildren(self, *children):
            for child in children:
                self.addChild(child)

        def removeChild(self, component):
            self.childComponents.remove(component)

        def clearChildren(self):
            for component in self.childComponents:
                self.removeChild(component)
            self.childComponents = []

        def getClickedChild(self, mouseEvent, offsetX=0, offsetY=0):
            currChild = len(self.childComponents)
            while currChild > 0:
                currChild -= 1
                child = self.childComponents[currChild]
                if "SKIP_CHILD_CHECK" in child.__dict__:
                    if child.SKIP_CHILD_CHECK:
                        if child.checkClick(mouseEvent, offsetX + self.computedPosition[0], offsetY + self.computedPosition[1]):
                            return child
                        else:
                            continue
                    else:
                        subCheck = child.getClickedChild(mouseEvent, offsetX + self.computedPosition[0], offsetY + self.computedPosition[1])
                        if subCheck == None: continue
                        return subCheck
                else:
                    if child.checkClick(mouseEvent, offsetX + self.computedPosition[0], offsetY + self.computedPosition[1]):
                        return child
            if self.checkClick(mouseEvent, offsetX, offsetY):
                return self
            return None

        def getChildAt(self, position):
            for child in self.childComponents:
                if child.computedPosition == list(position):
                    return child
            return None

        def render(self, largerSurface):
            if self.surface.get_locked(): return
            if not self.transparent:
                self.surface.fill(self.backgroundColor)
            else:
                self.surface.fill((0, 0, 0, 0))
            for child in self.childComponents:
                child.render(self.surface)
            super(GUI.Container, self).render(largerSurface)

        def refresh(self, children=True):
            super(GUI.Container, self).refresh()
            if children:
                for child in self.childComponents:
                    child.refresh()

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
                self.scaleX = (State.instance.getGUI().width / dW)
                self.scaleY = (State.instance.getGUI().height / dH)
                super(GUI.AppContainer, self).__init__((0, 0), width=screen.get_width(), height=screen.get_height()-40,
                                                       resizable=True, fixedSize=True)
            else:
                super(GUI.AppContainer, self).__init__((0, 0), width=screen.get_width(), height=screen.get_height()-40,
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
                super(GUI.AppContainer, self).render(self.surface)
            else:
                self.surface.blit(self.dialogScreenFreezes[0], (0, 0))
                self.dialogs[0].baseContainer.render(self.surface)
            screen.blit(self.surface, self.position)

        def refresh(self):
            self.width = screen.get_width()
            self.height = screen.get_height() - 40
            if self.application.parameters.get("resize", False):
                dW = float(self.application.parameters.get("size", {"width": 240}).get("width"))
                dH = float(self.application.parameters.get("size", {"height": 320}).get("height"))
                self.scaleX = 1.0 * (State.instance.getGUI().width / dW)
                self.scaleY = 1.0 * (State.instance.getGUI().height / dH)
            #super(GUI.AppContainer, self).refresh()

    class Text(Component):
        def __init__(self, position, text, color=DEFAULT, size=DEFAULT, **data):
            #Defaults are "item" and 14.
            color, size = GUI.Component.default(color, State.instance.getColorPalette().getColor("item"), size, 14)
            self.text = text
            self._originalText = text
            self.size = size
            self.color = color
            self.font = data.get("font", State.instance.getFont())
            self.use_freetype = data.get("freetype", False)
            self.responsive_width = data.get("responsive_width", True)
            data["surface"] = self.getRenderedText()
            super(GUI.Text, self).__init__(position, **data)

        def getRenderedText(self):
            if self.use_freetype:
                return self.font.get(self.size, True).render(str(self.text), self.color)
            return self.font.get(self.size).render(self.text, 1, self.color)

        def refresh(self):
            self.surface = self.getRenderedText()

        def render(self, largerSurface):
            if self.text != self._originalText:
                self.setText(self.text)
            super(GUI.Text, self).render(largerSurface)

        def setText(self, text):
            self.text = text if type(text) == str or type(text) == unicode else str(text)
            self._originalText = self.text
            self.refresh()
            if self.responsive_width:
                self.width = self.surface.get_width()
                self.height = self.surface.get_height()
            self.setDimensions()

    class MultiLineText(Component):
        @staticmethod
        def render_textrect(string, font, rect, text_color, background_color, justification, use_ft):
            final_lines = []
            requested_lines = string.splitlines()
            err = None
            for requested_line in requested_lines:
                if font.size(requested_line)[0] > rect.width:
                    words = requested_line.split(' ')
                    for word in words:
                        if font.size(word)[0] >= rect.width:
                            #print "The word " + word + " is too long to fit in the rect passed."
                            err = 0
                    accumulated_line = ""
                    for word in words:
                        test_line = accumulated_line + word + " "
                        if font.size(test_line)[0] < rect.width:
                            accumulated_line = test_line
                        else:
                            final_lines.append(accumulated_line)
                            accumulated_line = word + " "
                    final_lines.append(accumulated_line)
                else:
                    final_lines.append(requested_line)
            surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            surface.fill(background_color)
            accumulated_height = 0
            for line in final_lines:
                if accumulated_height + font.size(line)[1] >= rect.height:
                    err = 1
                if line != "":
                    tempsurface = None
                    if use_ft:
                        tempsurface = font.render(line, text_color)
                    else:
                        tempsurface = font.render(line, 1, text_color)
                    if justification == 0:
                        surface.blit(tempsurface, (0, accumulated_height))
                    elif justification == 1:
                        surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
                    elif justification == 2:
                        surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
                    else:
                        print "Invalid justification argument: " + str(justification)
                        err = 2
                accumulated_height += font.size(line)[1]
            return (surface, err, final_lines)

        def __init__(self, position, text, color=DEFAULT, size=DEFAULT, justification=DEFAULT, **data):
            #Defaults are "item", and 0 (left).
            color, size, justification = GUI.Component.default(color, State.instance.getColorPalette().getColor("item"), size, 14,
                                                         justification, 0)
            self.justification = justification
            self.color = color
            self.size = size
            self.text = text if type(text) == str or type(text) == unicode else str(text)
            self.textSurface = None
            self.font = data.get("font", State.instance.getFont())
            self.use_freetype = data.get("freetype", False)
            super(GUI.MultiLineText, self).__init__(position, **data)
            self.refresh()
            if self.width > State.instance.getGUI().width:
                self.width = State.instance.getGUI().width

        def getRenderedText(self):
            return GUI.MultiLineText.render_textrect(self.text, self.font.get(self.size, self.use_freetype), pygame.Rect(0, 0, self.computedWidth, self.computedHeight),
                                                     self.color, (0, 0, 0, 0), self.justification, self.use_freetype)[0]

        def refresh(self):
            super(GUI.MultiLineText, self).refresh()
            self.textSurface = self.getRenderedText()
            self.surface.fill((0, 0, 0, 0))
            self.surface.blit(self.textSurface, (0, 0))

        def setText(self, text):
            self.text = text if type(text) == str or type(text) == unicode else str(text)
            self.setDimensions()
            self.refresh()

    class ExpandingMultiLineText(MultiLineText):
        def __init__(self, position, text, color=DEFAULT, size=DEFAULT, justification=DEFAULT, lineHeight=DEFAULT, **data):
            #Defaults are "item", 14, 0, and 16.
            color, size, justification, lineHeight = GUI.Component.default(color, State.instance.getColorPalette().getColor("item"),
                                                                           size, 14,
                                                                           justification, 0,
                                                                           lineHeight, 16)
            self.lineHeight = lineHeight
            self.linkedScroller = data.get("scroller", None)
            self.textLines = []
            super(GUI.ExpandingMultiLineText, self).__init__(position, text, color, size, justification, **data)
            self.height = self.computedHeight
            self.refresh()

        def getRenderedText(self):
            fits = False
            surf = None
            while not fits:
                d = GUI.MultiLineText.render_textrect(self.text, self.font.get(self.size), pygame.Rect(self.computedPosition[0], self.computedPosition[1], self.computedWidth, self.height),
                                                      self.color, (0, 0, 0, 0), self.justification, self.use_freetype)
                surf = d[0]
                fits = d[1] != 1
                self.textLines = d[2]
                if not fits:
                    self.height += self.lineHeight
                    self.computedHeight = self.height
            self.setDimensions()
            #if self.linkedScroller != None:
            #    self.linkedScroller.refresh(False)
            return surf

    class Image(Component):
        def __init__(self, position, **data):
            self.path = ""
            self.originalSurface = None
            self.transparent = True
            self.resize_image = data.get("resize_image", True)
            if "path" in data:
                self.path = data["path"]
            else:
                self.path = "surface"
            if "surface" not in data:
                data["surface"] = pygame.image.load(data["path"])
            self.originalSurface = data["surface"]
            self.originalWidth = self.originalSurface.get_width()
            self.originalHeight = self.originalSurface.get_height()
            super(GUI.Image, self).__init__(position, **data)
            if self.resize_image: self.setSurface(pygame.transform.scale(self.originalSurface, (self.computedWidth, self.computedHeight)))

        def setImage(self, **data):
            if "path" in data:
                self.path = data["path"]
            else:
                self.path = "surface"
            if "surface" not in data:
                data["surface"] = pygame.image.load(data["path"])
            self.originalSurface = data["surface"]
            if data.get("resize", False):
                self.width = self.originalSurface.get_width()
                self.height = self.originalSurface.get_height()
            self.refresh()

        def refresh(self):
            if self.resize_image:
                self.setSurface(pygame.transform.scale(self.originalSurface, (self.computedWidth, self.computedHeight)))
            else:
                super(GUI.Image, self).refresh()

    class Slider(Component):
        def __init__(self, position, initialPct=0, **data):
            super(GUI.Slider, self).__init__(position, **data)
            self.percent = initialPct
            self.backgroundColor = data.get("backgroundColor", State.instance.getColorPalette().getColor("background"))
            self.color = data.get("color", State.instance.getColorPalette().getColor("item"))
            self.sliderColor = data.get("sliderColor", State.instance.getColorPalette().getColor("accent"))
            self.onChangeMethod = data.get("onChange", Application.dummy)
            self.refresh()

        def onChange(self):
            self.onChangeMethod(self.percent)

        def setPercent(self, percent):
            self.percent = percent

        def refresh(self):
            self.percentPixels = self.computedWidth / 100.0
            super(GUI.Slider, self).refresh()

        def render(self, largerSurface):
            self.surface.fill(self.backgroundColor)
            pygame.draw.rect(self.surface, self.color, [0, self.computedHeight/4, self.computedWidth, self.computedHeight/2])
            pygame.draw.rect(self.surface, self.sliderColor, [(self.percent*self.percentPixels)-15, 0, 30, self.computedHeight])
            super(GUI.Slider, self).render(largerSurface)

        def checkClick(self, mouseEvent, offsetX=0, offsetY=0):
            isClicked = super(GUI.Slider, self).checkClick(mouseEvent, offsetX, offsetY)
            if isClicked:
                self.percent = ((mouseEvent.pos[0] - offsetX - self.computedPosition[0])) / self.percentPixels
                if self.percent > 100.0: self.percent = 100.0
                self.onChange()
            return isClicked

        def getPercent(self):
            return self.percent

    class Button(Container):
        def __init__(self, position, text, bgColor=DEFAULT, textColor=DEFAULT, textSize=DEFAULT, **data):
            #Defaults are "darker:background", "item", and 14.
            bgColor, textColor, textSize = GUI.Component.default(bgColor, State.instance.getColorPalette().getColor("darker:background"),
                                  textColor, State.instance.getColorPalette().getColor("item"),
                                  textSize, 14)
            self.textComponent = GUI.Text((0, 0), text, textColor, textSize, font=data.get("font", State.instance.getFont()), freetype=data.get("freetype", False))
            self.paddingAmount = data.get("padding", 5)
            if "width" not in data: data["width"] = self.textComponent.computedWidth + (2 * self.paddingAmount)
            if "height" not in data: data["height"] = self.textComponent.computedHeight + (2 * self.paddingAmount)
            super(GUI.Button, self).__init__(position, **data)
            self.SKIP_CHILD_CHECK = True
            self.textComponent.setPosition(GUI.getCenteredCoordinates(self.textComponent, self))
            self.backgroundColor = bgColor
            self.addChild(self.textComponent)

        def setDimensions(self):
            super(GUI.Button, self).setDimensions()
            self.textComponent.setPosition(GUI.getCenteredCoordinates(self.textComponent, self))

        def setText(self, text):
            self.textComponent.setText(text)
            self.setDimensions()

        def render(self, largerSurface):
            super(GUI.Button, self).render(largerSurface)

        def getClickedChild(self, mouseEvent, offsetX=0, offsetY=0):
            if self.checkClick(mouseEvent, offsetX, offsetY):
                return self
            return None

    class Checkbox(Component):
        def __init__(self, position, checked=False, **data):
            if "border" not in data:
                data["border"] = 2
                data["borderColor"] = State.instance.getColorPalette().getColor("item")
            super(GUI.Checkbox, self).__init__(position, **data)
            self.backgroundColor = data.get("backgroundColor", State.instance.getColorPalette().getColor("background"))
            self.checkColor = data.get("checkColor", State.instance.getColorPalette().getColor("accent"))
            self.checkWidth = data.get("checkWidth", self.computedHeight/4)
            self.checked = checked
            self.internalClickOverrides["onClick"] = [self.check, ()]

        def getChecked(self):
            return self.checked

        def check(self, state="toggle"):
            if state == "toggle":
                self.checked = not self.checked
            else:
                self.checked = bool(state)

        def render(self, largerSurface):
            self.surface.fill(self.backgroundColor)
            if self.checked:
                pygame.draw.lines(self.surface, self.checkColor, False, [(0, self.computedHeight/2),
                                                                         (self.computedWidth/2, self.computedHeight-self.checkWidth/2),
                                                                         (self.computedWidth, 0)], self.checkWidth)
            super(GUI.Checkbox, self).render(largerSurface)

    class Switch(Component):
        def __init__(self, position, on=False, **data):
            if "border" not in data:
                data["border"] = 2
                data["borderColor"] = State.instance.getColorPalette().getColor("item")
            super(GUI.Switch, self).__init__(position, **data)
            self.backgroundColor = data.get("backgroundColor", State.instance.getColorPalette().getColor("background"))
            self.onColor = data.get("onColor", State.instance.getColorPalette().getColor("accent"))
            self.offColor = data.get("offColor", State.instance.getColorPalette().getColor("dark:background"))
            self.on = on
            self.internalClickOverrides["onClick"] = [self.switch, ()]

        def getChecked(self):
            return self.checked

        def switch(self, state="toggle"):
            if state == "toggle":
                self.on = not self.on
            else:
                self.on = bool(state)

        def render(self, largerSurface):
            self.surface.fill(self.backgroundColor)
            if self.on:
                pygame.draw.rect(self.surface, self.onColor, [self.computedWidth/2, 0, self.computedWidth/2, self.computedHeight])
            else:
                pygame.draw.rect(self.surface, self.offColor, [0, 0, self.computedWidth/2, self.computedHeight])
            pygame.draw.circle(self.surface, State.instance.getColorPalette().getColor("item"), (self.computedWidth/4, self.computedHeight/2), self.computedHeight/4, 2)
            pygame.draw.line(self.surface, State.instance.getColorPalette().getColor("item"), (3*(self.computedWidth/4), self.computedHeight/4),
                             (3*(self.computedWidth/4), 3*(self.computedHeight/4)), 2)
            super(GUI.Switch, self).render(largerSurface)

    class Canvas(Component):
        def __init__(self, position, **data):
            super(GUI.Canvas, self).__init__(position, **data)

    class KeyboardButton(Container):
        def __init__(self, position, symbol, altSymbol, **data):
            if "border" not in data:
                data["border"] = 1
                data["borderColor"] = State.instance.getColorPalette().getColor("item")
            super(GUI.KeyboardButton, self).__init__(position, **data)
            self.SKIP_CHILD_CHECK = True
            self.primaryTextComponent = GUI.Text((1, 0), symbol, State.instance.getColorPalette().getColor("item"), 20, font=data.get("font", State.instance.getTypingFont()))
            self.secondaryTextComponent = GUI.Text((self.computedWidth-8, 0), altSymbol, State.instance.getColorPalette().getColor("item"), 10, font=data.get("font", State.instance.getTypingFont()))
            self.primaryTextComponent.setPosition([GUI.getCenteredCoordinates(self.primaryTextComponent, self)[0]-6, self.computedHeight-self.primaryTextComponent.computedHeight-1])
            self.addChild(self.primaryTextComponent)
            self.addChild(self.secondaryTextComponent)
            self.blinkTime = 0
            self.internalClickOverrides["onClick"] = (self.registerBlink, ())
            self.internalClickOverrides["onLongClick"] = (self.registerBlink, (True,))

        def registerBlink(self, lp=False):
            self.blinkTime = State.instance.getGUI().update_interval / 6
            self.primaryTextComponent.color = State.instance.getColorPalette().getColor("background")
            self.secondaryTextComponent.color = State.instance.getColorPalette().getColor("background")
            self.backgroundColor = State.instance.getColorPalette().getColor("accent" if lp else "item")
            self.refresh()

        def getClickedChild(self, mouseEvent, offsetX=0, offsetY=0):
            if self.checkClick(mouseEvent, offsetX, offsetY):
                return self
            return None

        def render(self, largerSurface):
            if self.blinkTime >= 0:
                self.blinkTime -= 1
                if self.blinkTime < 0:
                    self.primaryTextComponent.color = State.instance.getColorPalette().getColor("item")
                    self.secondaryTextComponent.color = State.instance.getColorPalette().getColor("item")
                    self.backgroundColor = State.instance.getColorPalette().getColor("background")
                    self.refresh()
            super(GUI.KeyboardButton, self).render(largerSurface)

    class TextEntryField(Container):
        def __init__(self, position, initialText="", **data):
            if "border" not in data:
                data["border"] = 1
                data["borderColor"] = State.instance.getColorPalette().getColor("accent")
            if "textColor" not in data:
                data["textColor"] = State.instance.getColorPalette().getColor("item")
            if "blink" in data:
                self.blinkInterval = data["blink"]
            else:
                self.blinkInterval = 500
            self.doBlink = True
            self.blinkOn = False
            self.lastBlink = datetime.now()
            self.indicatorPosition = len(initialText)
            self.indicatorPxPosition = 0
            super(GUI.TextEntryField, self).__init__(position, **data)
            self.SKIP_CHILD_CHECK = True
            self.textComponent = GUI.Text((2, 0), initialText, data["textColor"], 16, font=State.instance.getTypingFont())
            self.updateOverflow()
            self.lastClickCoord = None
            self.textComponent.position[1] = GUI.getCenteredCoordinates(self.textComponent, self)[1]
            self.addChild(self.textComponent)
            self.MULTILINE = None
            self.internalClickOverrides["onClick"] = (self.activate, ())
            self.internalClickOverrides["onIntermediateUpdate"] = (self.dragScroll, ())

        def clearScrollParams(self):
            self.lastClickCoord = None

        def dragScroll(self):
            if self.lastClickCoord != None and self.overflow > 0:
                ydist = self.innerClickCoordinates[1] - self.lastClickCoord[1]
                self.overflow -= ydist
                if self.overflow > 0 and self.overflow + self.computedWidth < self.textComponent.computedWidth:
                    self.textComponent.position[0] = 2 - self.overflow
                else:
                    self.textComponent.position[0] = 2
            self.lastClickCoord = self.innerClickCoordinates

        def getPxPosition(self, fromPos=DEFAULT):
            return State.instance.getTypingFont().get(16).size(self.textComponent.text[:(self.indicatorPosition if fromPos==DEFAULT else fromPos)])[0]

        def activate(self):
            self.clearScrollParams()
            self.updateOverflow()
            State.instance.setKeyboard(GUI.Keyboard(self))
            if self.MULTILINE != None:
                for f in self.MULTILINE.textFields: f.doBlink = False
            self.doBlink = True
            mousePos = self.innerClickCoordinates[0] - self.innerOffset[0]
            if mousePos > self.textComponent.computedWidth:
                self.indicatorPosition = len(self.textComponent.text)
            else:
                prevWidth = 0
                for self.indicatorPosition in range(len(self.textComponent.text)):
                    currWidth = self.getPxPosition(self.indicatorPosition)
                    if mousePos >= prevWidth and mousePos <= currWidth:
                        self.indicatorPosition -= 1
                        break
                    prevWidth = currWidth
            State.instance.getKeyboard().active = True
            self.indicatorPxPosition = self.getPxPosition()
            if self.MULTILINE:
                self.MULTILINE.setCurrent(self)
            return self

        def updateOverflow(self):
            self.overflow = max(self.textComponent.computedWidth - (self.computedWidth - 4), 0)
            if self.overflow > 0:
                self.textComponent.position[0] = 2 - self.overflow
            else:
                self.textComponent.position[0] = 2

        def appendChar(self, char):
            if self.indicatorPosition == len(self.textComponent.text)-1:
                self.textComponent.text += char
            else:
                self.textComponent.text = self.textComponent.text[:self.indicatorPosition] + char + self.textComponent.text[self.indicatorPosition:]
            self.textComponent.refresh()
            self.indicatorPosition += len(char)
            self.updateOverflow()
            if self.MULTILINE != None:
                if self.overflow > 0:
                    newt = self.textComponent.text[max(self.textComponent.text.rfind(" "),
                                                       self.textComponent.text.rfind("-")):]
                    self.textComponent.text = self.textComponent.text.rstrip(newt)
                    self.MULTILINE.addField(newt)
                    self.MULTILINE.wrappedLines.append(self.MULTILINE.currentField)
                    #if self.MULTILINE.currentField == len(self.MULTILINE.textFields)-1:
                    #    self.MULTILINE.addField(newt)
                    #else:
                    #    self.MULTILINE.prependToNextField(newt)
                    self.textComponent.refresh()
                    self.updateOverflow()
            self.indicatorPxPosition = self.getPxPosition()

        def backspace(self):
            if self.indicatorPosition >= 1:
                self.indicatorPosition -= 1
                self.indicatorPxPosition = self.getPxPosition()
                self.textComponent.text = self.textComponent.text[:self.indicatorPosition] + self.textComponent.text[self.indicatorPosition+1:]
                self.textComponent.refresh()
            else:
                if self.MULTILINE != None and self.MULTILINE.currentField > 0:
                    self.MULTILINE.removeField(self)
                    self.MULTILINE.textFields[self.MULTILINE.currentField-1].appendChar(self.textComponent.text.strip(" "))
                    self.MULTILINE.textFields[self.MULTILINE.currentField-1].activate()
            self.updateOverflow()

        def delete(self):
            if self.indicatorPosition < len(self.textComponent.text):
                self.textComponent.text = self.textComponent.text[:self.indicatorPosition] + self.textComponent.text[self.indicatorPosition+1:]
                self.textComponent.refresh()
            self.updateOverflow()
            if self.MULTILINE != None:
                self.appendChar(self.MULTILINE.getDeleteChar())

        def getText(self):
            return self.textComponent.text

        def refresh(self):
            self.updateOverflow()
            super(GUI.TextEntryField, self).refresh()

        def render(self, largerSurface):
            if not self.transparent:
                self.surface.fill(self.backgroundColor)
            else:
                self.surface.fill((0, 0, 0, 0))
            for child in self.childComponents:
                child.render(self.surface)
            if self.doBlink:
                if ((datetime.now() - self.lastBlink).microseconds / 1000) >= self.blinkInterval:
                    self.lastBlink = datetime.now()
                    self.blinkOn = not self.blinkOn
                if self.blinkOn:
                    pygame.draw.rect(self.surface, self.textComponent.color, [self.indicatorPxPosition, 2, 2, self.computedHeight-4])
            super(GUI.Container, self).render(largerSurface)

        def getClickedChild(self, mouseEvent, offsetX=0, offsetY=0):
            if self.checkClick(mouseEvent, offsetX, offsetY):
                return self
            return None

    class PagedContainer(Container):
        def __init__(self, position, **data):
            super(GUI.PagedContainer, self).__init__(position, **data)
            self.pages = data.get("pages", [])
            self.currentPage = 0
            self.hideControls = data.get("hideControls", False)
            self.pageControls = GUI.Container((0, self.computedHeight-20), color=State.instance.getColorPalette().getColor("background"), width=self.computedWidth, height=20)
            self.pageLeftButton = GUI.Button((0, 0), " < ", State.instance.getColorPalette().getColor("item"), State.instance.getColorPalette().getColor("accent"),
                                            16, width=40, height=20, onClick=self.pageLeft, onLongClick=self.goToPage)
            self.pageRightButton = GUI.Button((self.computedWidth-40, 0), " > ", State.instance.getColorPalette().getColor("item"), State.instance.getColorPalette().getColor("accent"),
                                            16, width=40, height=20, onClick=self.pageRight, onLongClick=self.goToLastPage)
            self.pageIndicatorText = GUI.Text((0, 0), str(self.currentPage + 1)+" of "+str(len(self.pages)), State.instance.getColorPalette().getColor("item"),
                                            16)
            self.pageHolder = GUI.Container((0, 0), color=State.instance.getColorPalette().getColor("background"), width=self.computedWidth, height=(self.computedHeight-20 if not self.hideControls else self.computedHeight))
            self.pageIndicatorText.position[0] = GUI.getCenteredCoordinates(self.pageIndicatorText, self.pageControls)[0]
            super(GUI.PagedContainer, self).addChild(self.pageHolder)
            self.pageControls.addChild(self.pageLeftButton)
            self.pageControls.addChild(self.pageIndicatorText)
            self.pageControls.addChild(self.pageRightButton)
            if not self.hideControls:
                super(GUI.PagedContainer, self).addChild(self.pageControls)

        def addPage(self, page):
            self.pages.append(page)
            self.pageIndicatorText.text = str(self.currentPage + 1)+" of "+str(len(self.pages))
            self.pageIndicatorText.refresh()

        def getPage(self, number):
            return self.pages[number]

        def pageLeft(self):
            if self.currentPage >= 1:
                self.goToPage(self.currentPage - 1)

        def pageRight(self):
            if self.currentPage < len(self.pages) - 1:
                self.goToPage(self.currentPage + 1)

        def goToPage(self, number=0):
            self.currentPage = number
            self.pageHolder.clearChildren()
            self.pageHolder.addChild(self.getPage(self.currentPage))
            self.pageIndicatorText.setText(str(self.currentPage + 1)+" of "+str(len(self.pages)))
            self.pageIndicatorText.refresh()

        def goToLastPage(self): self.goToPage(len(self.pages) - 1)

        def getLastPage(self):
            return self.pages[len(self.pages) - 1]

        def generatePage(self, **data):
            if "width" not in data: data["width"] = self.pageHolder.computedWidth
            if "height" not in data: data["height"] = self.pageHolder.computedHeight
            data["isPage"] = True
            return GUI.Container((0, 0), **data)

        def addChild(self, component):
            if self.pages == []:
                self.addPage(self.generatePage(color=self.backgroundColor, width=self.pageHolder.computedWidth, height=self.pageHolder.computedHeight))
            self.getLastPage().addChild(component)

        def removeChild(self, component):
            self.pages[self.currentPage].removeChild(component)
            childrenCopy = self.pages[self.currentPage].childComponents[:]
            for page in self.pages:
                for child in page.childComponents:
                    page.removeChild(child)
            for child in childrenCopy:
                self.addChild(child)

        def removePage(self, page):
            if type(page) == int:
                self.pages.pop(page)
            else:
                self.pages.remove(page)
            if self.currentPage >= len(self.pages):
                self.goToPage(self.currentPage - 1)

        def clearChildren(self):
            self.pages = []
            self.addPage(self.generatePage(color=self.backgroundColor))
            self.goToPage()

    class GriddedPagedContainer(PagedContainer):
        def __init__(self, position, rows=5, columns=4, **data):
            self.padding = 5
            if "padding" in data: self.padding = data["padding"]
            self.rows = rows
            self.columns = columns
            super(GUI.PagedContainer, self).__init__(position, **data)
            self.perRow = ((self.computedHeight-20)-(2*self.padding)) / rows
            self.perColumn = (self.computedWidth-(2*self.padding)) / columns
            super(GUI.GriddedPagedContainer, self).__init__(position, **data)

        def isPageFilled(self, number):
            if type(number) == int:
                return len(self.pages[number].childComponents) == (self.rows * self.columns)
            else:
                return len(number.childComponents) == (self.rows * self.columns)

        def addChild(self, component):
            if self.pages == [] or self.isPageFilled(self.getLastPage()):
                self.addPage(self.generatePage(color=self.backgroundColor))
            newChildPosition = [self.padding, self.padding]
            if self.getLastPage().childComponents == []:
                component.setPosition(newChildPosition)
                self.getLastPage().addChild(component)
                return
            lastChildPosition = self.getLastPage().childComponents[len(self.getLastPage().childComponents) - 1].computedPosition[:]
            if lastChildPosition[0] < self.padding + (self.perColumn * (self.columns - 1)):
                newChildPosition = [lastChildPosition[0]+self.perColumn, lastChildPosition[1]]
            else:
                newChildPosition = [self.padding, lastChildPosition[1]+self.perRow]
            component.setPosition(newChildPosition)
            self.getLastPage().addChild(component)

    class ListPagedContainer(PagedContainer):
        def __init__(self, position, **data):
            self.padding = data.get("padding", 0)
            self.margin = data.get("margin", 0)
            super(GUI.ListPagedContainer, self).__init__(position, **data)

        def getHeightOfComponents(self):
            height = self.padding
            if self.pages == []: return self.padding
            for component in self.getLastPage().childComponents:
                height += component.computedHeight + (2*self.margin)
            return height

        def addChild(self, component):
            componentHeight = self.getHeightOfComponents()
            if self.pages == [] or componentHeight + (component.computedHeight + 2*self.margin) + (2*self.padding) >= self.pageHolder.computedHeight:
                self.addPage(self.generatePage(color=self.backgroundColor))
                componentHeight = self.getHeightOfComponents()
            component.setPosition([self.padding, componentHeight])
            self.getLastPage().addChild(component)
            component.refresh()

        def removeChild(self, component):
            super(GUI.ListPagedContainer, self).removeChild(component)
            if self.pages[0].childComponents == []:
                self.removePage(0)
                self.goToPage()

    class ButtonRow(Container):
        def __init__(self, position, **data):
            self.padding = data.get("padding", 0)
            self.margin = data.get("margin", 0)
            super(GUI.ButtonRow, self).__init__(position, **data)

        def getLastComponent(self):
            if len(self.childComponents) > 0:
                return self.childComponents[len(self.childComponents) - 1]
            return None

        def addChild(self, component):
            component.height = self.computedHeight - (2*self.padding)
            last = self.getLastComponent()
            if last != None:
                component.setPosition([last.computedPosition[0]+last.computedWidth+self.margin, self.padding])
            else:
                component.setPosition([self.padding, self.padding])
            component.setDimensions()
            super(GUI.ButtonRow, self).addChild(component)

        def removeChild(self, component):
            super(GUI.ButtonRow, self).removeChild(component)
            childrenCopy = self.childComponents[:]
            self.clearChildren()
            for child in childrenCopy:
                self.addChild(child)

    class ScrollIndicator(Component):
        def __init__(self, scrollCont, position, color, **data):
            super(GUI.ScrollIndicator, self).__init__(position, **data)
            self.internalClickOverrides["onIntermediateUpdate"] = (self.dragScroll, ())
            self.internalClickOverrides["onClick"] = (self.clearScrollParams, ())
            self.internalClickOverrides["onLongClick"] = (self.clearScrollParams, ())
            self.scrollContainer = scrollCont
            self.color = color
            self.lastClickCoord = None

        def update(self):
            self.pct = 1.0 * self.scrollContainer.computedHeight / (self.scrollContainer.maxOffset - self.scrollContainer.minOffset)
            self.slide = -self.scrollContainer.offset*self.pct
            self.sih = self.pct * self.computedHeight

        def render(self, largerSurface):
            self.surface.fill(self.color)
            pygame.draw.rect(self.surface, State.instance.getColorPalette().getColor("accent"), [0, int(self.slide*(1.0*self.computedHeight/self.scrollContainer.computedHeight)), self.computedWidth, int(self.sih)])
            super(GUI.ScrollIndicator, self).render(largerSurface)

        def clearScrollParams(self):
            self.lastClickCoord = None

        def dragScroll(self):
            if self.lastClickCoord != None:
                ydist = self.innerClickCoordinates[1] - self.lastClickCoord[1]
                self.scrollContainer.scroll(ydist)
            self.lastClickCoord = self.innerClickCoordinates

    class ScrollableContainer(Container):
        def __init__(self, position, **data):
            self.scrollAmount = data.get("scrollAmount", State.instance.getGUI().height / 8)
            super(GUI.ScrollableContainer, self).__init__(position, **data)
            self.container = GUI.Container((0, 0), transparent=True, width=self.computedWidth-20, height=self.computedHeight)
            self.scrollBar = GUI.Container((self.computedWidth-20, 0), width=20, height=self.computedHeight)
            self.scrollUpBtn = GUI.Image((0, 0), path="res/scrollup.png", width=20, height=40,
                                         onClick=self.scroll, onClickData=(self.scrollAmount,))
            self.scrollDownBtn = GUI.Image((0, self.scrollBar.computedHeight-40), path="res/scrolldown.png", width=20, height=40,
                                         onClick=self.scroll, onClickData=(-self.scrollAmount,))
            self.scrollIndicator = GUI.ScrollIndicator(self, (0, 40), self.backgroundColor, width=20, height=self.scrollBar.computedHeight-80, border=1, borderColor=State.instance.getColorPalette().getColor("item"))
            if self.computedHeight >= 120:
                self.scrollBar.addChild(self.scrollIndicator)
            self.scrollBar.addChild(self.scrollUpBtn)
            self.scrollBar.addChild(self.scrollDownBtn)
            super(GUI.ScrollableContainer, self).addChild(self.container)
            super(GUI.ScrollableContainer, self).addChild(self.scrollBar)
            self.offset = 0
            self.minOffset = 0
            self.maxOffset = self.container.computedHeight
            self.scrollIndicator.update()

        def scroll(self, amount):
            if amount < 0:
                if self.offset - amount - self.computedHeight <= -self.maxOffset:
                    return
            else:
                if self.offset + amount > self.minOffset:
                    #self.offset = -self.minOffset
                    return
            for child in self.container.childComponents:
                child.position[1] = child.computedPosition[1]+amount
            self.offset += amount
            self.scrollIndicator.update()

        def getVisibleChildren(self):
            visible = []
            for child in self.container.childComponents:
                if child.computedPosition[1]+child.computedHeight >= -10 and child.computedPosition[1]-child.computedHeight <= self.computedHeight + 10:
                    visible.append(child)
            return visible

        def getClickedChild(self, mouseEvent, offsetX=0, offsetY=0):
            if not self.checkClick(mouseEvent, offsetX, offsetY):
                return None
            clicked = self.scrollBar.getClickedChild(mouseEvent, offsetX + self.computedPosition[0], offsetY + self.computedPosition[1])
            if clicked != None: return clicked
            visible = self.getVisibleChildren()
            currChild = len(visible)
            while currChild > 0:
                currChild -= 1
                child = visible[currChild]
                if "SKIP_CHILD_CHECK" in child.__dict__:
                    if child.SKIP_CHILD_CHECK:
                        if child.checkClick(mouseEvent, offsetX + self.computedPosition[0], offsetY + self.computedPosition[1]):
                            return child
                        else:
                            continue
                    else:
                        subCheck = child.getClickedChild(mouseEvent, offsetX + self.computedPosition[0], offsetY + self.computedPosition[1])
                        if subCheck == None: continue
                        return subCheck
                else:
                    if child.checkClick(mouseEvent, offsetX + self.computedPosition[0], offsetY + self.computedPosition[1]):
                        return child
            if self.checkClick(mouseEvent, offsetX, offsetY):
                return self
            return None

        def addChild(self, component):
            if component.computedPosition[1] < self.minOffset: self.minOffset = component.computedPosition[1]
            if component.computedPosition[1]+component.computedHeight > self.maxOffset: self.maxOffset = component.computedPosition[1]+component.computedHeight
            self.container.addChild(component)
            self.scrollIndicator.update()

        def removeChild(self, component):
            self.container.removeChild(component)
            if component.computedPosition[1] == self.minOffset:
                self.minOffset = 0
                for comp in self.container.childComponents:
                    if comp.computedPosition[1] < self.minOffset: self.minOffset = comp.computedPosition[1]
            if component.computedPosition[1] == self.maxOffset:
                self.maxOffset = self.computedHeight
                for comp in self.container.childComponents:
                    if comp.computedPosition[1]+comp.computedHeight > self.maxOffset: self.maxOffset = comp.computedPosition[1]+comp.computedHeight
            self.scrollIndicator.update()

        def clearChildren(self):
            self.container.clearChildren()
            self.maxOffset = self.computedHeight
            self.offset = 0
            self.scrollIndicator.update()

        def render(self, largerSurface):
            super(GUI.ScrollableContainer, self).render(largerSurface)

        def refresh(self, children=True):
            #super(GUI.ScrollableContainer, self).refresh()
            self.minOffset = 0
            for comp in self.container.childComponents:
                if comp.computedPosition[1] < self.minOffset: self.minOffset = comp.computedPosition[1]
            self.maxOffset = self.computedHeight
            for comp in self.container.childComponents:
                if comp.computedPosition[1]+comp.computedHeight > self.maxOffset: self.maxOffset = comp.computedPosition[1]+comp.computedHeight
            self.scrollIndicator.update()
            self.container.refresh(children)

    class ListScrollableContainer(ScrollableContainer):
        def __init__(self, position, **data):
            self.margin = data.get("margin", 0)
            super(GUI.ListScrollableContainer, self).__init__(position, **data)

        def getCumulativeHeight(self):
            height = 0
            if self.container.childComponents == []: 0
            for component in self.container.childComponents:
                height += component.computedHeight + self.margin
            return height

        def addChild(self, component):
            component.position[1] = self.getCumulativeHeight()
            component.setDimensions()
            super(GUI.ListScrollableContainer, self).addChild(component)

        def removeChild(self, component):
            super(GUI.ListScrollableContainer, self).removeChild(component)
            childrenCopy = self.container.childComponents[:]
            self.container.childComponents = []
            for child in childrenCopy:
                self.addChild(child)

    class TextScrollableContainer(ScrollableContainer):
        def __init__(self, position, textComponent=DEFAULT, **data):
            #Defaults to creating a text component.
            data["scrollAmount"] = data.get("lineHeight", textComponent.lineHeight if textComponent != DEFAULT else 16)
            super(GUI.TextScrollableContainer, self).__init__(position, **data)
            if textComponent == DEFAULT:
                self.textComponent = GUI.ExpandingMultiLineText((0, 0), "", State.instance.getColorPalette().getColor("item"), width=self.container.computedWidth, height=self.container.computedHeight, scroller=self)
            else:
                self.textComponent = textComponent
                if self.textComponent.computedWidth == self.computedWidth:
                    self.textComponent.width = self.container.width
                    #self.textComponent.refresh()
            self.addChild(self.textComponent)

        def getTextComponent(self):
            return self.textComponent

    class MultiLineTextEntryField(ListScrollableContainer):
        def __init__(self, position, initialText="", **data):
            if "border" not in data:
                data["border"] = 1
                data["borderColor"] = State.instance.getColorPalette().getColor("accent")
            data["onClick"] = self.activateLast
            data["onClickData"] = ()
            super(GUI.MultiLineTextEntryField, self).__init__(position, **data)
            self.lineHeight = data.get("lineHeight", 20)
            self.maxLines = data.get("maxLines", -2)
            self.backgroundColor = data.get("backgroundColor", State.instance.getColorPalette().getColor("background"))
            self.textColor = data.get("color", State.instance.getColorPalette().getColor("item"))
            self.textFields = []
            self.wrappedLines = []
            self.currentField = -1
            self.setText(initialText)

        def activateLast(self):
            self.currentField = len(self.textFields) - 1
            self.textFields[self.currentField].activate()

        def refresh(self):
            super(GUI.MultiLineTextEntryField, self).refresh()
            self.clearChildren()
            for tf in self.textFields:
                self.addChild(tf)

        def setCurrent(self, field):
            self.currentField = self.textFields.index(field)

        def addField(self, initial_text):
            if len(self.textFields) == self.maxLines:
                return
            field = GUI.TextEntryField((0, 0), initial_text, width=self.container.computedWidth, height=self.lineHeight,
                                       backgroundColor=self.backgroundColor, textColor=self.textColor)
            field.border = 0
            field.MULTILINE = self
            self.currentField += 1
            self.textFields.insert(self.currentField, field)
            field.activate()
            self.refresh()

#         def prependToNextField(self, text): #HOLD FOR NEXT RELEASE
#             print "Prep: "+text
#             self.currentField += 1
#             currentText = self.textFields[self.currentField].textComponent.text
#             self.textFields[self.currentField].textComponent.text = ""
#             self.textFields[self.currentField].indicatorPosition = 0
#             self.textFields[self.currentField].refresh()
#             self.textFields[self.currentField].activate()
#             for word in (" "+text+" "+currentText).split(" "):
#                 self.textFields[self.currentField].appendChar(word+" ")
#             self.textFields[self.currentField].refresh()

        def removeField(self, field):
            if self.currentField > 0:
                if self.textFields.index(field) == self.currentField:
                    self.currentField -= 1
                self.textFields.remove(field)
            self.refresh()

        def getDeleteChar(self):
            if self.currentField < len(self.textFields) - 1:
                c = ""
                try:
                    c = self.textFields[self.currentField + 1].textComponent.text[0]
                    self.textFields[self.currentField + 1].textComponent.text = self.textFields[self.currentField + 1].textComponent.text[1:]
                    self.textFields[self.currentField + 1].updateOverflow()
                    self.textFields[self.currentField + 1].refresh()
                except:
                    self.removeField(self.textFields[self.currentField + 1])
                return c
            return ""

        def getText(self):
            t = ""
            p = 0
            for ftext in [f.getText() for f in self.textFields]:
                if p in self.wrappedLines:
                    t += ftext
                else:
                    t += ftext + "\n"
                p += 1
            t.rstrip("\n")
            return t

        def clear(self):
            self.textFields = []
            self.wrappedLines = []
            self.currentField = -1
            self.refresh()

        def setText(self, text):
            self.clear()
            if text == "":
                self.addField("")
            else:
                for line in text.replace("\r", "").split("\n"):
                    self.addField("")
                    line = line.rstrip()
                    words = line.split(" ")
                    oldN = self.currentField
                    for word in words:
                        self.textFields[self.currentField].appendChar(word)
                        self.textFields[self.currentField].appendChar(" ")
                    if oldN != self.currentField:
                        for n in range(oldN, self.currentField): self.wrappedLines.append(n)
                for field in self.textFields:
                    if field.overflow > 0:
                        field.textComponent.setText(field.textComponent.text.rstrip(" "))
                        field.updateOverflow()
            self.refresh()
            State.instance.getKeyboard().deactivate()

    class FunctionBar(object):
        def __init__(self):
            self.container = GUI.Container((0, State.instance.getGUI().height-40), background=State.instance.getColorPalette().getColor("background"), width=State.instance.getGUI().width, height=40)
            self.launcherApp = State.instance.getApplicationList().getApp("launcher")
            self.notificationMenu = GUI.NotificationMenu()
            self.recentAppSwitcher = GUI.RecentAppSwitcher()
            self.menu_button = GUI.Image((0, 0), surface=State.instance.getIcons().getLoadedIcon("menu"), onClick=self.activateLauncher, onLongClick=Application.fullCloseCurrent)
            self.app_title_text = GUI.Text((42, 8), "Python OS 6", State.instance.getColorPalette().getColor("item"), 20, onClick=self.toggleRecentAppSwitcher)
            self.clock_text = GUI.Text((State.instance.getGUI().width-45, 8), self.formatTime(), State.instance.getColorPalette().getColor("accent"), 20, onClick=self.toggleNotificationMenu, onLongClick=State.rescue) #Add Onclick Menu
            self.container.addChild(self.menu_button)
            self.container.addChild(self.app_title_text)
            self.container.addChild(self.clock_text)

        def formatTime(self):
            time = str(datetime.now())
            if time.startswith("0"): time = time[1:]
            return time[time.find(" ")+1:time.find(":", time.find(":")+1)]

        def render(self):
            if State.instance.getNotificationQueue().new:
                self.clock_text.color = (255, 59, 59)
            self.clock_text.text = self.formatTime()
            self.clock_text.refresh()
            self.container.render(screen)

        def activateLauncher(self):
            if State.instance.getActiveApplication() != self.launcherApp:
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

    class Keyboard(object):
        def __init__(self, textEntryField=None):
            self.shiftUp = False
            self.active = False
            self.textEntryField = textEntryField
            self.movedUI = False
            self._symbolFont = GUI.Font("res/symbols.ttf", 10, 20)
            if self.textEntryField.computedPosition[1] + self.textEntryField.computedHeight > 2*(State.instance.getGUI().height/3) or self.textEntryField.data.get("slideUp", False):
                State.instance.getActiveApplication().ui.setPosition((0, -80))
                self.movedUI = True
            self.baseContainer = None
            self.baseContainer = GUI.Container((0, 0), width=State.instance.getGUI().width, height=State.instance.getGUI().height/3)
            self.baseContainer.setPosition((0, 2*(State.instance.getGUI().height/3)))
            self.keyWidth = self.baseContainer.computedWidth / 10
            self.keyHeight = self.baseContainer.computedHeight / 4
            use_ft = State.instance.getTypingFont().ft_support
            #if use_ft:
            self.shift_sym = u"⇧"
            self.enter_sym = u"⏎"
            self.bkspc_sym = u"⌫"
            self.delet_sym = u"⌦"
#             else:
#                 self.shift_sym = "sh"
#                 self.enter_sym = "->"
#                 self.bkspc_sym = "<-"
#                 self.delet_sym = "del"
            self.keys1 = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
                         ["a", "s", "d", "f", "g", "h", "j", "k", "l", self.enter_sym],
                         [self.shift_sym, "z", "x", "c", "v", "b", "n", "m", ",", "."],
                         ["!", "?", " ", "", "", "", "", "-", "'", self.bkspc_sym]]
            self.keys2 = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                         ["@", "#", "$", "%", "^", "&", "*", "(", ")", "_"],
                         ["=", "+", "\\", "/", "<", ">", "|", "[", "]", ":"],
                         [";", "{", "}", "", "", "", "", "-", "\"", self.delet_sym]]
            row = 0
            for symrow in self.keys1:
                sym = 0
                for symbol in symrow:
                    button = None
                    if symbol == "":
                        sym += 1
                        continue
                    if symbol == " ":
                        button = GUI.KeyboardButton((sym * self.keyWidth, row * self.keyHeight), "", self.keys2[row][sym],
                                                    onClick=self.insertChar, onClickData=(self.keys1[row][sym],),
                                                    onLongClick=self.insertChar, onLongClickData=(self.keys2[row][sym],),
                                                    width=self.keyWidth*5, height=self.keyHeight, freetype=use_ft)
                    else:
                        if symbol == self.shift_sym or symbol == self.enter_sym or symbol == self.bkspc_sym or symbol == self.delet_sym:
                            button = GUI.KeyboardButton((sym * self.keyWidth, row * self.keyHeight), self.keys1[row][sym], self.keys2[row][sym],
                                                    onClick=self.insertChar, onClickData=(self.keys1[row][sym],),
                                                    onLongClick=self.insertChar, onLongClickData=(self.keys2[row][sym],),
                                                    width=self.keyWidth, height=self.keyHeight, border=1, borderColor=State.instance.getColorPalette().getColor("accent"),
                                                    font=self._symbolFont, freetype=use_ft)
                        else:
                            button = GUI.KeyboardButton((sym * self.keyWidth, row * self.keyHeight), self.keys1[row][sym], self.keys2[row][sym],
                                                        onClick=self.insertChar, onClickData=(self.keys1[row][sym],),
                                                        onLongClick=self.insertChar, onLongClickData=(self.keys2[row][sym],),
                                                        width=self.keyWidth, height=self.keyHeight,
                                                        freetype=use_ft)
                    self.baseContainer.addChild(button)
                    sym += 1
                row += 1

        def deactivate(self):
            self.active = False
            if self.movedUI:
                State.instance.getActiveApplication().ui.position[1] = 0
            self.textEntryField = None

        def setTextEntryField(self, field):
            self.textEntryField = field
            self.active = True
            if self.textEntryField.computedPosition[1] + self.textEntryField.height > State.instance.getGUI().height - self.baseContainer.computedHeight or self.textEntryField.data.get("slideUp", False):
                State.instance.getActiveApplication().ui.setPosition((0, -self.baseContainer.computedHeight))
                self.movedUI = True

        def getEnteredText(self):
            return self.textEntryField.getText()

        def insertChar(self, char):
            if char == self.shift_sym:
                self.shiftUp = not self.shiftUp
                for button in self.baseContainer.childComponents:
                    if self.shiftUp:
                        button.primaryTextComponent.text = button.primaryTextComponent.text.upper()
                    else:
                        button.primaryTextComponent.text = button.primaryTextComponent.text.lower()
                    button.primaryTextComponent.refresh()
                return
            if char == self.enter_sym:
                mult = self.textEntryField.MULTILINE
                self.deactivate()
                if mult != None:
                    mult.textFields[mult.currentField].doBlink = False
                    mult.addField("")
                return
            if char == self.bkspc_sym:
                self.textEntryField.backspace()
                return
            if char == self.delet_sym:
                self.textEntryField.delete()
            else:
                if self.shiftUp:
                    self.textEntryField.appendChar(char.upper())
                    self.shiftUp = False
                    for button in self.baseContainer.childComponents:
                        button.primaryTextComponent.text = button.primaryTextComponent.text.lower()
                        button.primaryTextComponent.refresh()
                else:
                    self.textEntryField.appendChar(char)

        def render(self, largerSurface):
            self.baseContainer.render(largerSurface)

    class Overlay(object):
        def __init__(self, position, **data):
            self.position = list(position)
            self.displayed = False
            self.width = int(int(data.get("width").rstrip("%")) * (State.instance.getActiveApplication().ui.width/100.0)) if type(data.get("width")) == str else data.get("width", State.instance.getGUI().width)
            self.height = int(int(data.get("height").rstrip("%")) * (State.instance.getActiveApplication().ui.height/100.0)) if type(data.get("height")) == str else data.get("height", State.instance.getGUI().height-40)
            self.color = data.get("color", State.instance.getColorPalette().getColor("background"))
            self.baseContainer = GUI.Container((0, 0), width=State.instance.getGUI().width, height=State.instance.getActiveApplication().ui.height, color=(0, 0, 0, 0), onClick=self.hide)
            self.container = data.get("container", GUI.Container(self.position[:], width=self.width, height=self.height, color=self.color))
            self.baseContainer.addChild(self.container)
            self.application = State.instance.getActiveApplication()

        def display(self):
            self.application = State.instance.getActiveApplication()
            self.application.ui.setDialog(self)
            self.displayed = True

        def hide(self):
            self.application.ui.clearDialog()
            self.application.ui.refresh()
            self.displayed = False

        def addChild(self, child):
            self.container.addChild(child)

    class Dialog(Overlay):
        def __init__(self, title, text, actionButtons, onResponseRecorded=None, onResponseRecordedData=(), **data):
            super(GUI.Dialog, self).__init__((0, (State.instance.getActiveApplication().ui.height/2)-65), height=data.get("height", 130),
                                             width=data.get("width", State.instance.getGUI().width),
                                             color=data.get("color", State.instance.getColorPalette().getColor("background")))
            self.container.border = 3
            self.container.borderColor = State.instance.getColorPalette().getColor("item")
            self.container.refresh()
            self.application = State.instance.getActiveApplication()
            self.title = title
            self.text = text
            self.response = None
            self.buttonList = GUI.Dialog.getButtonList(actionButtons, self) if type(actionButtons[0]) == str else actionButtons
            self.textComponent = GUI.MultiLineText((2, 2), self.text, State.instance.getColorPalette().getColor("item"), 16, width=self.container.computedWidth-4, height=96)
            self.buttonRow = GUI.ButtonRow((0, 96), width=State.instance.getGUI().width, height=40, color=(0, 0, 0, 0), padding=0, margin=0)
            for button in self.buttonList:
                self.buttonRow.addChild(button)
            self.addChild(self.textComponent)
            self.addChild(self.buttonRow)
            self.onResponseRecorded = onResponseRecorded
            self.onResponseRecordedData = onResponseRecordedData

        def display(self):
            State.instance.getFunctionBar().app_title_text.setText(self.title)
            self.application.ui.setDialog(self)

        def hide(self):
            State.instance.getFunctionBar().app_title_text.setText(State.instance.getActiveApplication().title)
            self.application.ui.clearDialog()
            self.application.ui.refresh()

        def recordResponse(self, response):
            self.response = response
            self.hide()
            if self.onResponseRecorded != None:
                if self.onResponseRecordedData != None:
                    self.onResponseRecorded(*((self.onResponseRecordedData)+(self.response,)))

        def getResponse(self):
            return self.response

        @staticmethod
        def getButtonList(titles, dialog):
            blist = []
            for title in titles:
                blist.append(GUI.Button((0, 0), title, State.instance.getColorPalette().getColor("item"), State.instance.getColorPalette().getColor("background"), 18,
                                        width=dialog.container.computedWidth/len(titles), height=40,
                                        onClick=dialog.recordResponse, onClickData=(title,)))
            return blist

    class OKDialog(Dialog):
        def __init__(self, title, text, onResposeRecorded=None, onResponseRecordedData=()):
            okbtn = GUI.Button((0,0), "OK", State.instance.getColorPalette().getColor("item"), State.instance.getColorPalette().getColor("background"), 18,
                               width=State.instance.getGUI().width, height=40, onClick=self.recordResponse, onClickData=("OK",))
            super(GUI.OKDialog, self).__init__(title, text, [okbtn], onResposeRecorded)

    class ErrorDialog(Dialog):
        def __init__(self, text, onResposeRecorded=None, onResponseRecordedData=()):
            okbtn = GUI.Button((0,0), "Acknowledged", State.instance.getColorPalette().getColor("item"), State.instance.getColorPalette().getColor("background"), 18,
                               width=State.instance.getGUI().width, height=40, onClick=self.recordResponse, onClickData=("Acknowledged",))
            super(GUI.ErrorDialog, self).__init__("Error", text, [okbtn], onResposeRecorded)
            self.container.backgroundColor = State.instance.getColorPalette().getColor("error")

    class WarningDialog(Dialog):
        def __init__(self, text, onResposeRecorded=None, onResponseRecordedData=()):
            okbtn = GUI.Button((0,0), "OK", State.instance.getColorPalette().getColor("item"), State.instance.getColorPalette().getColor("background"), 18,
                               width=State.instance.getGUI().width, height=40, onClick=self.recordResponse, onClickData=("OK",))
            super(GUI.WarningDialog, self).__init__("Warning", text, [okbtn], onResposeRecorded)
            self.container.backgroundColor = State.instance.getColorPalette().getColor("warning")

    class YNDialog(Dialog):
        def __init__(self, title, text, onResponseRecorded=None, onResponseRecordedData=()):
            ybtn = GUI.Button((0,0), "Yes", (200, 250, 200), (50, 50, 50), 18,
                               width=(State.instance.getGUI().width/2), height=40, onClick=self.recordResponse, onClickData=("Yes",))
            nbtn = GUI.Button((0,0), "No", State.instance.getColorPalette().getColor("item"), State.instance.getColorPalette().getColor("background"), 18,
                               width=(State.instance.getGUI().width/2), height=40, onClick=self.recordResponse, onClickData=("No",))
            super(GUI.YNDialog, self).__init__(title, text, [ybtn, nbtn], onResponseRecorded)
            self.onResponseRecordedData = onResponseRecordedData

    class OKCancelDialog(Dialog):
        def __init__(self, title, text, onResponseRecorded=None, onResponseRecordedData=()):
            okbtn = GUI.Button((0,0), "OK", State.instance.getColorPalette().getColor("background"), State.instance.getColorPalette().getColor("item"), 18,
                               width=State.instance.getGUI().width/2, height=40, onClick=self.recordResponse, onClickData=("OK",))
            cancbtn = GUI.Button((0,0), "Cancel", State.instance.getColorPalette().getColor("item"), State.instance.getColorPalette().getColor("background"), 18,
                               width=State.instance.getGUI().width/2, height=40, onClick=self.recordResponse, onClickData=("Cancel",))
            super(GUI.OKCancelDialog, self).__init__(title, text, [okbtn, cancbtn], onResponseRecorded, onResponseRecordedData)

    class AskDialog(Dialog):
        def __init__(self, title, text, onResposeRecorded=None, onResponseRecordedData=()):
            okbtn = GUI.Button((0,0), "OK", State.instance.getColorPalette().getColor("background"), State.instance.getColorPalette().getColor("item"), 18,
                               width=State.instance.getGUI().width/2, height=40, onClick=self.returnRecordedResponse)
            cancelbtn = GUI.Button((0,0), "Cancel", State.instance.getColorPalette().getColor("item"), State.instance.getColorPalette().getColor("background"), 18,
                               width=State.instance.getGUI().width/2, height=40, onClick=self.recordResponse, onClickData=("Cancel",))
            super(GUI.AskDialog, self).__init__(title, text, [okbtn, cancelbtn], onResposeRecorded, onResponseRecordedData)
            self.textComponent.computedHeight -= 20
            self.textComponent.refresh()
            self.textEntryField = GUI.TextEntryField((0, 80), width=self.container.computedWidth, height=20)
            self.container.addChild(self.textEntryField)

        def returnRecordedResponse(self):
            self.recordResponse(self.textEntryField.getText())

    class CustomContentDialog(Dialog):
        def __init__(self, title, customComponent, actionButtons, onResponseRecorded=None, btnPad=0, btnMargin=5, **data):
            self.application = State.instance.getActiveApplication()
            self.title = title
            self.response = None
            self.baseContainer = GUI.Container((0, 0), width=State.instance.getGUI().width, height=State.instance.getActiveApplication().ui.height, color=(0, 0, 0, 0.5))
            self.container = customComponent
            self.buttonList = GUI.Dialog.getButtonList(actionButtons, self) if type(actionButtons[0]) == str else actionButtons
            self.buttonRow = GUI.ButtonRow((0, self.container.computedHeight-33), width=self.container.computedWidth, height=40, color=(0, 0, 0, 0), padding=btnPad, margin=btnMargin)
            for button in self.buttonList:
                self.buttonRow.addChild(button)
            self.container.addChild(self.buttonRow)
            self.baseContainer.addChild(self.container)
            self.onResponseRecorded = onResponseRecorded
            self.data = data
            self.onResponseRecordedData = data.get("onResponseRecordedData", ())

    class NotificationMenu(Overlay):
        def __init__(self):
            super(GUI.NotificationMenu, self).__init__(("20%", "25%"), width="80%", height="75%", color=(20, 20, 20, 200))
            self.text = GUI.Text((1, 1), "Notifications", (200, 200, 200), 18)
            self.clearAllBtn = GUI.Button((self.width-50, 0), "Clear", (200, 200, 200), (20, 20, 20), width=50, height=20, onClick=self.clearAll)
            self.nContainer = GUI.ListScrollableContainer((0, 20), width="80%", height=self.height-20, transparent=True, margin=5)
            self.addChild(self.text)
            self.addChild(self.clearAllBtn)
            self.addChild(self.nContainer)
            self.refresh()

        def refresh(self):
            self.nContainer.clearChildren()
            for notification in State.instance.getNotificationQueue().notifications:
                self.nContainer.addChild(notification.getContainer())

        def display(self):
            self.refresh()
            State.instance.getNotificationQueue().new = False
            State.instance.getFunctionBar().clock_text.color = State.instance.getColorPalette().getColor("accent")
            super(GUI.NotificationMenu, self).display()

        def clearAll(self):
            State.instance.getNotificationQueue().clear()
            self.refresh()

    class RecentAppSwitcher(Overlay):
        def __init__(self):
            super(GUI.RecentAppSwitcher, self).__init__((0, screen.get_height()-100), height=60)
            self.container.border = 1
            self.container.borderColor = State.instance.getColorPalette().getColor("item")

        def populate(self):
            self.container.clearChildren()
            self.recent_pages = GUI.PagedContainer((20, 0), width=self.width-40, height=60, hideControls=True)
            self.recent_pages.addPage(self.recent_pages.generatePage())
            self.btnLeft = GUI.Button((0, 0), "<", State.instance.getColorPalette().getColor("accent"), State.instance.getColorPalette().getColor("item"), 20, width=20, height=60,
                                      onClick=self.recent_pages.pageLeft)
            self.btnRight = GUI.Button((self.width-20, 0), ">", State.instance.getColorPalette().getColor("accent"), State.instance.getColorPalette().getColor("item"), 20, width=20, height=60,
                                      onClick=self.recent_pages.pageRight)
            per_app = (self.width-40)/4
            current = 0
            for app in State.instance.getApplicationList().activeApplications:
                if app != State.instance.getActiveApplication() and app.parameters.get("persist", True) and app.name != "home":
                    if current >= 4:
                        current = 0
                        self.recent_pages.addPage(self.recent_pages.generatePage())
                    cont = GUI.Container((per_app*current, 0), transparent=True, width=per_app, height=self.height, border=1, borderColor=State.instance.getColorPalette().getColor("item"),
                                         onClick=self.activate, onClickData=(app,), onLongClick=self.closeAsk, onLongClickData=(app,))
                    cont.SKIP_CHILD_CHECK = True
                    icon = app.getIcon()
                    if not icon: icon = State.instance.getIcons().getLoadedIcon("unknown")
                    img = GUI.Image((0, 5), surface=icon)
                    img.position[0] = GUI.getCenteredCoordinates(img, cont)[0]
                    name = GUI.Text((0, 45), app.title, State.instance.getColorPalette().getColor("item"), 10)
                    name.position[0] = GUI.getCenteredCoordinates(name, cont)[0]
                    cont.addChild(img)
                    cont.addChild(name)
                    self.recent_pages.addChild(cont)
                    current += 1
            if len(self.recent_pages.getPage(0).childComponents) == 0:
                notxt = GUI.Text((0, 0), "No Recent Apps", State.instance.getColorPalette().getColor("item"), 16)
                notxt.position = GUI.getCenteredCoordinates(notxt, self.recent_pages.getPage(0))
                self.recent_pages.addChild(notxt)
            self.recent_pages.goToPage()
            self.addChild(self.recent_pages)
            self.addChild(self.btnLeft)
            self.addChild(self.btnRight)

        def display(self):
            self.populate()
            super(GUI.RecentAppSwitcher, self).display()

        def activate(self, app):
            self.hide()
            app.activate()

        def closeAsk(self, app):
            GUI.YNDialog("Close", "Are you sure you want to close the app "+app.title+"?", self.close, (app,)).display()

        def close(self, app, resp):
            if resp == "Yes":
                app.deactivate(False)
                self.hide()
                if State.instance.getActiveApplication() == State.instance.getApplicationList().getApp("launcher"):
                    Application.fullCloseCurrent()


    class Selector(Container):
        def __init__(self, position, items, **data):
            self.onValueChanged = data.get("onValueChanged", Application.dummy)
            self.onValueChangedData = data.get("onValueChangedData", ())
            self.overlay = GUI.Overlay((20, 20), width=State.instance.getGUI().width-40, height=State.instance.getGUI().height-80)
            self.overlay.container.border = 1
            self.scroller = GUI.ListScrollableContainer((0, 0), transparent=True, width=self.overlay.width, height=self.overlay.height, scrollAmount=20)
            for comp in self.generateItemSequence(items, 14, State.instance.getColorPalette().getColor("item")):
                self.scroller.addChild(comp)
            self.overlay.addChild(self.scroller)
            super(GUI.Selector, self).__init__(position, **data)
            self.eventBindings["onClick"] = self.showOverlay
            self.eventData["onClick"] = ()
            self.textColor = data.get("textColor", State.instance.getColorPalette().getColor("item"))
            self.items = items
            self.currentItem = self.items[0]
            self.textComponent = GUI.Text((0,0), self.currentItem, self.textColor, 14, onClick=self.showOverlay)
            self.textComponent.setPosition([2, GUI.getCenteredCoordinates(self.textComponent, self)[1]])
            self.addChild(self.textComponent)

        def showOverlay(self):
            self.overlay.display()

        def generateItemSequence(self, items, size=22, color=(0,0,0)):
            comps = []
            acc_height = 0
            for item in items:
                el_c = GUI.Container((0, acc_height), transparent=True, width=self.overlay.width, height=40,
                                     onClick=self.onSelect, onClickData=(item,), border=1, borderColor=(20,20,20))
                elem = GUI.Text((2, 0), item, color, size,
                                onClick=self.onSelect, onClickData=(item,))
                elem.position[1] = GUI.getCenteredCoordinates(elem, el_c)[1]
                el_c.addChild(elem)
                el_c.SKIP_CHILD_CHECK = True
                comps.append(el_c)
                acc_height += el_c.computedHeight
            return comps

        def onSelect(self, newVal):
            self.overlay.hide()
            self.currentItem = newVal
            self.textComponent.text = self.currentItem
            self.textComponent.refresh()
            self.onValueChanged(*(self.onValueChangedData + (newVal,)))

        def render(self, largerSurface):
            super(GUI.Selector, self).render(largerSurface)
            pygame.draw.circle(largerSurface, State.instance.getColorPalette().getColor("accent"), (self.computedPosition[0]+self.computedWidth-(self.computedHeight/2)-2, self.computedPosition[1]+(self.computedHeight/2)), (self.computedHeight/2)-5)

        def getClickedChild(self, mouseEvent, offsetX=0, offsetY=0):
            if self.checkClick(mouseEvent, offsetX, offsetY):
                return self
            return None

        def getValue(self):
            return self.currentItem