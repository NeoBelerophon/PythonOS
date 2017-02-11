from pyos.gui.component import Component
from pyos.gui.container import Container
import pyos.gui as gui
from pyos.gui.text import Text
from pyos.state import State


class Button(Container):
    def __init__(self, position, text, bgColor=gui.DEFAULT, textColor=gui.DEFAULT, textSize=gui.DEFAULT, **data):
        # Defaults are "darker:background", "item", and 14.
        bgColor, textColor, textSize = Component.default(bgColor, State.instance().getColorPalette().getColor("darker:background"),
                              textColor, State.instance().getColorPalette().getColor("item"),
                              textSize, 14)
        self.textComponent = Text((0, 0), text, textColor, textSize, font=data.get("font", State.instance().getFont()), freetype=data.get("freetype", False))
        self.paddingAmount = data.get("padding", 5)
        if "width" not in data: data["width"] = self.textComponent.computedWidth + (2 * self.paddingAmount)
        if "height" not in data: data["height"] = self.textComponent.computedHeight + (2 * self.paddingAmount)
        super(Button, self).__init__(position, **data)
        self.SKIP_CHILD_CHECK = True
        self.textComponent.setPosition(gui.core.getCenteredCoordinates(self.textComponent, self))
        self.backgroundColor = bgColor
        self.addChild(self.textComponent)

    def setDimensions(self):
        super(Button, self).setDimensions()
        self.textComponent.setPosition(gui.core.getCenteredCoordinates(self.textComponent, self))

    def setText(self, text):
        self.textComponent.setText(text)
        self.setDimensions()

    def render(self, largerSurface):
        super(Button, self).render(largerSurface)

    def getClickedChild(self, mouseEvent, offsetX=0, offsetY=0):
        if self.checkClick(mouseEvent, offsetX, offsetY):
            return self
        return None