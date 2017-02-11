from pyos.gui.pagedcontainer import PagedContainer


class GriddedPagedContainer(PagedContainer):
    def __init__(self, position, rows=5, columns=4, **data):
        self.padding = 5
        if "padding" in data: self.padding = data["padding"]
        self.rows = rows
        self.columns = columns
        super(PagedContainer, self).__init__(position, **data)
        self.perRow = ((self.computedHeight-20)-(2*self.padding)) / rows
        self.perColumn = (self.computedWidth-(2*self.padding)) / columns
        super(GriddedPagedContainer, self).__init__(position, **data)

    def isPageFilled(self, number):
        if type(number) == int:
            return len(self.pages[number].childComponents) == (self.rows * self.columns)
        else:
            return len(number.childComponents) == (self.rows * self.columns)

    def addChild(self, component):
        if self.pages == [] or self.isPageFilled(self.getLastPage()):
            self.addPage(self.generatePage(color=self.backgroundColor))
        newChildPosition = [self.padding, self.padding]
        if self.getLastPage().childComponents == []:
            component.setPosition(newChildPosition)
            self.getLastPage().addChild(component)
            return
        lastChildPosition = self.getLastPage().childComponents[len(self.getLastPage().childComponents) - 1].computedPosition[:]
        if lastChildPosition[0] < self.padding + (self.perColumn * (self.columns - 1)):
            newChildPosition = [lastChildPosition[0]+self.perColumn, lastChildPosition[1]]
        else:
            newChildPosition = [self.padding, lastChildPosition[1]+self.perRow]
        component.setPosition(newChildPosition)
        self.getLastPage().addChild(component)
