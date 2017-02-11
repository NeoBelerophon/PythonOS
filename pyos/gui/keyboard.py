# -*- coding: utf-8 -*-

from pyos.gui.container import Container
from pyos.gui.keyboardbutton import KeyboardButton
from pyos.state import State
from pyos.gui.font import Font


class Keyboard(object):
    def __init__(self, textEntryField=None):
        self.shiftUp = False
        self.active = False
        self.textEntryField = textEntryField
        self.movedUI = False
        self._symbolFont = Font("res/symbols.ttf", 10, 20)
        if self.textEntryField.computedPosition[1] + self.textEntryField.computedHeight > 2*(State.instance().getGUI().height/3) or self.textEntryField.data.get("slideUp", False):
            State.instance().getActiveApplication().ui.setPosition((0, -80))
            self.movedUI = True
        self.baseContainer = None
        self.baseContainer = Container((0, 0), width=State.instance().getGUI().width, height=State.instance().getGUI().height/3)
        self.baseContainer.setPosition((0, 2*(State.instance().getGUI().height/3)))
        self.keyWidth = self.baseContainer.computedWidth / 10
        self.keyHeight = self.baseContainer.computedHeight / 4
        use_ft = State.instance().getTypingFont().ft_support
        # if use_ft:
        self.shift_sym = u"⇧"
        self.enter_sym = u"⏎"
        self.bkspc_sym = u"⌫"
        self.delet_sym = u"⌦"
#             else:
#                 self.shift_sym = "sh"
#                 self.enter_sym = "->"
#                 self.bkspc_sym = "<-"
#                 self.delet_sym = "del"
        self.keys1 = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
                     ["a", "s", "d", "f", "g", "h", "j", "k", "l", self.enter_sym],
                     [self.shift_sym, "z", "x", "c", "v", "b", "n", "m", ",", "."],
                     ["!", "?", " ", "", "", "", "", "-", "'", self.bkspc_sym]]
        self.keys2 = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                     ["@", "#", "$", "%", "^", "&", "*", "(", ")", "_"],
                     ["=", "+", "\\", "/", "<", ">", "|", "[", "]", ":"],
                     [";", "{", "}", "", "", "", "", "-", "\"", self.delet_sym]]
        row = 0
        for symrow in self.keys1:
            sym = 0
            for symbol in symrow:
                button = None
                if symbol == "":
                    sym += 1
                    continue
                if symbol == " ":
                    button = KeyboardButton((sym * self.keyWidth, row * self.keyHeight), "", self.keys2[row][sym],
                                                onClick=self.insertChar, onClickData=(self.keys1[row][sym],),
                                                onLongClick=self.insertChar, onLongClickData=(self.keys2[row][sym],),
                                                width=self.keyWidth*5, height=self.keyHeight, freetype=use_ft)
                else:
                    if symbol == self.shift_sym or symbol == self.enter_sym or symbol == self.bkspc_sym or symbol == self.delet_sym:
                        button = KeyboardButton((sym * self.keyWidth, row * self.keyHeight), self.keys1[row][sym], self.keys2[row][sym],
                                                onClick=self.insertChar, onClickData=(self.keys1[row][sym],),
                                                onLongClick=self.insertChar, onLongClickData=(self.keys2[row][sym],),
                                                width=self.keyWidth, height=self.keyHeight, border=1, borderColor=State.instance().getColorPalette().getColor("accent"),
                                                font=self._symbolFont, freetype=use_ft)
                    else:
                        button = KeyboardButton((sym * self.keyWidth, row * self.keyHeight), self.keys1[row][sym], self.keys2[row][sym],
                                                    onClick=self.insertChar, onClickData=(self.keys1[row][sym],),
                                                    onLongClick=self.insertChar, onLongClickData=(self.keys2[row][sym],),
                                                    width=self.keyWidth, height=self.keyHeight,
                                                    freetype=use_ft)
                self.baseContainer.addChild(button)
                sym += 1
            row += 1

    def deactivate(self):
        self.active = False
        if self.movedUI:
            State.instance().getActiveApplication().ui.position[1] = 0
        self.textEntryField = None

    def setTextEntryField(self, field):
        self.textEntryField = field
        self.active = True
        if self.textEntryField.computedPosition[1] + self.textEntryField.height > State.instance().getGUI().height - self.baseContainer.computedHeight or self.textEntryField.data.get("slideUp", False):
            State.instance().getActiveApplication().ui.setPosition((0, -self.baseContainer.computedHeight))
            self.movedUI = True

    def getEnteredText(self):
        return self.textEntryField.getText()

    def insertChar(self, char):
        if char == self.shift_sym:
            self.shiftUp = not self.shiftUp
            for button in self.baseContainer.childComponents:
                if self.shiftUp:
                    button.primaryTextComponent.text = button.primaryTextComponent.text.upper()
                else:
                    button.primaryTextComponent.text = button.primaryTextComponent.text.lower()
                button.primaryTextComponent.refresh()
            return
        if char == self.enter_sym:
            mult = self.textEntryField.MULTILINE
            self.deactivate()
            if mult != None:
                mult.textFields[mult.currentField].doBlink = False
                mult.addField("")
            return
        if char == self.bkspc_sym:
            self.textEntryField.backspace()
            return
        if char == self.delet_sym:
            self.textEntryField.delete()
        else:
            if self.shiftUp:
                self.textEntryField.appendChar(char.upper())
                self.shiftUp = False
                for button in self.baseContainer.childComponents:
                    button.primaryTextComponent.text = button.primaryTextComponent.text.lower()
                    button.primaryTextComponent.refresh()
            else:
                self.textEntryField.appendChar(char)

    def render(self, largerSurface):
        self.baseContainer.render(largerSurface)
