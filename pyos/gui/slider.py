import pygame
from pyos.application import Application
from pyos.gui.component import Component
from pyos.state import State


class Slider(Component):
    def __init__(self, position, initialPct=0, **data):
        super(Slider, self).__init__(position, **data)
        self.percent = initialPct
        self.backgroundColor = data.get("backgroundColor", State.instance().getColorPalette().getColor("background"))
        self.color = data.get("color", State.instance().getColorPalette().getColor("item"))
        self.sliderColor = data.get("sliderColor", State.instance().getColorPalette().getColor("accent"))
        self.onChangeMethod = data.get("onChange", Application.dummy)
        self.refresh()

    def onChange(self):
        self.onChangeMethod(self.percent)

    def setPercent(self, percent):
        self.percent = percent

    def refresh(self):
        self.percentPixels = self.computedWidth / 100.0
        super(Slider, self).refresh()

    def render(self, largerSurface):
        self.surface.fill(self.backgroundColor)
        pygame.draw.rect(self.surface, self.color, [0, self.computedHeight/4, self.computedWidth, self.computedHeight/2])
        pygame.draw.rect(self.surface, self.sliderColor, [(self.percent*self.percentPixels)-15, 0, 30, self.computedHeight])
        super(Slider, self).render(largerSurface)

    def checkClick(self, mouseEvent, offsetX=0, offsetY=0):
        isClicked = super(Slider, self).checkClick(mouseEvent, offsetX, offsetY)
        if isClicked:
            self.percent = ((mouseEvent.pos[0] - offsetX - self.computedPosition[0])) / self.percentPixels
            if self.percent > 100.0: self.percent = 100.0
            self.onChange()
        return isClicked

    def getPercent(self):
        return self.percent
