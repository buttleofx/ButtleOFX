![ButtleOFX](https://raw.github.com/buttleofx/ButtleOFX/develop/blackMosquito.png "ButtleOFX")ButtleOFX
========================
**Project under early development.**

ButtleOFX project is a set of GUI tools built around the [TuttleOFX](www.tuttleofx.org) framework.


Development teams
-------

ButtleOFX is developped within student projects at [IMAC Engineering school](http://imac.alwaysdata.net).

###Team 2.0

Version 2.0 (2013-2014) is currently on progress.   

Tutor :   
>- [Fabien CASTAN](https://github.com/fabiencastan)   

###Team 1.0

Version 1.0 (2012-2013) is the first iteration of the project.   
It's a proof of concept version, closer to an Alpha than a RC.

Tutor :   
>- [Fabien CASTAN](https://github.com/fabiencastan)   

Students :   
>- [Clément Champetier](https://github.com/cchampet)
>- [Xochitl Florimont](https://github.com/Xochitl)
>- [Aurélien Graffard](https://github.com/agreffard)
>- [Elisa Prana](https://github.com/eprana)
>- [Arthur Tourneret](https://github.com/artourn)

See [project's blog.](http://buttleofx.wordpress.com/)


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


License
-------
Follows the TuttleOFX license.
>see [**TuttleOFX/COPYING.md**](http://github.com/tuttleofx/TuttleOFX/blob/master/COPYING.md)


More information 
----------------

Official website: [https://sites.google.com/site/tuttleofx](https://sites.google.com/site/tuttleofx).

**ButtleOFX** on github: [https://github.com/tuttleofx/ButtleOFX](https://github.com/tuttleofx/ButtleOFX)

**TuttleOFX** on github: [https://github.com/tuttleofx/TuttleOFX](https://github.com/tuttleofx/TuttleOFX)
