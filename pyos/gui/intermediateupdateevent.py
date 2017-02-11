class IntermediateUpdateEvent(object):
    def __init__(self, pos, src):
        self.pos = pos
        self.sourceEvent = src