from PyQt5 import QtCore
import logging


class WithBool:
    """
        Helper class
    """
    def __init__(self, value=False, notifyChange=None):
        self.value = value
        self.notifyChange = notifyChange

    def __bool__(self):
        return self.value

    def __enter__(self):
        self.value = True
        if self.notifyChange:
            self.notifyChange.emit()
        return self

    def __exit__(self, type, value, traceback):
        self.value = False
        if self.notifyChange:
            self.notifyChange.emit()


class WithMutex:
    """
        Helper class
    """
    def __init__(self, mutex):
        self.mutex = mutex

    def __enter__(self):
        self.mutex.lock()
        return self

    def __exit__(self, type, value, traceback):
        self.mutex.unlock()


class WorkerThread(QtCore.QThread):
    def __init__(self, target, param):
        super(WorkerThread, self).__init__()
        self._target = target
        self._param = param

    def run(self):
        self._target(*self._param)


class ParallelThread(QtCore.QObject):
    """
        Simulates a singleton about usage of threads in a needed parallel context.
        Know if current thread was stopped.
    """

    def __init__(self):
        super(ParallelThread, self).__init__(None)
        logging.debug("ParallelThread construction")
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
            if self._workerThread.isRunning():
                self._workerThread.wait()
            self._workerThread = None

    def start(self, target, argsParam=()):
        if self._workerThread:
            self.stop()

        self._isStopped = False
        self._workerThread = WorkerThread(target, argsParam)
        self._workerThread.start()

    def getWorkerThread(self):
        return self._workerThread

    def join(self):
        if self._workerThread and self._workerThread.isRunning():
            self._workerThread.wait()