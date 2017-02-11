from pyos.gui.component import Component
from pyos.state import State


class Container(Component):
    def __init__(self, position, **data):
        super(Container, self).__init__(position, **data)
        self.transparent = False
        self.backgroundColor = (0, 0, 0)
        self.childComponents = []
        self.SKIP_CHILD_CHECK = False
        self.transparent = data.get("transparent", False)
        self.backgroundColor = data.get("color", State.instance().getColorPalette().getColor("background"))
        if "children" in data: self.childComponents = data["children"]

    def addChild(self, component):
        if self.resizable and "resizeble" not in component.data:
            component.resizable = True
            component.refresh()
        self.childComponents.append(component)

    def addChildren(self, *children):
        for child in children:
            self.addChild(child)

    def removeChild(self, component):
        self.childComponents.remove(component)

    def clearChildren(self):
        for component in self.childComponents:
            self.removeChild(component)
        self.childComponents = []

    def getClickedChild(self, mouseEvent, offsetX=0, offsetY=0):
        currChild = len(self.childComponents)
        while currChild > 0:
            currChild -= 1
            child = self.childComponents[currChild]
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

    def getChildAt(self, position):
        for child in self.childComponents:
            if child.computedPosition == list(position):
                return child
        return None

    def render(self, largerSurface):
        if self.surface.get_locked(): return
        if not self.transparent:
            self.surface.fill(self.backgroundColor)
        else:
            self.surface.fill((0, 0, 0, 0))
        for child in self.childComponents:
            child.render(self.surface)
        super(Container, self).render(largerSurface)

    def refresh(self, children=True):
        super(Container, self).refresh()
        if children:
            for child in self.childComponents:
                child.refresh()
