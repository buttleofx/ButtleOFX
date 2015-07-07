![ButtleOFX](https://raw.github.com/buttleofx/ButtleOFX/develop/blackMosquito.png "ButtleOFX")ButtleOFX
========================

Pre-requisites
--------------

- python 3
-- numpy
-- PyOpenGL
- Qt 5.4 (QtQuick 2)
- PyQt 5.4
- TuttleOFX


Install dependencies
--------------------

```
su

ROOT=$PWD

## Python
apt-get install python3
pip3 install numpy PyOpenGL

## Qt
cd $ROOT
wget http://download.qt-project.org/official_releases/online_installers/qt-opensource-linux-x64-online.run
chmod +x qt-opensource-linux-x64-online.run
./qt-opensource-linux-x64-online.run

rm -rf $ROOT/Qt/Tools $ROOT/Qt/Examples $ROOT/Qt/Docs $ROOT/Qt/5.4/gcc_64/include

## SIP
cd $ROOT
wget http://sourceforge.net/projects/pyqt/files/sip/sip-4.16.6/sip-4.16.6.tar.gz
tar xvzf sip-4.16.6.tar.gz
cd sip-4.16.6
python3 configure.py
make
make install

## PyQt
cd $ROOT
wget http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.4.1/PyQt-gpl-5.4.1.tar.gz
tar xvzf PyQt-gpl-5.4.1.tar.gz
cd PyQt-gpl-5.4.1
python3 configure.py --qmake /opt/Qt5.4/5.4/gcc_64/bin/qmake --sip-incdir ../sip-4.16.6/siplib
make
make install

rm $ROOT/*.tar.gz $ROOT/*.run
```

[TuttleOFX Installation](https://raw.github.com/tuttleofx/TuttleOFX/develop/INSTALL.md)


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


Create self-contained binaries
------------------------------

```
ROOT=$PWD
PYTHON_DIR=$ROOT/py3.4_env
PYTHON=$PYTHON_DIR/bin/python
PIP=$PYTHON_DIR/bin/pip

python3 "$(curl https://gist.github.com/vsajip/4673395/raw/3420d9150ce1e9797dc8522fce7386d8643b02a1/pyvenvex.py)" $PYTHON_DIR

$PIP install numpy
$PIP install PyOpenGL
# $PIP install PyOpenGL_accelerate # dont use by default, it creates some troubles on some platforms


## Qt
cd $ROOT
wget http://download.qt-project.org/official_releases/online_installers/qt-opensource-linux-x64-online.run
chmod +x qt-opensource-linux-x64-online.run
# In the UI choose to install in the current directory
./qt-opensource-linux-x64-online.run

## SIP
cd $ROOT
wget http://sourceforge.net/projects/pyqt/files/sip/sip-4.16.6/sip-4.16.6.tar.gz
tar xvzf sip-4.16.6.tar.gz
cd sip-4.16.6
$PYTHON configure.py
make
make install

## PyQt
cd $ROOT
wget http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.4.1/PyQt-gpl-5.4.1.tar.gz
tar xvzf PyQt-gpl-5.4.1.tar.gz
cd PyQt-gpl-5.4.1
$PYTHON configure.py --qmake $ROOT/Qt/5.4/gcc_64/bin/qmake --sip-incdir ../sip-4.16.6/siplib
make
make install

## Clean
rm -rf sip-4.16.6
rm -rf PyQt-gpl-5.4.1
rm $ROOT/*.tar.gz $ROOT/*.run

rm -rf $ROOT/Qt/Tools $ROOT/Qt/Examples $ROOT/Qt/Docs $ROOT/Qt/5.4/gcc_64/include
rm -rf $ROOT/Qt/MaintenanceTool* $ROOT/Qt/InstallationLog.txt
mv $ROOT/Qt/5.4/gcc_64/bin/qmlviewer $ROOT/Qt/5.4/gcc_64
rm -rf $ROOT/Qt/5.4/gcc_64/lib/*.a
rm -rf $ROOT/Qt/5.4/gcc_64/lib/*.la
rm -rf $ROOT/Qt/5.4/gcc_64/lib/cmake $ROOT/Qt/5.4/gcc_64/lib/pkgconfig
rm -rf $ROOT/Qt/5.4/gcc_64/bin
rm -rf $ROOT/Qt/5.4/gcc_64/mkspecs

rm -rf $ROOT/Qt/5.4/gcc_64/qml/Enginio $ROOT/Qt/5.4/gcc_64/qml/QtAudioEngine $ROOT/Qt/5.4/gcc_64/qml/QtBluetooth $ROOT/Qt/5.4/gcc_64/qml/QtLocation $ROOT/Qt/5.4/gcc_64/qml/QtNfc $ROOT/Qt/5.4/gcc_64/qml/QtPositioning $ROOT/Qt/5.4/gcc_64/qml/QtSensors $ROOT/Qt/5.4/gcc_64/qml/QtTest $ROOT/Qt/5.4/gcc_64/qml/QtWebChannel $ROOT/Qt/5.4/gcc_64/qml/QtWebKit

find . -name "__pycache__" -exec rm -rf {} \;
find . -name "*.prl" -delete

```


