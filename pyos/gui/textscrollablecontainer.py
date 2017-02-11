from pyos.state import State
from pyos.gui.expandingmultilinetext import ExpandingMultiLineText
from pyos.gui.scrollablecontainer import ScrollableContainer
import pyos.gui as gui


class TextScrollableContainer(ScrollableContainer):
    def __init__(self, position, textComponent=gui.DEFAULT, **data):
        # Defaults to creating a text component.
        data["scrollAmount"] = data.get("lineHeight", textComponent.lineHeight if textComponent != gui.DEFAULT else 16)
        super(TextScrollableContainer, self).__init__(position, **data)
        if textComponent == gui.DEFAULT:
            self.textComponent = ExpandingMultiLineText((0, 0), "", State.instance().getColorPalette().getColor("item"), width=self.container.computedWidth, height=self.container.computedHeight, scroller=self)
        else:
            self.textComponent = textComponent
            if self.textComponent.computedWidth == self.computedWidth:
                self.textComponent.width = self.container.width
                #self.textComponent.refresh()
        self.addChild(self.textComponent)

    def getTextComponent(self):
        return self.textComponent
