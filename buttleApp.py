#! /usr/bin/env python3
import sys
import os

currentFilePath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentFilePath)
sys.path.append(os.path.join(currentFilePath,'QuickMamba'))

#----------------------------------------

import quickmamba
import buttleofx.main

if __name__ == '__main__':
    quickmamba.qmlRegister()

    app = buttleofx.main.ButtleApp(sys.argv)
    buttleofx.main.main(sys.argv, app)
    app.exec_()
