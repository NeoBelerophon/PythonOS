from pyos.gui.text import Text
from pyos.state import State
from pyos.gui.container import Container
import pyos.gui as gui


class KeyboardButton(Container):
    def __init__(self, position, symbol, altSymbol, **data):
        if "border" not in data:
            data["border"] = 1
            data["borderColor"] = State.instance().getColorPalette().getColor("item")
        super(KeyboardButton, self).__init__(position, **data)
        self.SKIP_CHILD_CHECK = True
        self.primaryTextComponent = Text((1, 0), symbol, State.instance().getColorPalette().getColor("item"), 20, font=data.get("font", State.instance().getTypingFont()))
        self.secondaryTextComponent = Text((self.computedWidth-8, 0), altSymbol, State.instance().getColorPalette().getColor("item"), 10, font=data.get("font", State.instance().getTypingFont()))
        self.primaryTextComponent.setPosition([gui.core().getCenteredCoordinates(self.primaryTextComponent, self)[0]-6, self.computedHeight-self.primaryTextComponent.computedHeight-1])
        self.addChild(self.primaryTextComponent)
        self.addChild(self.secondaryTextComponent)
        self.blinkTime = 0
        self.internalClickOverrides["onClick"] = (self.registerBlink, ())
        self.internalClickOverrides["onLongClick"] = (self.registerBlink, (True,))

    def registerBlink(self, lp=False):
        self.blinkTime = State.instance().getGUI().update_interval / 6
        self.primaryTextComponent.color = State.instance().getColorPalette().getColor("background")
        self.secondaryTextComponent.color = State.instance().getColorPalette().getColor("background")
        self.backgroundColor = State.instance().getColorPalette().getColor("accent" if lp else "item")
        self.refresh()

    def getClickedChild(self, mouseEvent, offsetX=0, offsetY=0):
        if self.checkClick(mouseEvent, offsetX, offsetY):
            return self
        return None

    def render(self, largerSurface):
        if self.blinkTime >= 0:
            self.blinkTime -= 1
            if self.blinkTime < 0:
                self.primaryTextComponent.color = State.instance().getColorPalette().getColor("item")
                self.secondaryTextComponent.color = State.instance().getColorPalette().getColor("item")
                self.backgroundColor = State.instance().getColorPalette().getColor("background")
                self.refresh()
        super(KeyboardButton, self).render(largerSurface)
