from pyos.gui.button import Button
from pyos.gui.buttonrow import ButtonRow
from pyos.gui.container import Container
from pyos.gui.multilinetext import MultiLineText
from pyos.gui.overlay import Overlay
from pyos.gui.textentryfield import TextEntryField
from pyos.state import State

class Dialog(Overlay):
    def __init__(self, title, text, actionButtons, onResponseRecorded=None, onResponseRecordedData=(), **data):
        super(Dialog, self).__init__((0, (State.instance().getActiveApplication().ui.height/2)-65), height=data.get("height", 130),
                                         width=data.get("width", State.instance().getGUI().width),
                                         color=data.get("color", State.instance().getColorPalette().getColor("background")))
        self.container.border = 3
        self.container.borderColor = State.instance().getColorPalette().getColor("item")
        self.container.refresh()
        self.application = State.instance().getActiveApplication()
        self.title = title
        self.text = text
        self.response = None
        self.buttonList = Dialog.getButtonList(actionButtons, self) if type(actionButtons[0]) == str else actionButtons
        self.textComponent = MultiLineText((2, 2), self.text, State.instance().getColorPalette().getColor("item"), 16, width=self.container.computedWidth-4, height=96)
        self.buttonRow = ButtonRow((0, 96), width=State.instance().getGUI().width, height=40, color=(0, 0, 0, 0), padding=0, margin=0)
        for button in self.buttonList:
            self.buttonRow.addChild(button)
        self.addChild(self.textComponent)
        self.addChild(self.buttonRow)
        self.onResponseRecorded = onResponseRecorded
        self.onResponseRecordedData = onResponseRecordedData

    def display(self):
        State.instance().getFunctionBar().app_title_text.setText(self.title)
        self.application.ui.setDialog(self)

    def hide(self):
        State.instance().getFunctionBar().app_title_text.setText(State.instance().getActiveApplication().title)
        self.application.ui.clearDialog()
        self.application.ui.refresh()

    def recordResponse(self, response):
        self.response = response
        self.hide()
        if self.onResponseRecorded != None:
            if self.onResponseRecordedData != None:
                self.onResponseRecorded(*((self.onResponseRecordedData)+(self.response,)))

    def getResponse(self):
        return self.response

    @staticmethod
    def getButtonList(titles, dialog):
        blist = []
        for title in titles:
            blist.append(Button((0, 0), title, State.instance().getColorPalette().getColor("item"), State.instance().getColorPalette().getColor("background"), 18,
                                    width=dialog.container.computedWidth/len(titles), height=40,
                                    onClick=dialog.recordResponse, onClickData=(title,)))
        return blist


class OKDialog(Dialog):
    def __init__(self, title, text, onResposeRecorded=None, onResponseRecordedData=()):
        okbtn = Button((0,0), "OK", State.instance().getColorPalette().getColor("item"), State.instance().getColorPalette().getColor("background"), 18,
                           width=State.instance().getGUI().width, height=40, onClick=self.recordResponse, onClickData=("OK",))
        super(OKDialog, self).__init__(title, text, [okbtn], onResposeRecorded)


class ErrorDialog(Dialog):
    def __init__(self, text, onResposeRecorded=None, onResponseRecordedData=()):
        okbtn = Button((0,0), "Acknowledged", State.instance().getColorPalette().getColor("item"), State.instance().getColorPalette().getColor("background"), 18,
                           width=State.instance().getGUI().width, height=40, onClick=self.recordResponse, onClickData=("Acknowledged",))
        super(ErrorDialog, self).__init__("Error", text, [okbtn], onResposeRecorded)
        self.container.backgroundColor = State.instance().getColorPalette().getColor("error")


class WarningDialog(Dialog):
    def __init__(self, text, onResposeRecorded=None, onResponseRecordedData=()):
        okbtn = Button((0,0), "OK", State.instance().getColorPalette().getColor("item"), State.instance().getColorPalette().getColor("background"), 18,
                           width=State.instance().getGUI().width, height=40, onClick=self.recordResponse, onClickData=("OK",))
        super(WarningDialog, self).__init__("Warning", text, [okbtn], onResposeRecorded)
        self.container.backgroundColor = State.instance().getColorPalette().getColor("warning")


class YNDialog(Dialog):
    def __init__(self, title, text, onResponseRecorded=None, onResponseRecordedData=()):
        ybtn = Button((0,0), "Yes", (200, 250, 200), (50, 50, 50), 18,
                           width=(State.instance().getGUI().width/2), height=40, onClick=self.recordResponse, onClickData=("Yes",))
        nbtn = Button((0,0), "No", State.instance().getColorPalette().getColor("item"), State.instance().getColorPalette().getColor("background"), 18,
                           width=(State.instance().getGUI().width/2), height=40, onClick=self.recordResponse, onClickData=("No",))
        super(YNDialog, self).__init__(title, text, [ybtn, nbtn], onResponseRecorded)
        self.onResponseRecordedData = onResponseRecordedData


class OKCancelDialog(Dialog):
    def __init__(self, title, text, onResponseRecorded=None, onResponseRecordedData=()):
        okbtn = Button((0,0), "OK", State.instance().getColorPalette().getColor("background"), State.instance().getColorPalette().getColor("item"), 18,
                           width=State.instance().getGUI().width/2, height=40, onClick=self.recordResponse, onClickData=("OK",))
        cancbtn = Button((0,0), "Cancel", State.instance().getColorPalette().getColor("item"), State.instance().getColorPalette().getColor("background"), 18,
                           width=State.instance().getGUI().width/2, height=40, onClick=self.recordResponse, onClickData=("Cancel",))
        super(OKCancelDialog, self).__init__(title, text, [okbtn, cancbtn], onResponseRecorded, onResponseRecordedData)


class AskDialog(Dialog):
    def __init__(self, title, text, onResposeRecorded=None, onResponseRecordedData=()):
        okbtn = Button((0,0), "OK", State.instance().getColorPalette().getColor("background"), State.instance().getColorPalette().getColor("item"), 18,
                           width=State.instance().getGUI().width/2, height=40, onClick=self.returnRecordedResponse)
        cancelbtn = Button((0,0), "Cancel", State.instance().getColorPalette().getColor("item"), State.instance().getColorPalette().getColor("background"), 18,
                           width=State.instance().getGUI().width/2, height=40, onClick=self.recordResponse, onClickData=("Cancel",))
        super(AskDialog, self).__init__(title, text, [okbtn, cancelbtn], onResposeRecorded, onResponseRecordedData)
        self.textComponent.computedHeight -= 20
        self.textComponent.refresh()
        self.textEntryField = TextEntryField((0, 80), width=self.container.computedWidth, height=20)
        self.container.addChild(self.textEntryField)

    def returnRecordedResponse(self):
        self.recordResponse(self.textEntryField.getText())


class CustomContentDialog(Dialog):
    def __init__(self, title, customComponent, actionButtons, onResponseRecorded=None, btnPad=0, btnMargin=5, **data):
        self.application = State.instance().getActiveApplication()
        self.title = title
        self.response = None
        self.baseContainer = Container((0, 0), width=State.instance().getGUI().width, height=State.instance().getActiveApplication().ui.height, color=(0, 0, 0, 0.5))
        self.container = customComponent
        self.buttonList = Dialog.getButtonList(actionButtons, self) if type(actionButtons[0]) == str else actionButtons
        self.buttonRow = ButtonRow((0, self.container.computedHeight-33), width=self.container.computedWidth, height=40, color=(0, 0, 0, 0), padding=btnPad, margin=btnMargin)
        for button in self.buttonList:
            self.buttonRow.addChild(button)
        self.container.addChild(self.buttonRow)
        self.baseContainer.addChild(self.container)
        self.onResponseRecorded = onResponseRecorded
        self.data = data
        self.onResponseRecordedData = data.get("onResponseRecordedData", ())
