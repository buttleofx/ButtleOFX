from PyQt5 import QtCore


class WorkerThread(QtCore.QThread):
    def __init__(self, target, param):
        super(WorkerThread, self).__init__()
        self._target = target
        self._param = param

    def run(self):
        self._target(*self._param)


class ThreadPool(QtCore.QObject):
    def __init__(self):
        super(ThreadPool, self).__init__(None)
        self._debugMode = False
        self._threadList = []
        self._mutex = QtCore.QMutex(QtCore.QMutex.Recursive)
        self._activeWorker = None  # more readable
        self._stopFlag = False

    def __del__(self):
        self.debug("STOP THREAD WRAPPER", self)
        self.stop()

    def debug(self, *output):
        if self._debugMode:
            print(*output)

    def getActiveWorker(self):
        return self._activeWorker

    def getMutex(self):
        return self._mutex

    def isWorking(self):
        """ if len(workers) > 1 : considered as not working, another worker is querying job """
        return len(self._threadList) == 1

    def stop(self):
        self._stopFlag = True
        for threadItem in self._threadList:
            threadItem.wait()
        self._threadList.clear()
        self._activeWorker = None

    def isStopped(self):
        return self._stopFlag

    def setStopFlag(self, flag):
        self._stopFlag = flag

    def start(self, target, argsParam=()):
        if self.getPoolSize() > 0:
            self.stop()

        worker = WorkerThread(target, argsParam)
        if not self._activeWorker:
            self._activeWorker = worker
        self._threadList.append(worker)
        worker.start()

    def pop(self):
        if self._threadList:
            self._threadList.pop(0)
            self._activeWorker = None if not self._threadList else self._threadList[0]

    def join(self):
        self.debug("join threadPool")
        self.debug("size pool", self.getPoolSize())

        if self._activeWorker:
            self.debug("worker present")
            self.debug("size pool", self.getPoolSize())
            
            self._activeWorker.wait()
        self.debug("end join")

    def lock(self):
        self.debug("Lock", self._mutex)
        self._mutex.lock()

    def unlock(self):
        self.debug("Unlock", self._mutex)
        self._mutex.unlock()

    def getPoolSize(self):
        return len(self._threadList)
