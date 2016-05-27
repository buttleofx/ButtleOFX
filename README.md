# ButtleOFX
[![Stories in Ready](https://badge.waffle.io/buttleofx/ButtleOFX.png?label=ready &title=Ready)](http://waffle.io/buttleofx/ButtleOFX)

**Project under early development.**

ButtleOFX is an open source compositing software based on [TuttleOFX](https://github.com/tuttleofx/TuttleOFX) framework.

More informations on the official website: [http://buttleofx.wordpress.com](http://buttleofx.wordpress.com) 

[Documentation](http://buttleofx.readthedocs.org/)

## Install - Docker

The docker image was built with `uid=1000 and gid=1000` to easily handle the GUI transaction between host and docker.

If your uid and gid are different you should modify the `Dockerfile`.

Then build the image with `docker build -t buttleofx/buttleofx`.

### Release

To run the application, you just need to run these docker commands

```
docker pull buttleofx/buttleofx

XSOCK=/tmp/.X11-unix
docker run \ 
	-it \
	--rm \
	-v $XSOCK:$XSOCK:rw \
	-e DISPLAY=$DISPLAY \
	buttleofx/buttleofx
```

### Development

You need to mount the development files into the docker container when runing the image
- `BUTTLEOFX_DEV=/opt/ButtleOFX_git`(from Dockerfile)

- `-v "$(pwd)":$BUTTLEOFX_DEV:ro`


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