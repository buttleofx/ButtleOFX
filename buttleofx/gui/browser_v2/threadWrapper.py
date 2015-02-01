import threading


class ThreadWrapper():

    def __init__(self):
        self._lock = threading.Lock()
        self._jobs = []

    def getLock(self):
        return self._lock

    def startThread(self, f, argsParam=()):
        if len(self._jobs) > 20:
            return
        self._jobs.append(threading.Thread(target=f, args=argsParam))
        self._jobs[-1:][0].start()

    def getNbJobs(self):
        return len(self._jobs)

    def pop(self):
        self._jobs.pop(0)

    def stopAllThreads(self):
        self._jobs.clear()

    def unlock(self):
        try:
            self.getLock().release()
        except:
            pass

    def lock(self):
        self.getLock().acquire()