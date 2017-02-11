import json


class ColorPalette(object):
        def __init__(self):
            self.palette = {
                       "normal": {
                                  "background": (200, 200, 200),
                                  "item": (20, 20, 20),
                                  "accent": (100, 100, 200),
                                  "warning": (250, 160, 45),
                                  "error": (250, 50, 50)
                                  },
                       "dark": {
                                "background": (50, 50, 50),
                                "item": (220, 220, 220),
                                "accent": (50, 50, 150),
                                "warning": (200, 110, 0),
                                "error": (200, 0, 0)
                                },
                       "light": {
                                 "background": (250, 250, 250),
                                 "item": (50, 50, 50),
                                 "accent": (150, 150, 250),
                                 "warning": (250, 210, 95),
                                 "error": (250, 100, 100)
                                 }
                       }
            self.scheme = "normal"

        def getPalette(self):
            return self.palette

        def getScheme(self):
            return self.scheme

        def getColor(self, item):
            if item.find(":") == -1:
                return self.palette[self.scheme][item]
            else:
                split = item.split(":")
                cadd = lambda c, d: (c[0]+d[0], c[1]+d[1], c[2]+d[2])
                if split[0] == "darker":
                    return max(cadd(self.getColor(split[1]), (-20, -20, -20)), (0, 0, 0))
                if split[0] == "dark":
                    return max(cadd(self.getColor(split[1]), (-40, -40, -40)), (0, 0, 0))
                if split[0] == "lighter":
                    return min(cadd(self.getColor(split[1]), (20, 20, 20)), (250, 250, 250))
                if split[0] == "light":
                    return min(cadd(self.getColor(split[1]), (40, 40, 40)), (250, 250, 250))
                if split[0] == "transparent":
                    return self.getColor(split[1]) + (int(split[2].rstrip("%"))/100,)

        def __getitem__(self, item):
            return self.getColor(item)

        def setScheme(self, scheme="normal"):
            self.scheme = scheme

        @staticmethod
        def loadFromFile(path):
            f = open(path, "rU")
            colordata = json.load(f)
            toreturn = ColorPalette()
            for key in dict(colordata).keys():
                toreturn.palette[key] = colordata.get(key)
            f.close()
            return toreturn

        @staticmethod
        def HTMLToRGB(colorstring):
            colorstring = colorstring.strip()
            if colorstring[0] == '#': colorstring = colorstring[1:]
            if len(colorstring) != 6:
                raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
            r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
            r, g, b = [int(n, 16) for n in (r, g, b)]
            return (r, g, b)

        @staticmethod
        def RGBToHTMLColor(rgb_tuple):
            hexcolor = '#%02x%02x%02x' % rgb_tuple
            return hexcolor
