from pyos.gui.component import Component
from pyos.state import State
import pyos.gui as gui


class Text(Component):
    def __init__(self, position, text, color=gui.DEFAULT, size=gui.DEFAULT, **data):
        # Defaults are "item" and 14.
        color, size = Component.default(color, State.instance().getColorPalette().getColor("item"), size, 14)
        self.text = text
        self._originalText = text
        self.size = size
        self.color = color
        self.font = data.get("font", State.instance().getFont())
        self.use_freetype = data.get("freetype", False)
        self.responsive_width = data.get("responsive_width", True)
        data["surface"] = self.getRenderedText()
        super(Text, self).__init__(position, **data)

    def getRenderedText(self):
        if self.use_freetype:
            return self.font.get(self.size, True).render(str(self.text), self.color)
        return self.font.get(self.size).render(self.text, 1, self.color)

    def refresh(self):
        self.surface = self.getRenderedText()

    def render(self, largerSurface):
        if self.text != self._originalText:
            self.setText(self.text)
        super(Text, self).render(largerSurface)

    def setText(self, text):
        self.text = text if type(text) == str or type(text) == unicode else str(text)
        self._originalText = self.text
        self.refresh()
        if self.responsive_width:
            self.width = self.surface.get_width()
            self.height = self.surface.get_height()
        self.setDimensions()