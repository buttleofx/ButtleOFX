<<<<<<< HEAD
![ButtleOFX](https://raw.github.com/buttleofx/ButtleOFX/develop/blackMosquito.png "ButtleOFX")ButtleOFX
========================
**Project under early development.**

[ButtleOFX](http://buttleofx.wordpress.com) is an open source compositing software.

It is built on top of the [TuttleOFX](http://tuttleofx.org) framework which relies on the [OpenFX plugin standard](http://openeffects.org).

Website: [http://buttleofx.wordpress.com](http://buttleofx.wordpress.com)


Development teams
-----------------

ButtleOFX is developped within student projects at [IMAC Engineering school](http://imac.alwaysdata.net).

###Team 3.0

Version 3.0 (2014-2015) is currently in progress.   

Tutor :   
>- [Fabien CASTAN](https://github.com/fabiencastan)   
>- [Clément CHAMPETIER](https://github.com/cchampet)

Students :   
>- [Jordi BASTIDE](https://github.com/Jordinaire)
>- [Maxime ENGEL](https://github.com/MaximeEngel)
>- [Maxime GILBERT](https://github.com/mxmgilbert)
>- [Mathias GOYHENECHE](https://github.com/MGoyheneche)
>- [Alexis OBLET](https://github.com/aoblet)

###Team 2.0 (2013-2014)

Release an alpha version of the software with a new Browser module and a new Quick Parameter Editor.

Tutor :   
>- [Fabien CASTAN](https://github.com/fabiencastan)   

Students :   
>- [Lucie DELAIRE](https://github.com/Lucie2lr)
>- [Jonathan DOUET](https://github.com/jon92)
>- [Anthony GUIOT](https://github.com/aguiot)
>- [Virginie LALANDE](https://github.com/vilal)
>- [Baptiste MOIZARD](https://github.com/Bazard)

###Team 1.0 (2012-2013)

Creation of a basic compositing software with a Graph Editor, a Parameter Editor and a Viewer.

Tutor :   
>- [Fabien CASTAN](https://github.com/fabiencastan)   

Students :   
>- [Clément CHAMPETIER](https://github.com/cchampet)
>- [Xochitl FLORIMONT](https://github.com/Xochitl)
>- [Aurélien GRAFFARD](https://github.com/agreffard)
>- [Elisa PRANA](https://github.com/eprana)
>- [Arthur TOURNERET](https://github.com/artourn)


Pre-requisites
--------------

- python 3
- PyQt 5.2 (QtQuick 2)
- TuttleOFX


Getting the source
------------------

```
git clone git://github.com/buttleofx/ButtleOFX.git
cd ButtleOFX
git submodule update -i --recursive
```

Run
---

```
export TUTTLEOFX_ROOT=/path/to/TuttleOFX/install
export PYTHONPATH=$TUTTLEOFX_ROOT/python
export OFX_PLUGIN_PATH=$TUTTLEOFX_ROOT/plugin
python3 buttleApp.py
```

Errors
------

If you encounter errors to see plugins, you may need to clear the plugins cache:  
`rm -rf ~/.tuttleofx`


License
-------

Follows the TuttleOFX license.
>see [**TuttleOFX/COPYING.md**](http://github.com/tuttleofx/TuttleOFX/blob/master/COPYING.md)


More information 
----------------

**ButtleOFX**
>- website: [http://buttleofx.wordpress.com](http://buttleofx.wordpress.com)
>- github: [https://github.com/buttleofx/ButtleOFX](https://github.com/buttleofx/ButtleOFX)

**TuttleOFX**
>- website: [http://tuttleofx.org](http://tuttleofx.org)
>- github: [https://github.com/tuttleofx/TuttleOFX](https://github.com/tuttleofx/TuttleOFX)

**OpenFX**
>- website: [http://openeffects.org](http://openeffects.org)
>- github: [http://github.com/ofxa/openfx](http://github.com/ofxa/openfx)
=======
QuickMamba
==========

QtQuick tools


Links
-----
[google style guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html)


