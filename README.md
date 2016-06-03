# ButtleOFX
[![Stories in Ready](https://badge.waffle.io/buttleofx/ButtleOFX.png?label=ready &title=Ready)](http://waffle.io/buttleofx/ButtleOFX)

**Project under early development.**

ButtleOFX is an open source compositing software based on [TuttleOFX](https://github.com/tuttleofx/TuttleOFX) framework.

More informations on the official website: [http://buttleofx.wordpress.com](http://buttleofx.wordpress.com) 

[Documentation](http://buttleofx.readthedocs.org/)

## Install - Docker

### Release

`Docker 1.11.1` minimum is required. [See docker install procedure](https://docs.docker.com/engine/installation/linux/).

To run the application, you just need to execute these docker commands:

```bash
docker pull buttleofx/buttleofx

XSOCK=/tmp/.X11-unix
ARGUMENT_USER_GROUPS=$(for i in $(id -G); do echo -n "--group-add $i "; done)

docker run \
	--rm \
	-it \
	-v $XSOCK:$XSOCK:rw \
	-v $HOME:$HOME \
	-v /etc/passwd:/etc/passwd:ro \
	-v /etc/group:/etc/group:ro \
	-e DISPLAY=$DISPLAY \
	-u $(id -u):$(id -g) \
	-w $HOME \
	$ARGUMENT_USER_GROUPS \
	buttleofx/buttleofx

```
ButtleOFX image is executed with the host user and groups.

The `home` folder is mounted with read-write permissions.

`/etc/passwd and /etc/group` are also mounted to provide host users and groups informations to the container (read-only).


### Development

You need to mount the development files into the docker container when runing the image

- `BUTTLEOFX_DEV=/opt/ButtleOFX_git`(from Dockerfile)

- `-v "$(pwd)":$BUTTLEOFX_DEV:ro`


See [Docker hub](http://hub.docker.com/r/buttleofx/buttleofx)

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