import sys
sys.path.append("../..")

import logging

from quickmamba.patterns import Signal

# Sample usage:
class Model(object):
    def __init__(self, value):
        self.__value = value
        self.changed = Signal()

    def set_value(self, value):
        self.__value = value
        self.changed() # Emit signal

    def get_value(self):
        return self.__value


class View(object):
    def __init__(self, model):
        self.model = model
        model.changed.connect(self.model_changed)

    def model_changed(self):
        logging.debug("New value:", self.model.get_value())


model = Model(10)
view1 = View(model)
view2 = View(model)
view3 = View(model)

model.set_value(20)

del view1
model.set_value(30)

model.changed.clear()
model.set_value(40)

