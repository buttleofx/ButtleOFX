![ButtleOFX](https://raw.github.com/buttleofx/ButtleOFX/develop/blackMosquito.png "ButtleOFX")ButtleOFX
========================
**Project under early development.**

ButtleOFX project is a set of GUI tools built around the [TuttleOFX](www.tuttleofx.org) framework.


Development teams
-------

ButtleOFX is developped within student projects at [IMAC Engineering school](http://imac.alwaysdata.net).

See [project's blog.](http://buttleofx.wordpress.com/)


###Team 2.0

Version 2.0 (2013-2014) is currently on progress.   

Tutor :   
>- [Fabien CASTAN](https://github.com/fabiencastan)   

Students :   
>- [Lucie DELAIRE](https://github.com/Lucie2lr)
>- [Jonathan DOUET](https://github.com/jon92)
>- [Anthony GUIOT](https://github.com/aguiot)
>- [Virginie LALANDE](https://github.com/vilal)
>- [Baptiste MOIZARD](https://github.com/Bazard)

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


Pre-requisites
-----------

- python 3
- PyQt 5.2 (QtQuick 2)


Compilation
-----------

- Getting the source  
`git clone git://github.com/buttleofx/ButtleOFX.git`  
`cd ButtleOFX`  
`git submodule update -i --recursive`  


Run
---

``export TUTTLEOFX_BIN=/path/to/TuttleOFX/dist/`hostname`/gcc-`gcc -dumpversion`/production``  
`export PYTHONPATH=$TUTTLEOFX_BIN/python`  
`export OFX_PLUGIN_PATH=$TUTTLEOFX_BIN/plugin`  
     
`python3 buttleApp.py`  


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
