from pyos.gui.scrollablecontainer import ScrollableContainer


class ListScrollableContainer(ScrollableContainer):
    def __init__(self, position, **data):
        self.margin = data.get("margin", 0)
        super(ListScrollableContainer, self).__init__(position, **data)

    def getCumulativeHeight(self):
        height = 0
        if self.container.childComponents == []: 0
        for component in self.container.childComponents:
            height += component.computedHeight + self.margin
        return height

    def addChild(self, component):
        component.position[1] = self.getCumulativeHeight()
        component.setDimensions()
        super(ListScrollableContainer, self).addChild(component)

    def removeChild(self, component):
        super(ListScrollableContainer, self).removeChild(component)
        childrenCopy = self.container.childComponents[:]
        self.container.childComponents = []
        for child in childrenCopy:
            self.addChild(child)
