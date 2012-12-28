import sys
import os

currentFilePath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentFilePath)
sys.path.append(os.path.join(currentFilePath,'QuickMamba'))

#----------------------------------------

import buttleofx.gui.viewerGL
import quickmamba

if __name__ == '__main__':
    quickmamba.qmlRegister()
    buttleofx.gui.viewerGL.main(sys.argv)

