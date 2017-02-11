from datetime import datetime


class LongClickEvent(object):
    def __init__(self, mouseDown):
        self.mouseDown = mouseDown
        self.mouseDownTime = datetime.now()
        self.mouseUp = None
        self.mouseUpTime = None
        self.intermediatePoints = []
        self.pos = self.mouseDown.pos

    def intermediateUpdate(self, mouseMove):
        if self.mouseUp is None and (len(self.intermediatePoints) == 0 or mouseMove.pos != self.intermediatePoints[-1]):
            self.intermediatePoints.append(mouseMove.pos)

    def end(self, mouseUp):
        self.mouseUp = mouseUp
        self.mouseUpTime = datetime.now()
        self.pos = self.mouseUp.pos

    def getLatestUpdate(self):
        if len(self.intermediatePoints) == 0: return self.pos
        else: return self.intermediatePoints[len(self.intermediatePoints) - 1]

    def checkValidLongClick(self, time=300): # Checks timestamps against parameter (in milliseconds)
        delta = self.mouseUpTime - self.mouseDownTime
        return (delta.microseconds / 1000) >= time
