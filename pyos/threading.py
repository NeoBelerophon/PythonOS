from datetime import datetime
from thread import start_new_thread
from pyos.state import State


class Thread(object):
    def __init__(self, method, **data):
        self.eventBindings = {}
        self.pause = False
        self.stop = False
        self.firstRun = True
        self.method = method
        self.pause = data.get("startPaused", False)
        self.eventBindings["onStart"] = data.get("onStart", None)
        self.eventBindings["onStop"] = data.get("onStop", None)
        self.eventBindings["onPause"] = data.get("onPause", None)
        self.eventBindings["onResume"] = data.get("onResume", None)
        self.eventBindings["onCustom"] = data.get("onCustom", None)

    @staticmethod
    def __defaultEvtMethod(self, *args):
        return

    def execEvent(self, evtKey, *params):
        toExec = self.eventBindings.get(evtKey, Thread.__defaultEvtMethod)
        if toExec is None:
            return
        if type(toExec) == list:
            toExec[0](*toExec[1])
        else:
            toExec(*params)

    def setPause(self, state="toggle"):
        if type(state) != bool:
            self.pause = not self.pause
        else:
            self.pause = state
        if self.pause:
            self.execEvent("onPause")
        else:
            self.execEvent("onResume")

    def setStop(self):
        self.stop = True
        self.execEvent("onStop")

    def run(self):
        try:
            if self.firstRun:
                if self.eventBindings["onStart"] is not None:
                    self.execEvent("onStart")
                self.firstRun = False
            if not self.pause and not self.stop:
                self.method()
        except:
            State.instance().error_recovery("Thread error.", "Thread bindings: " + str(self.eventBindings))
            self.stop = True
            self.firstRun = False


class Task(Thread):
    def __init__(self, method, *additionalData):
        super(Task, self).__init__(method)
        self.returnedData = None
        self.additionalData = additionalData

    def run(self):
        self.returnedData = self.method(*self.additionalData)
        self.setStop()

    def getReturn(self):
        return self.returnedData

    def setPause(self):
        return

    def execEvent(self, evtKey, *params):
        return


class StagedTask(Task):
    def __init__(self, method, maxStage=10):
        super(StagedTask, self).__init__(method)
        self.stage = 1
        self.maxStage = maxStage

    def run(self):
        self.returnedData = self.method(self.stage)
        self.stage += 1
        if self.stage >= self.maxStage:
            self.setStop()


class TimedTask(Task):
    def __init__(self, executeOn, method, *additionalData):
        self.executionTime = executeOn
        super(TimedTask, self).__init__(method, *additionalData)

    def run(self):
        delta = self.executionTime - datetime.now()
        if delta.total_seconds() <= 0:
            super(TimedTask, self).run()


class ParallelTask(Task):
    # Warning: This starts a new thread.
    def __init__(self, method, *additionalData):
        super(ParallelTask, self).__init__(method, *additionalData)
        self.ran = False

    def run(self):
        if not self.ran:
            start_new_thread(self.runHelper, ())
            self.ran = True

    def getReturn(self):
        return None

    def runHelper(self):
        self.method(*self.additionalData)
        self.setStop()

    def setStop(self):
        super(ParallelTask, self).setStop()


class Controller(object):
    def __init__(self):
        self.threads = []
        self.dataRequests = {}

    def requestData(self, fromThread, default=None):
        self.dataRequests[fromThread] = default

    def getRequestedData(self, fromThread):
        return self.dataRequests[fromThread]

    def addThread(self, thread):
        self.threads.append(thread)

    def removeThread(self, thread):
        try:
            if type(thread) == int:
                self.threads.pop(thread)
            else:
                self.threads.remove(thread)
        except:
            print "Thread was not removed!"

    def stopAllThreads(self):
        for thread in self.threads:
            thread.setStop()

    def run(self):
        for thread in self.threads:
            thread.run()
            if thread in self.dataRequests:
                try:
                    self.dataRequests[thread] = thread.getReturn()
                except:
                    self.dataRequests[thread] = False  # getReturn called on Thread, not Task
            if thread.stop:
                self.threads.remove(thread)
