# -*- coding: utf-8 -*-

'''
Created on Dec 27, 2015

@author: Adam Furman
@copyright: MIT License
'''

from pyos.io import readJSON
from pyos.state import State

try:
    import pygame.freetype
except ImportError:
    pass


if __name__ == "__main__":
    try:
        settings = readJSON("res/settings.json")
    except:
        print "Error loading settings from res/settings.json"

    # TEST
    # State.state_shell()
    for app in state.getApplicationList().getApplicationList():
        if app.evtHandlers.get("onOSLaunch", None) != None:
            try:
                app.evtHandlers.get("onOSLaunch")()
            except:
                State.error_recovery("App startup task failed to run properly.", "App: " + str(app.name))
    state.getApplicationList().getApp("home").activate()
    try:
        State.main()
    except:
        State.error_recovery("Fatal system error.")
