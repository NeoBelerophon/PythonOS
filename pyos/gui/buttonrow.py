from pyos.gui.container import Container


class ButtonRow(Container):
    def __init__(self, position, **data):
        self.padding = data.get("padding", 0)
        self.margin = data.get("margin", 0)
        super(ButtonRow, self).__init__(position, **data)

    def getLastComponent(self):
        if len(self.childComponents) > 0:
            return self.childComponents[len(self.childComponents) - 1]
        return None

    def addChild(self, component):
        component.height = self.computedHeight - (2 * self.padding)
        last = self.getLastComponent()
        if last is not None:
            component.setPosition([last.computedPosition[0] + last.computedWidth + self.margin, self.padding])
        else:
            component.setPosition([self.padding, self.padding])
        component.setDimensions()
        super(ButtonRow, self).addChild(component)

    def removeChild(self, component):
        super(ButtonRow, self).removeChild(component)
        childrenCopy = self.childComponents[:]
        self.clearChildren()
        for child in childrenCopy:
            self.addChild(child)
