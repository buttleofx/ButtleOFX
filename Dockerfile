FROM tuttleofx/tuttleofx-python3.5

MAINTAINER ButtleOFX <buttleofx-dev@googlegroups.com>

ENV BUTTLEOFX_DEV=/opt/ButtleOFX_git \
    HOME=/home/developer

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
    && pip3 install numpy PyOpenGL PyOpenGL_accelerate \
    && apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/developer && \
    mkdir -p /etc/sudoers.d && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer

COPY . $BUTTLEOFX_DEV
WORKDIR $BUTTLEOFX_DEV
USER developer
ENTRYPOINT python3 ${BUTTLEOFX_DEV}/buttleApp.py