FROM bossjones/ultron8-hacking:0.1.0

# container user
ARG CONTAINER_GID=501
ARG CONTAINER_UID=501
ARG CONTAINER_USER=developer

# host ip address
ARG HOST_IP

# set container user as environment variable
ENV CONTAINER_USER=${CONTAINER_USER}

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

ENV PATH="/home/${CONTAINER_USER}/.local/bin:${PATH}"
