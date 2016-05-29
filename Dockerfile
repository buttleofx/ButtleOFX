FROM tuttleofx/tuttleofx:python3-latest

MAINTAINER ButtleOFX <buttleofx-dev@googlegroups.com>

ENV BUTTLEOFX_DEV=/opt/ButtleOFX_git

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    qt5-default \
    qtdeclarative5-dev \
    python3-pyqt5 \
    python3-pyqt5.qtquick \
    qml-module-qtquick-controls \
    qml-module-qtquick-layouts \
    qml-module-qtquick-dialogs \
    qml-module-qtquick-localstorage \
    libgl1-mesa-dev \
    mesa-utils \
    && pip3 install numpy PyOpenGL PyOpenGL_accelerate planar \
    && apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cache

COPY . $BUTTLEOFX_DEV
WORKDIR $BUTTLEOFX_DEV
ENTRYPOINT python3 ${BUTTLEOFX_DEV}/buttleApp.py