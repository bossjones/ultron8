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

USER ${CONTAINER_USER}
WORKDIR /home/${CONTAINER_USER}
ENV LANG C.UTF-8

COPY --chown=developer:developer requirements.txt requirements.txt
COPY --chown=developer:developer requirements-dev.txt requirements-dev.txt
COPY --chown=developer:developer requirements-doc.txt requirements-doc.txt
COPY --chown=developer:developer requirements-test.txt requirements-test.txt
COPY --chown=developer:developer Pipfile Pipfile
COPY --chown=developer:developer Pipfile.lock Pipfile.lock

RUN pip3 install tox-pyenv && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir -r requirements-dev.txt && \
    pip3 install --no-cache-dir -r requirements-test.txt && \
    pip3 install --no-cache-dir -r requirements-doc.txt && \
    pip3 install --no-cache-dir tox && \
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

RUN USER=${CONTAINER_USER} && \
    GROUP=${CONTAINER_USER} && \
    curl -SsL https://github.com/boxboat/fixuid/releases/download/v0.4/fixuid-0.4-linux-amd64.tar.gz | tar -C /usr/local/bin -xzf - && \
    chown root:root /usr/local/bin/fixuid && \
    chmod 4755 /usr/local/bin/fixuid && \
    mkdir -p /etc/fixuid && \
    printf "user: $USER\ngroup: $GROUP\npaths:\n  - /home/developer\n  - /.pyenv\n" > /etc/fixuid/config.yml

USER root
