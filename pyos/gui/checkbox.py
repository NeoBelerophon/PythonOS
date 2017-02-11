import pygame

from pyos.state import State
from pyos.gui.component import Component


class Checkbox(Component):
    def __init__(self, position, checked=False, **data):
        if "border" not in data:
            data["border"] = 2
            data["borderColor"] = State.instance().getColorPalette().getColor("item")
        super(Checkbox, self).__init__(position, **data)
        self.backgroundColor = data.get("backgroundColor", State.instance().getColorPalette().getColor("background"))
        self.checkColor = data.get("checkColor", State.instance().getColorPalette().getColor("accent"))
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
        super(Checkbox, self).render(largerSurface)