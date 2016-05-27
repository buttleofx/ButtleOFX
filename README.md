# ButtleOFX
[![Stories in Ready](https://badge.waffle.io/buttleofx/ButtleOFX.png?label=ready &title=Ready)](http://waffle.io/buttleofx/ButtleOFX)

**Project under early development.**

ButtleOFX is an open source compositing software based on [TuttleOFX](https://github.com/tuttleofx/TuttleOFX) framework.

More informations on the official website: [http://buttleofx.wordpress.com](http://buttleofx.wordpress.com) 

[Documentation](http://buttleofx.readthedocs.org/)

## Install - Docker

### Release

To run the application, you just need to run these docker commands.

```
docker pull buttleofx/buttleofx-env

xhost +

XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
BUTTLEOFX_DEV=/opt/ButtleOFX_git
touch $XAUTH

docker run \
	-it \
	--rm \
	--device=/dev/dri/card0:/dev/dri/card0 \
	-v $XSOCK:$XSOCK:rw \
	-v $XAUTH:$XAUTH:rw \
	-e DISPLAY=$DISPLAY \
	-e XAUTHORITY=$XAUTH \
	buttleofx/buttleofx-release

xhost -

```

### Development

This will mount your development files inside the docker container

```
docker pull buttleofx/buttleofx-env

xhost +

XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
BUTTLEOFX_DEV=/opt/ButtleOFX_git
touch $XAUTH

docker run \
	-it \
	--rm \
	--device=/dev/dri/card0:/dev/dri/card0 \
	-v $XSOCK:$XSOCK:rw \
	-v $XAUTH:$XAUTH:rw \
	-v "$(pwd)":$BUTTLEOFX_DEV:ro \
	-e BUTTLEOFX_DEV=$BUTTLEOFX_DEV \
	-e DISPLAY=$DISPLAY \
	-e XAUTHORITY=$XAUTH \
	-w $BUTTLEOFX_DEV \
	buttleofx/buttleofx-env python3 $BUTTLEOFX_DEV/buttleApp.py

xhost -

```

See [Docker hub](http://hub.docker.com/buttleofx/buttleofx)

## License

Follows the TuttleOFX license [**TuttleOFX/COPYING.md**](https://raw.github.com/tuttleofx/TuttleOFX/develop/COPYING.md)


## More information 

[Development teams](AUTHORS.md)

**TuttleOFX**
>- website: [http://tuttleofx.org](http://tuttleofx.org)
>- github: [https://github.com/tuttleofx/TuttleOFX](https://github.com/tuttleofx/TuttleOFX)

**OpenFX**
>- website: [http://openeffects.org](http://openeffects.org)
>- github: [http://github.com/ofxa/openfx](http://github.com/ofxa/openfx)

**QuickMamba**
>- github: [http://github.com/buttleofx/QuickMamba](http://github.com/buttleofx/QuickMamba)