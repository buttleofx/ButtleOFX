from PyQt5 import QtCore
import logging


class WorkerThread(QtCore.QThread):
    def __init__(self, target, param):
        super(WorkerThread, self).__init__()
        self._target = target
        self._param = param

    def run(self):
        self._target(*self._param)


class ThreadWrapper(QtCore.QObject):
    def __init__(self):
        logging.debug("ThreadWrapper begin constructor")
        super(ThreadWrapper, self).__init__(None)
        self._threadList = []
        self._mutex = QtCore.QMutex(QtCore.QMutex.Recursive)
        self._activeWorker = None  # more readable
        self._stopFlag = False
        logging.debug("ThreadWrapper end constructor")

    def __del__(self):
        logging.debug("STOP THREAD WRAPPER", self)
        self.stop()

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
        logging.debug("join threadPool")
        logging.debug("size pool %s" % self.getPoolSize())

        if self._activeWorker:
            logging.debug("worker present")
            logging.debug("size pool %s" % self.getPoolSize())
            
            self._activeWorker.wait()
        logging.debug("end join")

    def getPoolSize(self):
        return len(self._threadList)
