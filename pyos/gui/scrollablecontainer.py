from pyos.state import State
from pyos.gui.container import Container
from pyos.gui.image import Image
from pyos.gui.scrollindicator import ScrollIndicator


class ScrollableContainer(Container):
    def __init__(self, position, **data):
        self.scrollAmount = data.get("scrollAmount", State.instance().getGUI().height / 8)
        super(ScrollableContainer, self).__init__(position, **data)
        self.container = Container((0, 0), transparent=True, width=self.computedWidth-20, height=self.computedHeight)
        self.scrollBar = Container((self.computedWidth-20, 0), width=20, height=self.computedHeight)
        self.scrollUpBtn = Image((0, 0), path="res/scrollup.png", width=20, height=40,
                                     onClick=self.scroll, onClickData=(self.scrollAmount,))
        self.scrollDownBtn = Image((0, self.scrollBar.computedHeight-40), path="res/scrolldown.png", width=20, height=40,
                                     onClick=self.scroll, onClickData=(-self.scrollAmount,))
        self.scrollIndicator = ScrollIndicator(self, (0, 40), self.backgroundColor, width=20, height=self.scrollBar.computedHeight-80, border=1, borderColor=State.instance().getColorPalette().getColor("item"))
        if self.computedHeight >= 120:
            self.scrollBar.addChild(self.scrollIndicator)
        self.scrollBar.addChild(self.scrollUpBtn)
        self.scrollBar.addChild(self.scrollDownBtn)
        super(ScrollableContainer, self).addChild(self.container)
        super(ScrollableContainer, self).addChild(self.scrollBar)
        self.offset = 0
        self.minOffset = 0
        self.maxOffset = self.container.computedHeight
        self.scrollIndicator.update()

    def scroll(self, amount):
        if amount < 0:
            if self.offset - amount - self.computedHeight <= -self.maxOffset:
                return
        else:
            if self.offset + amount > self.minOffset:
                #self.offset = -self.minOffset
                return
        for child in self.container.childComponents:
            child.position[1] = child.computedPosition[1]+amount
        self.offset += amount
        self.scrollIndicator.update()

    def getVisibleChildren(self):
        visible = []
        for child in self.container.childComponents:
            if child.computedPosition[1]+child.computedHeight >= -10 and child.computedPosition[1]-child.computedHeight <= self.computedHeight + 10:
                visible.append(child)
        return visible

    def getClickedChild(self, mouseEvent, offsetX=0, offsetY=0):
        if not self.checkClick(mouseEvent, offsetX, offsetY):
            return None
        clicked = self.scrollBar.getClickedChild(mouseEvent, offsetX + self.computedPosition[0], offsetY + self.computedPosition[1])
        if clicked != None: return clicked
        visible = self.getVisibleChildren()
        currChild = len(visible)
        while currChild > 0:
            currChild -= 1
            child = visible[currChild]
            if "SKIP_CHILD_CHECK" in child.__dict__:
                if child.SKIP_CHILD_CHECK:
                    if child.checkClick(mouseEvent, offsetX + self.computedPosition[0], offsetY + self.computedPosition[1]):
                        return child
                    else:
                        continue
                else:
                    subCheck = child.getClickedChild(mouseEvent, offsetX + self.computedPosition[0], offsetY + self.computedPosition[1])
                    if subCheck == None: continue
                    return subCheck
            else:
                if child.checkClick(mouseEvent, offsetX + self.computedPosition[0], offsetY + self.computedPosition[1]):
                    return child
        if self.checkClick(mouseEvent, offsetX, offsetY):
            return self
        return None

    def addChild(self, component):
        if component.computedPosition[1] < self.minOffset: self.minOffset = component.computedPosition[1]
        if component.computedPosition[1]+component.computedHeight > self.maxOffset: self.maxOffset = component.computedPosition[1]+component.computedHeight
        self.container.addChild(component)
        self.scrollIndicator.update()

    def removeChild(self, component):
        self.container.removeChild(component)
        if component.computedPosition[1] == self.minOffset:
            self.minOffset = 0
            for comp in self.container.childComponents:
                if comp.computedPosition[1] < self.minOffset: self.minOffset = comp.computedPosition[1]
        if component.computedPosition[1] == self.maxOffset:
            self.maxOffset = self.computedHeight
            for comp in self.container.childComponents:
                if comp.computedPosition[1]+comp.computedHeight > self.maxOffset: self.maxOffset = comp.computedPosition[1]+comp.computedHeight
        self.scrollIndicator.update()

    def clearChildren(self):
        self.container.clearChildren()
        self.maxOffset = self.computedHeight
        self.offset = 0
        self.scrollIndicator.update()

    def render(self, largerSurface):
        super(ScrollableContainer, self).render(largerSurface)

    def refresh(self, children=True):
        #super(ScrollableContainer, self).refresh()
        self.minOffset = 0
        for comp in self.container.childComponents:
            if comp.computedPosition[1] < self.minOffset: self.minOffset = comp.computedPosition[1]
        self.maxOffset = self.computedHeight
        for comp in self.container.childComponents:
            if comp.computedPosition[1]+comp.computedHeight > self.maxOffset: self.maxOffset = comp.computedPosition[1]+comp.computedHeight
        self.scrollIndicator.update()
        self.container.refresh(children)
