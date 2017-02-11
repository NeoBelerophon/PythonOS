from pyos.gui.pagedcontainer import PagedContainer


class ListPagedContainer(PagedContainer):
    def __init__(self, position, **data):
        self.padding = data.get("padding", 0)
        self.margin = data.get("margin", 0)
        super(ListPagedContainer, self).__init__(position, **data)

    def getHeightOfComponents(self):
        height = self.padding
        if not self.pages: return self.padding
        for component in self.getLastPage().childComponents:
            height += component.computedHeight + (2 * self.margin)
        return height

    def addChild(self, component):
        componentHeight = self.getHeightOfComponents()
        if self.pages == [] or componentHeight + (component.computedHeight + 2 * self.margin) + (
                    2 * self.padding) >= self.pageHolder.computedHeight:
            self.addPage(self.generatePage(color=self.backgroundColor))
            componentHeight = self.getHeightOfComponents()
        component.setPosition([self.padding, componentHeight])
        self.getLastPage().addChild(component)
        component.refresh()

    def removeChild(self, component):
        super(ListPagedContainer, self).removeChild(component)
        if not self.pages[0].childComponents:
            self.removePage(0)
            self.goToPage()
