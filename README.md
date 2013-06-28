![ButtleOFX](http://github.com/tuttleofx/TuttleOFX/raw/master/plugins/_scripts/ImageEffectApi/Resources/L_ProjectName_.png "ButtleOFX")ButtleOFX
========================
**Project under early development.**

ButtleOFX project is a set of GUI tools built around the TuttleOFX framework.

___
License
-------
Follows the TuttleOFX license.
>see [**TuttleOFX/COPYING.md**](http://github.com/tuttleofx/TuttleOFX/blob/master/COPYING.md)

___
Compilation
-----------

- Getting the source  
`git clone git://github.com/buttleofx/ButtleOFX.git`  
`cd ButtleOFX`  
`git submodule update -i --recursive`  


3rdParties
----------

`git clone git://gitorious.org/~freesmael/qt-labs/freesmaels-qmlcanvas.git qmlcanvas`  
`cd qmlcanvas`  
`qmake-qt4`  
`make`  

`git clone git://gitorious.org/qt/qtquickcontrols.git -b qt4`  
`cd qtquickcontrols`  
`qmake-qt4`  
`make install`  


Run
---

``export BUTTLEOFX=`pwd` ``  
``export TUTTLEOFX_BIN=$BUTTLEOFX/TuttleOFX/dist/`hostname`/gcc-`gcc -dumpversion`/production``  
`export PYTHONPATH=$TUTTLEOFX_BIN/python`  
`export OFX_PLUGIN_PATH=$TUTTLEOFX_BIN/plugin`  
     
`python buttleApp.py`  


Errors
------

If you encounter errors to see plugins, you may need to clear the plugins cache:
rm -rf ~/.tuttleofx


More information 
----------------

Official website: [https://sites.google.com/site/tuttleofx](https://sites.google.com/site/tuttleofx).

**ButtleOFX** on github: [https://github.com/tuttleofx/ButtleOFX](https://github.com/tuttleofx/ButtleOFX)

**TuttleOFX** on github: [https://github.com/tuttleofx/TuttleOFX](https://github.com/tuttleofx/TuttleOFX)

