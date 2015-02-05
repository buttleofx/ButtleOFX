import threading


class Worker(threading.Thread):
    """
        Specific class for ActionManager. Can't be used somewhere else.
        It's not generic.
        Object used to execute actions with multi-threading.
    """
    isWaiting = False
    isDestroyed = False
    lockInProgress = threading.Lock()

    def __init__(self, queue, inProgress, done, notify):
        super(Worker, self).__init__()
        self._queue = queue
        self._done = done
        self._inProgress = inProgress
        self._notify = notify

    def executeTask(self):
        # lock when model check into queue while loading
        Worker.lockWhileWaiting()

        actionWrapper = self._queue.get()
        if not actionWrapper:
            return
        self._inProgress.append(actionWrapper)

        for action in actionWrapper.getActions():
            action.process()
            actionWrapper.upProcessed()
            self._notify.emit()

        # lock when model check into inProgressList while loading
        Worker.lockWhileWaiting()

        # search in progressList the index to push into doneList
        Worker.lockInProgress.acquire()
        indexTaskDone = self.getIndexFromList(self._inProgress, id(actionWrapper))
        if indexTaskDone > -1:
            self._done.append(self._inProgress.pop(indexTaskDone))
        Worker.lockInProgress.release()

    def getIndexFromList(self, list, idItem):
        for idx, el in enumerate(list):
            if idItem == id(el):
                return idx
        return -1

    def run(self):
        while 1 and not Worker.isDestroyed:
            self.executeTask()

    @staticmethod
    def lockWhileWaiting():
        while Worker.isWaiting:
            pass

    @staticmethod
    def work():
        Worker.isWaiting = False

    @staticmethod
    def wait():
        Worker.isWaiting = True

    @staticmethod
    def destroy():
        Worker.isDestroyed = True
