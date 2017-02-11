from datetime import datetime
import pygame

from pyos.gui.keyboard import Keyboard
from pyos.state import State
from pyos.gui.container import Container
from pyos.gui.text import Text
import pyos.gui as gui


class TextEntryField(Container):
    def __init__(self, position, initialText="", **data):
        if "border" not in data:
            data["border"] = 1
            data["borderColor"] = State.instance().getColorPalette().getColor("accent")
        if "textColor" not in data:
            data["textColor"] = State.instance().getColorPalette().getColor("item")
        if "blink" in data:
            self.blinkInterval = data["blink"]
        else:
            self.blinkInterval = 500
        self.doBlink = True
        self.blinkOn = False
        self.lastBlink = datetime.now()
        self.indicatorPosition = len(initialText)
        self.indicatorPxPosition = 0
        super(TextEntryField, self).__init__(position, **data)
        self.SKIP_CHILD_CHECK = True
        self.textComponent = Text((2, 0), initialText, data["textColor"], 16, font=State.instance().getTypingFont())
        self.updateOverflow()
        self.lastClickCoord = None
        self.textComponent.position[1] = gui.core.getCenteredCoordinates(self.textComponent, self)[1]
        self.addChild(self.textComponent)
        self.MULTILINE = None
        self.internalClickOverrides["onClick"] = (self.activate, ())
        self.internalClickOverrides["onIntermediateUpdate"] = (self.dragScroll, ())

    def clearScrollParams(self):
        self.lastClickCoord = None

    def dragScroll(self):
        if self.lastClickCoord is not None and self.overflow > 0:
            ydist = self.innerClickCoordinates[1] - self.lastClickCoord[1]
            self.overflow -= ydist
            if self.overflow > 0 and self.overflow + self.computedWidth < self.textComponent.computedWidth:
                self.textComponent.position[0] = 2 - self.overflow
            else:
                self.textComponent.position[0] = 2
        self.lastClickCoord = self.innerClickCoordinates

    def getPxPosition(self, fromPos=gui.DEFAULT):
        return State.instance().getTypingFont().get(16).size(self.textComponent.text[:(self.indicatorPosition if fromPos==gui.DEFAULT else fromPos)])[0]

    def activate(self):
        self.clearScrollParams()
        self.updateOverflow()
        State.instance().setKeyboard(Keyboard(self))
        if self.MULTILINE is not None:
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
        State.instance().getKeyboard().active = True
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
        super(TextEntryField, self).refresh()

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
        super(Container, self).render(largerSurface)

    def getClickedChild(self, mouseEvent, offsetX=0, offsetY=0):
        if self.checkClick(mouseEvent, offsetX, offsetY):
            return self
        return None
