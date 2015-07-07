import sys
import os
from buttleofx.gui.viewerGL.main import main as VglMain

currentFilePath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentFilePath)
sys.path.append(os.path.join(currentFilePath, 'QuickMamba'))

# ----------------------------------------

import quickmamba

if __name__ == '__main__':
    quickmamba.qmlRegister()
    VglMain(sys.argv)

