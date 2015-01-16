import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtQuick

from pySequenceParser import sequenceParser


class BrowserModel(QtCore.QObject):

    def __init__(self, path):
        self.path = path

    def browse(self):
        return sequenceParser.browse(self.path)

    def files(self):
        return sequenceParser.fileInDirectory(self.path)

