import pygame

import pyos.gui as gui
from pyos.gui.listscrollablecontainer import ListScrollableContainer
from pyos.gui.overlay import Overlay
from pyos.gui.text import Text
from pyos.state import State
from pyos.application import Application
from pyos.gui.container import Container


class Selector(Container):
    def __init__(self, position, items, **data):
        self.onValueChanged = data.get("onValueChanged", Application.dummy)
        self.onValueChangedData = data.get("onValueChangedData", ())
        self.overlay = Overlay((20, 20), width=State.instance().getGUI().width-40, height=State.instance().getGUI().height-80)
        self.overlay.container.border = 1
        self.scroller = ListScrollableContainer((0, 0), transparent=True, width=self.overlay.width, height=self.overlay.height, scrollAmount=20)
        for comp in self.generateItemSequence(items, 14, State.instance().getColorPalette().getColor("item")):
            self.scroller.addChild(comp)
        self.overlay.addChild(self.scroller)
        super(Selector, self).__init__(position, **data)
        self.eventBindings["onClick"] = self.showOverlay
        self.eventData["onClick"] = ()
        self.textColor = data.get("textColor", State.instance().getColorPalette().getColor("item"))
        self.items = items
        self.currentItem = self.items[0]
        self.textComponent = Text((0,0), self.currentItem, self.textColor, 14, onClick=self.showOverlay)
        self.textComponent.setPosition([2, gui.core.getCenteredCoordinates(self.textComponent, self)[1]])
        self.addChild(self.textComponent)

    def showOverlay(self):
        self.overlay.display()

    def generateItemSequence(self, items, size=22, color=(0,0,0)):
        comps = []
        acc_height = 0
        for item in items:
            el_c = gui.Container((0, acc_height), transparent=True, width=self.overlay.width, height=40,
                                 onClick=self.onSelect, onClickData=(item,), border=1, borderColor=(20,20,20))
            elem = gui.Text((2, 0), item, color, size,
                            onClick=self.onSelect, onClickData=(item,))
            elem.position[1] = gui.core.getCenteredCoordinates(elem, el_c)[1]
            el_c.addChild(elem)
            el_c.SKIP_CHILD_CHECK = True
            comps.append(el_c)
            acc_height += el_c.computedHeight
        return comps

    def onSelect(self, newVal):
        self.overlay.hide()
        self.currentItem = newVal
        self.textComponent.text = self.currentItem
        self.textComponent.refresh()
        self.onValueChanged(*(self.onValueChangedData + (newVal,)))

    def render(self, largerSurface):
        super(gui.Selector, self).render(largerSurface)
        pygame.draw.circle(largerSurface, State.instance().getColorPalette().getColor("accent"), (self.computedPosition[0]+self.computedWidth-(self.computedHeight/2)-2, self.computedPosition[1]+(self.computedHeight/2)), (self.computedHeight/2)-5)

    def getClickedChild(self, mouseEvent, offsetX=0, offsetY=0):
        if self.checkClick(mouseEvent, offsetX, offsetY):
            return self
        return None

    def getValue(self):
        return self.currentItem