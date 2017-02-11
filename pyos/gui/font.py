import pygame


class Font(object):
    def __init__(self, path="res/RobotoCondensed-Regular.ttf", minSize=10, maxSize=30):
        self.path = path
        curr_size = minSize
        self.sizes = {}
        self.ft_support = True
        self.ft_sizes = {}
        while curr_size <= maxSize:
            if self.ft_support:
                try:
                    self.ft_sizes[curr_size] = pygame.freetype.Font(path, curr_size)
                except:
                    self.ft_support = False
            self.sizes[curr_size] = pygame.font.Font(path, curr_size)
            curr_size += 1

    def get(self, size=14, ft=False):
        if ft and self.ft_support:
            if size not in self.ft_sizes:
                self.ft_sizes[size] = pygame.freetype.Font(self.path, size)
            return self.ft_sizes[size]
        else:
            if size not in self.sizes:
                self.sizes[size] = pygame.font.Font(self.path, size)
            return self.sizes[size]