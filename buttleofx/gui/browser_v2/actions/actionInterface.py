from buttleofx.gui.browser_v2.browserItem import BrowserItem


class ActionInterface():
    """
        Interface which determines the template comportment for an action on a BrowserItem
        action method must be implemented.
    """
    def __init__(self, browserItem):
        self._browserItem = browserItem

    def __del__(self):
        # print("Action destroyed")
        pass

    def begin(self):
        self._browserItem.notifyAddAction()

    def end(self):
        self._browserItem.notifyRemoveAction()

    def abort(self):
        self._browserItem.notifyRemoveAction()

    def action(self):
        raise NotImplementedError("ActionInterface::action() must be implemented")

    def revert(self):
        raise NotImplementedError("ActionInterface::revert() must be implemented")

    def process(self):
        self.begin()
        self.action()
        self.end()

    def getBrowserItem(self):
        return self._browserItem
