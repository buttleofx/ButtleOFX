import sys
import os
from buttleofx.gui.viewerGL.main import main

currentFilePath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentFilePath)
sys.path.append(os.path.join(currentFilePath, 'QuickMamba'))

# ----------------------------------------

import buttleofx.gui.viewerGL
import quickmamba

if __name__ == '__main__':
    quickmamba.qmlRegister()
    buttleofx.gui.viewerGL.main.main(sys.argv)

