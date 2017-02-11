import pyos
from pyos.gui.button import Button
from pyos.gui.container import Container
from pyos.gui.dialog import WarningDialog
from pyos.gui.image import Image
from pyos.gui.listpagedcontainer import ListPagedContainer
from pyos.gui.text import Text

state = None
app = None

def buildAppEntry(a):
    cont =Container((0,0), color=state.getColorPalette().getColor("background"), width=app.ui.width-2, height=40)
    ic = a.getIcon()
    icon = None
    if ic != False:
        icon =Image((0,0), surface=a.getIcon())
    else:
        icon =Image((0,0), surface=state.getIcons().getLoadedIcon("unknown"))
    title =Text((40, 10), a.title, state.getColorPalette().getColor("item"), 20)
    pauseBtn = Button((app.ui.width-100, 0), "Pause", state.getColorPalette().getColor("background"), state.getColorPalette().getColor("item"),
                               20, width=50, height=40, border=1, borderColor=state.getColorPalette().getColor("accent"),
                               onClick=registerPauseClick, onClickData=(a, cont))
    stopBtn = Button((app.ui.width-50, 0), "Stop", state.getColorPalette().getColor("background"), state.getColorPalette().getColor("item"),
                               20, width=50, height=40, border=1, borderColor=state.getColorPalette().getColor("accent"),
                               onClick=registerStopClick, onClickData=(a, cont))
    if a.thread.pause:
        pauseBtn.textComponent.text = "Resume"
        pauseBtn.refresh()
    if a.thread.stop or a.thread.firstRun:
        stopBtn.textComponent.text = "Start"
        pauseBtn.refresh()
        pauseBtn.textComponent.text = " - "
        pauseBtn.refresh()
    cont.addChild(icon)
    cont.addChild(title)
    cont.addChild(pauseBtn)
    cont.addChild(stopBtn)
    return cont

def registerPauseClick(a, cont):
    pauseBtn = cont.getChildAt([app.ui.width-100,0])
    if a.thread.stop or a.thread.firstRun: return
    if a.thread.pause:
        a.activate()
        pauseBtn.textComponent.text = "Pause"
        pauseBtn.refresh()
    else:
        a.deactivate(True)
        pauseBtn.textComponent.text = "Resume"
        pauseBtn.refresh()

def registerStopClick(a, cont):
    pauseBtn = cont.getChildAt([app.ui.width-100,0])
    stopBtn = cont.getChildAt([app.ui.width-50,0])
    if a.thread.stop or a.thread.firstRun:
        a.activate()
        stopBtn.textComponent.text = "Stop"
        stopBtn.refresh()
        pauseBtn.textComponent.text = "Pause"
        pauseBtn.refresh()
    else:
        a.deactivate(False)
        stopBtn.textComponent.text = "Start"
        stopBtn.refresh()
        pauseBtn.textComponent.text = " - "
        pauseBtn.refresh()
        
def loadList():
    app.ui.clearChildren()
    appList = ListPagedContainer((0, 0), width=app.ui.width, height=app.ui.height, color=state.getColorPalette().getColor("background"))
    app.ui.addChild(appList)
    for a in state.getApplicationList().getApplicationList():
        appList.addChild(buildAppEntry(a))
    appList.goToPage()

def onLoad(s, a):
    global state, app
    app = a
    state = s
    loadList()
    WarningDialog("This application modifies the state of other apps. Using it may result in data loss.").display()
    