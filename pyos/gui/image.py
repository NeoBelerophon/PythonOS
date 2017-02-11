import pygame
from pyos.gui.component import Component


class Image(Component):
    def __init__(self, position, **data):
        self.path = ""
        self.originalSurface = None
        self.transparent = True
        self.resize_image = data.get("resize_image", True)
        if "path" in data:
            self.path = data["path"]
        else:
            self.path = "surface"
        if "surface" not in data:
            data["surface"] = pygame.image.load(data["path"])
        self.originalSurface = data["surface"]
        self.originalWidth = self.originalSurface.get_width()
        self.originalHeight = self.originalSurface.get_height()
        super(Image, self).__init__(position, **data)
        if self.resize_image: self.setSurface(pygame.transform.scale(self.originalSurface, (self.computedWidth, self.computedHeight)))

    def setImage(self, **data):
        if "path" in data:
            self.path = data["path"]
        else:
            self.path = "surface"
        if "surface" not in data:
            data["surface"] = pygame.image.load(data["path"])
        self.originalSurface = data["surface"]
        if data.get("resize", False):
            self.width = self.originalSurface.get_width()
            self.height = self.originalSurface.get_height()
        self.refresh()

    def refresh(self):
        if self.resize_image:
            self.setSurface(pygame.transform.scale(self.originalSurface, (self.computedWidth, self.computedHeight)))
        else:
            super(Image, self).refresh()
