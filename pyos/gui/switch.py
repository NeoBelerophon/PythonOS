import pygame

from pyos import State
from pyos.gui.component import Component


class Switch(Component):
    def __init__(self, position, on=False, **data):
        if "border" not in data:
            data["border"] = 2
            data["borderColor"] = State.instance().getColorPalette().getColor("item")
        super(Switch, self).__init__(position, **data)
        self.backgroundColor = data.get("backgroundColor", State.instance().getColorPalette().getColor("background"))
        self.onColor = data.get("onColor", State.instance().getColorPalette().getColor("accent"))
        self.offColor = data.get("offColor", State.instance().getColorPalette().getColor("dark:background"))
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
        pygame.draw.circle(self.surface, State.instance().getColorPalette().getColor("item"), (self.computedWidth/4, self.computedHeight/2), self.computedHeight/4, 2)
        pygame.draw.line(self.surface, State.instance().getColorPalette().getColor("item"), (3*(self.computedWidth/4), self.computedHeight/4),
                         (3*(self.computedWidth/4), 3*(self.computedHeight/4)), 2)
        super(Switch, self).render(largerSurface)
