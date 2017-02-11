import pygame

from pyos.state import State
from pyos.gui.component import Component


class ScrollIndicator(Component):
    def __init__(self, scrollCont, position, color, **data):
        super(ScrollIndicator, self).__init__(position, **data)
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
        pygame.draw.rect(self.surface, State.instance().getColorPalette().getColor("accent"), [0, int(self.slide*(1.0*self.computedHeight/self.scrollContainer.computedHeight)), self.computedWidth, int(self.sih)])
        super(ScrollIndicator, self).render(largerSurface)

    def clearScrollParams(self):
        self.lastClickCoord = None

    def dragScroll(self):
        if self.lastClickCoord != None:
            ydist = self.innerClickCoordinates[1] - self.lastClickCoord[1]
            self.scrollContainer.scroll(ydist)
        self.lastClickCoord = self.innerClickCoordinates
