import pygame
import os
import json


class Icons(object):
        def __init__(self):
            self.rootPath = "res/icons/"
            self.icons = {
                     "menu": "menu.png",
                     "unknown": "unknown.png",
                     "error": "error.png",
                     "warning": "warning.png",
                     "file": "file.png",
                     "folder": "folder.png",
                     "wifi": "wifi.png",
                     "python": "python.png",
                     "quit": "quit.png",
                     "copy": "files_copy.png",
                     "delete": "files_delete.png",
                     "goto": "files_goto.png",
                     "home_dir": "files_home.png",
                     "move": "files_move.png",
                     "select": "files_select.png",
                     "up": "files_up.png",
                     "back": "back.png",
                     "forward": "forward.png",
                     "search": "search.png",
                     "info": "info.png",
                     "open": "open.png",
                     "save": "save.png"
                     }

        def getIcons(self):
            return self.icons

        def getRootPath(self):
            return self.rootPath

        def getLoadedIcon(self, icon, folder=""):
            try:
                return pygame.image.load(os.path.join(self.rootPath, self.icons[icon]))
            except:
                if os.path.exists(icon):
                    return pygame.transform.scale(pygame.image.load(icon), (40, 40))
                if os.path.exists(os.path.join("res/icons/", icon)):
                    return pygame.transform.scale(pygame.image.load(os.path.join("res/icons/", icon)), (40, 40))
                if os.path.exists(os.path.join(folder, icon)):
                    return pygame.transform.scale(pygame.image.load(os.path.join(folder, icon)), (40, 40))
                return pygame.image.load(os.path.join(self.rootPath, self.icons["unknown"]))

        @staticmethod
        def loadFromFile(path):
            f = open(path, "rU")
            icondata = json.load(f)
            toreturn = Icons()
            for key in dict(icondata).keys():
                toreturn.icons[key] = icondata.get(key)
            f.close()
            return toreturn