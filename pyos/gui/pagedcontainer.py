import pyos.gui as gui

from pyos.state import State
from pyos.gui.button import Button
from pyos.gui.container import Container
from pyos.gui.text import Text


class PagedContainer(Container):
    def __init__(self, position, **data):
        super(PagedContainer, self).__init__(position, **data)
        self.pages = data.get("pages", [])
        self.currentPage = 0
        self.hideControls = data.get("hideControls", False)
        self.pageControls = Container((0, self.computedHeight-20), color=State.instance().getColorPalette().getColor("background"), width=self.computedWidth, height=20)
        self.pageLeftButton = Button((0, 0), " < ", State.instance().getColorPalette().getColor("item"), State.instance().getColorPalette().getColor("accent"),
                                        16, width=40, height=20, onClick=self.pageLeft, onLongClick=self.goToPage)
        self.pageRightButton = Button((self.computedWidth-40, 0), " > ", State.instance().getColorPalette().getColor("item"), State.instance().getColorPalette().getColor("accent"),
                                        16, width=40, height=20, onClick=self.pageRight, onLongClick=self.goToLastPage)
        self.pageIndicatorText = Text((0, 0), str(self.currentPage + 1)+" of "+str(len(self.pages)), State.instance().getColorPalette().getColor("item"),
                                        16)
        self.pageHolder = Container((0, 0), color=State.instance().getColorPalette().getColor("background"), width=self.computedWidth, height=(self.computedHeight-20 if not self.hideControls else self.computedHeight))
        self.pageIndicatorText.position[0] = gui.core.getCenteredCoordinates(self.pageIndicatorText, self.pageControls)[0]
        super(PagedContainer, self).addChild(self.pageHolder)
        self.pageControls.addChild(self.pageLeftButton)
        self.pageControls.addChild(self.pageIndicatorText)
        self.pageControls.addChild(self.pageRightButton)
        if not self.hideControls:
            super(PagedContainer, self).addChild(self.pageControls)

    def addPage(self, page):
        self.pages.append(page)
        self.pageIndicatorText.text = str(self.currentPage + 1)+" of "+str(len(self.pages))
        self.pageIndicatorText.refresh()

    def getPage(self, number):
        return self.pages[number]

    def pageLeft(self):
        if self.currentPage >= 1:
            self.goToPage(self.currentPage - 1)

    def pageRight(self):
        if self.currentPage < len(self.pages) - 1:
            self.goToPage(self.currentPage + 1)

    def goToPage(self, number=0):
        self.currentPage = number
        self.pageHolder.clearChildren()
        self.pageHolder.addChild(self.getPage(self.currentPage))
        self.pageIndicatorText.setText(str(self.currentPage + 1)+" of "+str(len(self.pages)))
        self.pageIndicatorText.refresh()

    def goToLastPage(self): self.goToPage(len(self.pages) - 1)

    def getLastPage(self):
        return self.pages[len(self.pages) - 1]

    def generatePage(self, **data):
        if "width" not in data: data["width"] = self.pageHolder.computedWidth
        if "height" not in data: data["height"] = self.pageHolder.computedHeight
        data["isPage"] = True
        return Container((0, 0), **data)

    def addChild(self, component):
        if self.pages == []:
            self.addPage(self.generatePage(color=self.backgroundColor, width=self.pageHolder.computedWidth, height=self.pageHolder.computedHeight))
        self.getLastPage().addChild(component)

    def removeChild(self, component):
        self.pages[self.currentPage].removeChild(component)
        childrenCopy = self.pages[self.currentPage].childComponents[:]
        for page in self.pages:
            for child in page.childComponents:
                page.removeChild(child)
        for child in childrenCopy:
            self.addChild(child)

    def removePage(self, page):
        if type(page) == int:
            self.pages.pop(page)
        else:
            self.pages.remove(page)
        if self.currentPage >= len(self.pages):
            self.goToPage(self.currentPage - 1)

    def clearChildren(self):
        self.pages = []
        self.addPage(self.generatePage(color=self.backgroundColor))
        self.goToPage()