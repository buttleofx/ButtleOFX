import sys
import os

currentFilePath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentFilePath)
sys.path.append(os.path.join(currentFilePath,'QuickMamba'))

#----------------------------------------

import quickmamba
import buttleofx

if __name__ == '__main__':
    quickmamba.qmlRegister()

    app = buttleofx.ButtleApp(sys.argv)
    buttleofx.main(sys.argv, app)
    app.exec_()
