from pyos.state import State
from pyos.gui.listscrollablecontainer import ListScrollableContainer
from pyos.gui.textentryfield import TextEntryField


class MultiLineTextEntryField(ListScrollableContainer):
    def __init__(self, position, initialText="", **data):
        if "border" not in data:
            data["border"] = 1
            data["borderColor"] = State.instance().getColorPalette().getColor("accent")
        data["onClick"] = self.activateLast
        data["onClickData"] = ()
        super(MultiLineTextEntryField, self).__init__(position, **data)
        self.lineHeight = data.get("lineHeight", 20)
        self.maxLines = data.get("maxLines", -2)
        self.backgroundColor = data.get("backgroundColor", State.instance().getColorPalette().getColor("background"))
        self.textColor = data.get("color", State.instance().getColorPalette().getColor("item"))
        self.textFields = []
        self.wrappedLines = []
        self.currentField = -1
        self.setText(initialText)

    def activateLast(self):
        self.currentField = len(self.textFields) - 1
        self.textFields[self.currentField].activate()

    def refresh(self):
        super(MultiLineTextEntryField, self).refresh()
        self.clearChildren()
        for tf in self.textFields:
            self.addChild(tf)

    def setCurrent(self, field):
        self.currentField = self.textFields.index(field)

    def addField(self, initial_text):
        if len(self.textFields) == self.maxLines:
            return
        field = TextEntryField((0, 0), initial_text, width=self.container.computedWidth, height=self.lineHeight,
                                   backgroundColor=self.backgroundColor, textColor=self.textColor)
        field.border = 0
        field.MULTILINE = self
        self.currentField += 1
        self.textFields.insert(self.currentField, field)
        field.activate()
        self.refresh()

#         def prependToNextField(self, text): #HOLD FOR NEXT RELEASE
#             print "Prep: "+text
#             self.currentField += 1
#             currentText = self.textFields[self.currentField].textComponent.text
#             self.textFields[self.currentField].textComponent.text = ""
#             self.textFields[self.currentField].indicatorPosition = 0
#             self.textFields[self.currentField].refresh()
#             self.textFields[self.currentField].activate()
#             for word in (" "+text+" "+currentText).split(" "):
#                 self.textFields[self.currentField].appendChar(word+" ")
#             self.textFields[self.currentField].refresh()

    def removeField(self, field):
        if self.currentField > 0:
            if self.textFields.index(field) == self.currentField:
                self.currentField -= 1
            self.textFields.remove(field)
        self.refresh()

    def getDeleteChar(self):
        if self.currentField < len(self.textFields) - 1:
            c = ""
            try:
                c = self.textFields[self.currentField + 1].textComponent.text[0]
                self.textFields[self.currentField + 1].textComponent.text = self.textFields[self.currentField + 1].textComponent.text[1:]
                self.textFields[self.currentField + 1].updateOverflow()
                self.textFields[self.currentField + 1].refresh()
            except:
                self.removeField(self.textFields[self.currentField + 1])
            return c
        return ""

    def getText(self):
        t = ""
        p = 0
        for ftext in [f.getText() for f in self.textFields]:
            if p in self.wrappedLines:
                t += ftext
            else:
                t += ftext + "\n"
            p += 1
        t.rstrip("\n")
        return t

    def clear(self):
        self.textFields = []
        self.wrappedLines = []
        self.currentField = -1
        self.refresh()

    def setText(self, text):
        self.clear()
        if text == "":
            self.addField("")
        else:
            for line in text.replace("\r", "").split("\n"):
                self.addField("")
                line = line.rstrip()
                words = line.split(" ")
                oldN = self.currentField
                for word in words:
                    self.textFields[self.currentField].appendChar(word)
                    self.textFields[self.currentField].appendChar(" ")
                if oldN != self.currentField:
                    for n in range(oldN, self.currentField): self.wrappedLines.append(n)
            for field in self.textFields:
                if field.overflow > 0:
                    field.textComponent.setText(field.textComponent.text.rstrip(" "))
                    field.updateOverflow()
        self.refresh()
        State.instance().getKeyboard().deactivate()