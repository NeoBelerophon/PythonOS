from pyos.gui.multilinetext import MultiLineText
from pyos.gui.component import Component
from pyos.state import State
import pyos.gui as gui


class ExpandingMultiLineText(MultiLineText):
    def __init__(self, position, text, color=gui.DEFAULT, size=gui.DEFAULT, justification=gui.DEFAULT, lineHeight=gui.DEFAULT, **data):
        # Defaults are "item", 14, 0, and 16.
        color, size, justification, lineHeight = Component.default(color, State.instance().getColorPalette().getColor("item"),
                                                                       size, 14,
                                                                       justification, 0,
                                                                       lineHeight, 16)
        self.lineHeight = lineHeight
        self.linkedScroller = data.get("scroller", None)
        self.textLines = []
        super(ExpandingMultiLineText, self).__init__(position, text, color, size, justification, **data)
        self.height = self.computedHeight
        self.refresh()

    def getRenderedText(self):
        fits = False
        surf = None
        while not fits:
            d = MultiLineText.render_textrect(self.text, self.font.get(self.size), pygame.Rect(self.computedPosition[0], self.computedPosition[1], self.computedWidth, self.height),
                                                  self.color, (0, 0, 0, 0), self.justification, self.use_freetype)
            surf = d[0]
            fits = d[1] != 1
            self.textLines = d[2]
            if not fits:
                self.height += self.lineHeight
                self.computedHeight = self.height
        self.setDimensions()
        # if self.linkedScroller != None:
        #    self.linkedScroller.refresh(False)
        return surf