FROM bossjones/ultron8-hacking:0.1.0

# container user
ARG CONTAINER_GID=501
ARG CONTAINER_UID=501
ARG CONTAINER_USER=developer
ARG PYENV_VERSION=3.6.8

# host ip address
ARG HOST_IP

# set container user as environment variable
ENV CONTAINER_USER=${CONTAINER_USER}
ENV PYENV_VERSION=${PYENV_VERSION}
ENV CONTAINER_GID=${CONTAINER_GID}
ENV CONTAINER_UID=${CONTAINER_UID}

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# SOURCE: https://phauer.com/2018/install-cairo-cairosvg-alpine-docker/
RUN apk add --no-cache \
    build-base cairo-dev cairo cairo-tools gobject-introspection-dev \
    # pillow dependencies
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev libxml2-dev g++ gcc libxslt-dev

USER ${CONTAINER_USER}
WORKDIR /home/${CONTAINER_USER}
ENV LANG C.UTF-8

COPY --chown=developer:developer requirements.txt requirements.txt
COPY --chown=developer:developer requirements-dev.txt requirements-dev.txt
COPY --chown=developer:developer requirements-doc.txt requirements-doc.txt
COPY --chown=developer:developer requirements-test.txt requirements-test.txt
COPY --chown=developer:developer Pipfile Pipfile
COPY --chown=developer:developer Pipfile.lock Pipfile.lock

RUN pip3 install -q --no-cache-dir -U pip setuptools tox && \
    pip3 install -q --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir -r requirements-dev.txt && \
    pip3 install -q --no-cache-dir -r requirements-test.txt && \
    pip3 install -q --no-cache-dir -r requirements-doc.txt && \
    pyenv rehash

# Copy over everything required to run tox
COPY --chown=developer:developer setup.cfg setup.py tox.ini ./
COPY --chown=developer:developer ultron8/__init__.py ultron8/__init__.py

RUN set -x; tree; tox -e py36 --notest; echo "NOTE: This most likely produced a stack trace, and that is ok! The full install will happen when you call docker run."

# ENV PATH="/home/${CONTAINER_USER}/.local/bin:${PATH}"

# COPY --chown=developer:developer . /home/${CONTAINER_USER}/app

ENV GOSU_VERSION=1.11

RUN cd /tmp && \
  sudo curl -sSL https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-amd64 -o /usr/local/bin/gosu && \
  sudo chmod +x /usr/local/bin/gosu && \
  sudo chown developer:developer /usr/local/bin/gosu

USER root

RUN USER=${CONTAINER_USER} && \
    GROUP=${CONTAINER_USER} && \
    curl -SsL https://github.com/boxboat/fixuid/releases/download/v0.4/fixuid-0.4-linux-amd64.tar.gz | tar -C /usr/local/bin -xzf - && \
    chown root:root /usr/local/bin/fixuid && \
    chmod 4755 /usr/local/bin/fixuid && \
    mkdir -p /etc/fixuid && \
    printf "user: $USER\ngroup: $GROUP\npaths:\n  - /home/developer\n  - /.pyenv\n" > /etc/fixuid/config.yml && \
    echo "  - /home/developer/.config" >> /etc/fixuid/config.yml && \
    echo "  - /home/developer/.cache" >> /etc/fixuid/config.yml && \
    echo "  - /start-gunicorn.sh" >> /etc/fixuid/config.yml && \
    echo "  - /gunicorn_conf.py" >> /etc/fixuid/config.yml && \
    echo "  - /start-reload-gunicorn.sh" >> /etc/fixuid/config.yml

USER ${CONTAINER_USER}:${CONTAINER_USER}

# Set working directory.
WORKDIR /home/${CONTAINER_USER}/app

COPY --chown=developer:developer ./start-gunicorn.sh /start-gunicorn.sh

RUN sudo chmod +x /start-gunicorn.sh

COPY --chown=developer:developer ./gunicorn_conf.py /gunicorn_conf.py

COPY --chown=developer:developer ./start-reload-gunicorn.sh /start-reload-gunicorn.sh

RUN sudo chmod +x /start-reload-gunicorn.sh


# SOURCE: https://www.reddit.com/r/godot/comments/9r72kv/godot_302_docker_image_for_automatic_exports/
# # Install fixuid.
# RUN curl -SsL https://github.com/boxboat/fixuid/releases/download/v0.4/fixuid-0.4-linux-amd64.tar.gz | tar -C /usr/local/bin -xzf - && \
#     chown root:root /usr/local/bin/fixuid && \
#     chmod 4755 /usr/local/bin/fixuid && \
#     mkdir -p /etc/fixuid && \
#     echo "user: docker" >> /etc/fixuid/config.yml && \
#     echo "group: docker" >> /etc/fixuid/config.yml && \
#     echo "paths:" >> /etc/fixuid/config.yml && \
#     echo "  - /home/docker/.config" >> /etc/fixuid/config.yml && \
#     echo "  - /home/docker/.cache" >> /etc/fixuid/config.yml

# Author and Docker Image information.
# LABEL maintainer="hrvoje.varga@gmail.com"
# LABEL build="docker build --network host -t hvarga/godot-docker ."
# LABEL run="docker run --rm --name godot-docker -v `pwd`:/home/docker/project -u $(id -u $USER):$(id -g $USER) hvarga/godot-docker make"


# && echo '#!/bin/bash\n\neval $( fixuid -q )\neval $*' > docker_startup_script.sh \
# && chmod a+x docker_startup_script.sh

# test -f $HOME/.ssh/id_rsa || ( install -m 0700 -d $HOME/.ssh && ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_rsa -q -N "" )


# RUN mkdir ~/.cache && \
# mkdir -p ~/.config/godot && \
# mkdir -p ~/.local/share/godot/templates/3.0.6.stable
