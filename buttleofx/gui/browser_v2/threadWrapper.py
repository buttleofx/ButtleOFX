import threading


class ThreadWrapper():

    def __init__(self):
        self._lock = threading.Lock()
        self._jobs = []

    def getLock(self):
        return self._lock

    def startThread(self, f):
        if len(self._jobs) > 20:
            return
        self._jobs.append(threading.Thread(target=f))
        self._jobs[-1:][0].start()

    def getNbJobs(self):
        return len(self._jobs)

    def pop(self):
        self._jobs.pop(0)