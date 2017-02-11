import os

import pygame
from pyos.gui.longclickevent import LongClickEvent
from pyos.gui.intermediateupdateevent import IntermediateUpdateEvent
from pyos.state import State

class EventQueue(object):
    def __init__(self):
        self.events = []

    def check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                State.instance().getThreadController().stopAllThreads()
                pygame.quit()
                os._exit(1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.events.append(LongClickEvent(event))
            if event.type == pygame.MOUSEMOTION and len(self.events) > 0 and isinstance(self.events[len(self.events)-1], LongClickEvent):
                self.events[len(self.events)-1].intermediateUpdate(event)
            if event.type == pygame.MOUSEBUTTONUP and len(self.events) > 0 and isinstance(self.events[len(self.events)-1], LongClickEvent):
                self.events[len(self.events)-1].end(event)
                if not self.events[len(self.events)-1].checkValidLongClick():
                    self.events[len(self.events)-1] = self.events[len(self.events)-1].mouseUp

    def getLatest(self):
        if len(self.events) == 0: return None
        return self.events.pop()

    def removeEvent(self, ev):
        if ev in self.events:
            self.events.remove(ev)

    def getLatestComplete(self):
        if len(self.events) == 0: return None
        p = len(self.events) - 1
        while p >= 0:
            event = self.events[p]
            if isinstance(event, LongClickEvent):
                if event.mouseUp != None:
                    return self.events.pop(p)
                else:
                    return IntermediateUpdateEvent(self.events[len(self.events) - 1].getLatestUpdate(), self.events[len(self.events) - 1])
            else:
                return self.events.pop(p)
            p -= 1

    def clear(self):
        self.events = []