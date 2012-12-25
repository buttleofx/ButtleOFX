import sys
import os

currentFilePath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentFilePath)
sys.path.append(os.path.join(currentFilePath,'QuickMamba'))

#----------------------------------------

import buttleofx

if __name__ == '__main__':
    buttleofx.main(sys.argv)

