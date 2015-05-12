from PyQt5 import QtCore
import logging


class WorkerThread(QtCore.QThread):
    def __init__(self, target, param):
        super(WorkerThread, self).__init__()
        self._target = target
        self._param = param

    def run(self):
        self._target(*self._param)


class ThreadParallel(QtCore.QObject):

    def __init__(self):
        logging.debug("ThreadWrapper construction")
        super(ThreadParallel, self).__init__(None)
        self._mutex = QtCore.QMutex(QtCore.QMutex.Recursive)
        self._workerThread = None
        self._isStopped = True

    def __del__(self):
        self.stop()

    def getMutex(self):
        return self._mutex

    def isStopped(self):
        return self._isStopped

    def stop(self):
        self._isStopped = True
        if self._workerThread:
            self._workerThread.wait()
            self._workerThread = None

    def start(self, target, argsParam=()):
        if self._workerThread:
            self.stop()

        self._isStopped = False
        self._workerThread = WorkerThread(target, argsParam)
        self._workerThread.start()

    def join(self):
        if self._workerThread:
            self._workerThread.wait()
