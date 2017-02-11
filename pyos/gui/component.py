import pygame
import pyos.gui as gui

from pyos.gui.intermediateupdateevent import IntermediateUpdateEvent
from pyos.state import State
from copy import deepcopy


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
            self.borderColor = data.get("borderColor", State.instance().getColorPalette().getColor("item"))
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
        appc = State.instance().getActiveApplication().ui
        # Compute Position
        if type(self.position[0]) == str:
            self.computedPosition[0] = self._percentToPix(self.position[0], (State.instance().getActiveApplication().ui.width/100.0))
        else:
            if self.resizable:
                self.computedPosition[0] = int(self.position[0] * appc.scaleX)
            else:
                self.computedPosition[0] = int(self.position[0])
        if type(self.position[1]) == str:
            self.computedPosition[1] = self._percentToPix(self.position[1], (State.instance().getActiveApplication().ui.height/100.0))
        else:
            if self.resizable:
                self.computedPosition[1] = int(self.position[1] * appc.scaleY)
            else:
                self.computedPosition[1] = int(self.position[1])

        # Compute Width and Height
        if type(self.width) == str:
            self.computedWidth = self._percentToPix(self.width, (State.instance().getActiveApplication().ui.width/100.0))
        else:
            if self.resizable:
                self.computedWidth = int(self.width * appc.scaleX)
            else:
                self.computedWidth = int(self.width)
        if type(self.height) == str:
            self.computedHeight = self._percentToPix(self.height, (State.instance().getActiveApplication().ui.height/100.0))
        else:
            if self.resizable:
                self.computedHeight = int(self.height * appc.scaleY)
            else:
                self.computedHeight = int(self.height)

        # print "Computed to: " + str(self.computedPosition) + ", " + str(self.computedWidth) + "x" + str(self.computedHeight) + ", " + str(self.resizable)

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
            if not isinstance(mouseEvent, IntermediateUpdateEvent):
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
            values.append(items[p+1] if items[p] == gui.DEFAULT else items[p])
            p += 2
        return tuple(values)
