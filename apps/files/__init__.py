import pyos
from shutil import move, copy2, copytree, rmtree
from sys import platform

application = None
state = None

class Operations:
    @staticmethod
    def copy(srcList, dstDir):
        if not pyos.os.path.isdir(dstDir):
            pyos.GUI.ErrorDialog("The destination you have selected is not a directory").display()
            return
        count = 0
        for src in srcList:
            if src.isFile():
                try:
                    copy2(src.absolutePath, dstDir)
                    count += 1
                except:
                    pyos.GUI.ErrorDialog("Failed to copy a file.").display()
            if src.isDir():
                try:
                    copytree(src.absolutePath, dstDir)
                    count += 1
                except:
                    pyos.GUI.ErrorDialog("Failed to copy a folder.").display()
        state.getNotificationQueue().push(pyos.Notification("Copy Complete", "Finished copying "+str(count)+" items."))
        
    @staticmethod
    def move(srcList, dstDir):
        if not pyos.os.path.isdir(dstDir):
            pyos.GUI.ErrorDialog("The destination you have selected is not a directory").display()
            return
        count = 0
        for src in srcList:
            if src.isFile():
                try:
                    move(src.absolutePath, dstDir)
                    count += 1
                except:
                    pyos.GUI.ErrorDialog("Failed to move a file.").display()
            if src.isDir():
                try:
                    copytree(src.absolutePath, dstDir)
                    rmtree(src.absolutePath)
                    count += 1
                except:
                    pyos.GUI.ErrorDialog("Failed to move a folder.").display()
        state.getNotificationQueue().push(pyos.Notification("Move Complete", "Finished moving "+str(count)+" items."))
        
    @staticmethod
    def delete(items):
        for item in items:
            if item.isFile():
                try:
                    pyos.os.remove(item.absolutePath)
                except:
                    pyos.GUI.ErrorDialog("Failed to remove a file.").display()
            if item.isDir():
                try:
                    rmtree(item.absolutePath)
                except:
                    pyos.GUI.ErrorDialog("Failed to remove a folder.").display()
                    
class ApplicationSupport(object):
    def __init__(self):
        self.applications = {}
        for app in state.getApplicationList().getApplicationList():
            if "file" in app.parameters:
                self.applications[app] = app.parameters["file"]
        self.currentlySelected = None
        self.selectionDialog = None
    
    def getSuitableApps(self, ftype):
        suitable = []
        for app, data in self.applications.iteritems():
            if ftype in data:
                suitable.append(app)
        return suitable
    
    def launch(self, path):
        self.cancelLaunch()
        if self.currentlySelected == None:
            self.setCurrentSelection(self.selector.getValue())
        try:
            self.currentlySelected.file = path
            self.currentlySelected.activate()
        except:
            pyos.GUI.ErrorDialog("Unable to launch the requested application").display()
            return
        
    def setCurrentSelection(self, name):
        try:
            self.currentlySelected = [app for app in self.applications.keys() if app.name == name][0]
        except:
            self.currentlySelected = None
            
    def cancelLaunch(self):
        self.selectionDialog.hide()

    def choiceDialog(self, path, short):
        suitable = self.getSuitableApps(path[path.rfind("."):])
        text = pyos.GUI.Text((2, 2), "Select an application to open "+str(short), state.getColorPalette().getColor("item"))
        self.selector = pyos.GUI.Selector((0, 20), [app.name for app in suitable], width=240, height=40,
                                     onValueChanged=self.setCurrentSelection,
                                     border=1, borderColor=state.getColorPalette().getColor("item"))
        cont = pyos.GUI.Container((0, application.ui.height-95), color=state.getColorPalette().getColor("background"), width=240, height=95,
                                  border=1, borderColor=state.getColorPalette().getColor("item"))
        cont.addChild(text)
        cont.addChild(self.selector)
        launchBtn = pyos.GUI.Button((0, 0), "Launch", state.getColorPalette().getColor("item"), state.getColorPalette().getColor("background"), 16,
                                    width=100, height=30, onClick=self.launch, onClickData=(path,))
        cancelBtn = pyos.GUI.Button((0, 0), "Cancel", state.getColorPalette().getColor("item"), state.getColorPalette().getColor("background"), 16,
                                    width=100, height=30, onClick=self.cancelLaunch)
        self.selectionDialog = pyos.GUI.CustomContentDialog("Open With", cont, [launchBtn, cancelBtn])
        self.selectionDialog.display()
        

class FileEntry(pyos.GUI.Container):
    @staticmethod
    def getFileName(absolute):
        return absolute[absolute.rfind("/")+1:]
    
    def __init__(self, position, filepath, **data):
        data["onClickData"] = (self,)
        super(FileEntry, self).__init__(position, **data)
        self.absolutePath = filepath.replace("\\", "/")
        self.shortPath = FileEntry.getFileName(self.absolutePath)
        self.selected = False
        if data.get("selected", False):
            self.toggleSelection()
        self.onSelected = data.get("onSelected", None)
        self.onDeselected = data.get("onDeselected", None)
        
        self.icon = None
        if self.isFile():
            self.icon = pyos.GUI.Image((0, 0), surface=state.getIcons().getLoadedIcon("file"), width=40, height=40,
                                       onClick=self.toggleSelection,
                                       onLongClick=self.eventBindings.get("onClick", pyos.Application.dummy), onLongClickData=(self,))
        if self.isDir():
            self.icon = pyos.GUI.Image((0, 0), surface=state.getIcons().getLoadedIcon("folder"), width=40, height=40,
                                       onClick=self.toggleSelection,
                                       onLongClick=self.eventBindings.get("onClick", pyos.Application.dummy), onLongClickData=(self,))
        self.sizeText = pyos.GUI.Text((self.width-40, 12), self.getSize(), state.getColorPalette().getColor("item"), 16,
                                      onClick=self.eventBindings.get("onClick", pyos.Application.dummy), onClickData=(self,))
        self.text = pyos.GUI.Text((41, 12), self.shortPath, state.getColorPalette().getColor("item"), 16,
                                  onClick=self.eventBindings.get("onClick", pyos.Application.dummy), onClickData=(self,))
        self.addChild(self.icon)
        self.addChild(self.text)
        self.addChild(self.sizeText)
        
    def onSelect(self):
        if self.onSelected != None:
            self.onSelected(self)
    
    def onDeselect(self):
        if self.onDeselected != None:
            self.onDeselected(self)
        
    def isFile(self):
        return pyos.os.path.isfile(self.absolutePath)
    
    def isDir(self):
        return pyos.os.path.isdir(self.absolutePath)
    
    def getSize(self):
        if self.isFile():
            return str(pyos.os.path.getsize(self.absolutePath) / 1000)+"kb"
        if self.isDir():
            return "dir"
        return "-"
    
    def toggleSelection(self):
        self.selected = not self.selected
        if self.selected:
            self.backgroundColor = state.getColorPalette().getColor("accent")
            self.onSelect()
        else:
            self.backgroundColor = state.getColorPalette().getColor("background")
            self.onDeselect()
    

class FileExplorer(pyos.GUI.Container):    
    def __init__(self, position, **data):
        super(FileExplorer, self).__init__(position, **data)
        self.path = str(pyos.__file__).rstrip(".pyos.pyc").replace("\\", "/")
        self.selected = []
        self.fileList = pyos.GUI.ListScrollableContainer((0, 40), width=self.width, height=self.height-40, color=state.getColorPalette().getColor("background"),
                                                         margin=0, padding=0, scrollAmount=40)
        self.addChild(self.fileList)
        self.generateButtonBar()
        self.appSupport = ApplicationSupport()
        self.toCopy = None
        self.toMove = None
        self.loadDir()
        
    def generateButtonBar(self):
        self.buttonBar = pyos.GUI.ButtonRow((0, 0), width=self.width, height=40, color=state.getColorPalette().getColor("background"),
                                            border=1, borderColor=state.getColorPalette().getColor("item"),
                                            padding=0, margin=0)
        up = pyos.GUI.Image((0,0), surface=state.getIcons().getLoadedIcon("up"), width=40, height=40,
                            onClick=self.navUp)
        home = pyos.GUI.Image((0,0), surface=state.getIcons().getLoadedIcon("home_dir"), width=40, height=40,
                            onClick=self.navHome)
        goto = pyos.GUI.Image((0,0), surface=state.getIcons().getLoadedIcon("goto"), width=40, height=40,
                            onClick=self.navAsk, onLongClick=self.displayLocationDialog)
        self.copyBtn = pyos.GUI.Image((0,0), surface=state.getIcons().getLoadedIcon("copy"), width=40, height=40,
                            onClick=self.copy, onLongClick=self.clearCopy)
        self.moveBtn = pyos.GUI.Image((0,0), surface=state.getIcons().getLoadedIcon("move"), width=40, height=40,
                            onClick=self.move, onLongClick=self.clearMove)
        delete = pyos.GUI.Image((0,0), surface=state.getIcons().getLoadedIcon("delete"), width=40, height=40,
                            onClick=self.deleteAsk)
        self.buttonBar.addChild(up)
        self.buttonBar.addChild(home)
        self.buttonBar.addChild(goto)
        self.buttonBar.addChild(self.copyBtn)
        self.buttonBar.addChild(self.moveBtn)
        self.buttonBar.addChild(delete)
        self.addChild(self.buttonBar)
        
    def scanDir(self):
        entries = pyos.os.listdir(self.path)
        entries = [e for e in entries if not e.startswith(".")]
        files = sorted([e for e in entries if pyos.os.path.isfile(pyos.os.path.join(self.path, e))])
        folders = sorted([e for e in entries if pyos.os.path.isdir(pyos.os.path.join(self.path, e))])
        return folders + files
    
    def loadDir(self):
        self.fileList.clearChildren()
        for entry in self.scanDir():
            entryContainer = FileEntry((0, -80), pyos.os.path.join(self.path, entry), width=self.fileList.container.width, height=40,
                                             color=state.getColorPalette().getColor("background"), selected=(pyos.os.path.join(self.path, entry) in self.selected),
                                             onSelected=self.selected.append, onDeselected=self.selected.remove,
                                             onClick=self.navToSub
                                       )
            self.fileList.addChild(entryContainer)
        if self.fileList.container.childComponents == []:
            self.fileList.addChild(pyos.GUI.Text((2, 2), "This folder is empty.", state.getColorPalette().getColor("item")))
            
    def navUp(self):
        self.path = self.path[:self.path.rfind("/")]
        self.loadDir()
        
    def navHome(self):
        self.path = str(pyos.__file__).rstrip(".pyos.pyc").replace("\\", "/")
        self.loadDir()
        
    def navToSub(self, subDir):
        if subDir.isDir():
            self.path = subDir.absolutePath
            self.loadDir()
        if subDir.isFile():
            self.appSupport.choiceDialog(subDir.absolutePath, subDir.shortPath)
            
    def navToAbs(self, path):
        if not pyos.os.path.exists(path):
            pyos.GUI.ErrorDialog("The path you entered does not exist or cannot be accessed.").display()
            return
        self.path = path.replace("\\", "/")
        self.loadDir()
            
    def navAsk(self):
        pyos.GUI.AskDialog("Enter Path", "Enter the directory you wish to navigate to.", self.navToAbs).display()
        
    def displayLocationDialog(self):
        pyos.GUI.OKDialog("Location", "Current Location\n"+self.path.replace("/", "/ ")).display()
        
    def move(self):
        if self.selected == []:
            pyos.GUI.OKDialog("Copy", "Please select one or more items to copy.").display()
            return
        if self.toMove == None:
            self.toMove = self.selected[:]
            self.moveBtn.border = 2
            self.moveBtn.borderColor = state.getColorPalette().getColor("accent")
            return
        else:
            Operations.move(self.toMove, self.path)
            self.clearMove()
            
    def clearMove(self):
        self.toMove = None
        self.moveBtn.border = 0
        self.moveBtn.borderColor = (0, 0, 0, 0)
        self.moveBtn.refresh()
        self.selected = []
        self.loadDir()
            
    def copy(self):
        if self.selected == []:
            pyos.GUI.OKDialog("Copy", "Please select one or more items to copy.").display()
            return
        if self.toCopy == None:
            self.toCopy = self.selected[:]
            self.copyBtn.border = 2
            self.copyBtn.borderColor = state.getColorPalette().getColor("accent")
            return
        else:
            Operations.copy(self.toCopy, self.path)
            self.clearCopy()
            
    def clearCopy(self):
        self.toCopy = None
        self.copyBtn.border = 0
        self.copyBtn.borderColor = (0, 0, 0, 0)
        self.copyBtn.refresh()
        self.selected = []
        self.loadDir()
        
    def delete(self, resp):
        if resp == "Yes":
            Operations.delete(self.selected)
            self.selected = []
            self.loadDir()
        
    def deleteAsk(self):
        pyos.GUI.YNDialog("Delete", "Are you sure you wish to permanently delete "+str(len(self.selected))+" items?", self.delete).display()
        
def onStart(s, a):
    global state, application
    state = s
    application = a
    explorer = FileExplorer((0, 0), width=application.ui.width, height=application.ui.height)
    application.explorer = explorer
    application.ui.addChild(explorer)
    
def onResume():
    print "Resumed Files"
    application.explorer.loadDir()
