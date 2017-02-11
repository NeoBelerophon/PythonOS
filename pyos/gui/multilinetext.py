from pyos.gui.component import Component
import pygame
import pyos.gui as gui
from pyos.state import State


class MultiLineText(Component):
    @staticmethod
    def render_textrect(string, font, rect, text_color, background_color, justification, use_ft):
        final_lines = []
        requested_lines = string.splitlines()
        err = None
        for requested_line in requested_lines:
            if font.size(requested_line)[0] > rect.width:
                words = requested_line.split(' ')
                for word in words:
                    if font.size(word)[0] >= rect.width:
                        # print "The word " + word + " is too long to fit in the rect passed."
                        err = 0
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    if font.size(test_line)[0] < rect.width:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        surface.fill(background_color)
        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + font.size(line)[1] >= rect.height:
                err = 1
            if line != "":
                tempsurface = None
                if use_ft:
                    tempsurface = font.render(line, text_color)
                else:
                    tempsurface = font.render(line, 1, text_color)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    print "Invalid justification argument: " + str(justification)
                    err = 2
            accumulated_height += font.size(line)[1]
        return (surface, err, final_lines)

    def __init__(self, position, text, color=gui.DEFAULT, size=gui.DEFAULT, justification=gui.DEFAULT, **data):
        #Defaults are "item", and 0 (left).
        color, size, justification = Component.default(color, State.instance().getColorPalette().getColor("item"), size, 14,
                                                     justification, 0)
        self.justification = justification
        self.color = color
        self.size = size
        self.text = text if type(text) == str or type(text) == unicode else str(text)
        self.textSurface = None
        self.font = data.get("font", State.instance().getFont())
        self.use_freetype = data.get("freetype", False)
        super(MultiLineText, self).__init__(position, **data)
        self.refresh()
        if self.width > State.instance().getGUI().width:
            self.width = State.instance().getGUI().width

    def getRenderedText(self):
        return MultiLineText.render_textrect(self.text, self.font.get(self.size, self.use_freetype), pygame.Rect(0, 0, self.computedWidth, self.computedHeight),
                                                 self.color, (0, 0, 0, 0), self.justification, self.use_freetype)[0]

    def refresh(self):
        super(MultiLineText, self).refresh()
        self.textSurface = self.getRenderedText()
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.textSurface, (0, 0))

    def setText(self, text):
        self.text = text if type(text) == str or type(text) == unicode else str(text)
        self.setDimensions()
        self.refresh()
