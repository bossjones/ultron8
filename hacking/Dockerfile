FROM docker:18.09.6-dind

# container user
ARG CONTAINER_GID=501
ARG CONTAINER_UID=501
ARG CONTAINER_USER=developer

# host ip address
ARG HOST_IP

# set container user as environment variable
ENV CONTAINER_USER=${CONTAINER_USER}

# ENV DEBIAN_FRONTEND noninteractive
# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# install ca-certificates so that HTTPS works consistently
# other runtime dependencies for Python are installed later
RUN apk add --no-cache ca-certificates

ENV GPG_KEY 0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D
ENV PYTHON_VERSION 3.6.8

RUN set -ex \
	&& apk add --no-cache --virtual .fetch-deps \
		gnupg \
		tar \
		xz \
	\
	&& wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
	&& wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" \
	&& export GNUPGHOME="$(mktemp -d)" \
	&& rm -rf "$GNUPGHOME" python.tar.xz.asc \
	&& mkdir -p /usr/src/python \
	&& tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
	&& rm python.tar.xz \
	\
	&& apk add --no-cache --virtual .build-deps  \
		bzip2-dev \
		coreutils \
		dpkg-dev dpkg \
		expat-dev \
		findutils \
		gcc \
		gdbm-dev \
		libc-dev \
		libffi-dev \
		libnsl-dev \
		libtirpc-dev \
		linux-headers \
		make \
		ncurses-dev \
		openssl-dev \
		pax-utils \
		readline-dev \
		sqlite-dev \
		tcl-dev \
		tk \
		tk-dev \
		xz-dev \
		zlib-dev \
# add build deps before removing fetch deps in case there's overlap
	&& apk del .fetch-deps \
	\
	&& cd /usr/src/python \
	&& gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
	&& ./configure \
		--build="$gnuArch" \
		--enable-loadable-sqlite-extensions \
		--enable-shared \
		--with-system-expat \
		--with-system-ffi \
		--without-ensurepip \
	&& make -j "$(nproc)" \
# set thread stack size to 1MB so we don't segfault before we hit sys.getrecursionlimit()
# https://github.com/alpinelinux/aports/commit/2026e1259422d4e0cf92391ca2d3844356c649d0
		EXTRA_CFLAGS="-DTHREAD_STACK_SIZE=0x100000" \
	&& make install \
	\
	&& find /usr/local -type f -executable -not \( -name '*tkinter*' \) -exec scanelf --needed --nobanner --format '%n#p' '{}' ';' \
		| tr ',' '\n' \
		| sort -u \
		| awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
		| xargs -rt apk add --no-cache --virtual .python-rundeps \
	&& apk del .build-deps \
	\
	&& find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' + \
	&& rm -rf /usr/src/python \
	\
	&& python3 --version

# make some useful symlinks that are expected to exist
RUN cd /usr/local/bin \
	&& ln -s idle3 idle \
	&& ln -s pydoc3 pydoc \
	&& ln -s python3 python \
	&& ln -s python3-config python-config

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 19.1.1

RUN set -ex; \
	\
	wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py'; \
	\
	python get-pip.py \
		--disable-pip-version-check \
		--no-cache-dir \
		"pip==$PYTHON_PIP_VERSION" \
	; \
	pip --version; \
	\
	find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' +; \
	rm -f get-pip.py

# SOURCE: https://github.com/bossjones/ubuntu-devtop-vm/blob/482474d8c4cb44f2389a5b314ee050fbecdbdc2b/bionic/Dockerfile

# ENV LC_CTYPE en_US.UTF-8

RUN set -eux; \
    apk add --no-cache \
    git \
    vim \
    zsh \
    tmux \
    curl \
    unzip \
    jq

# # RUN zsh -c exit

# RUN apt-get update && \
#     apt-get install -y locales ca-certificates && \
#     apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
#     localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
# ENV LANG en_US.UTF-8

# # RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
# # RUN locale-gen

# ENV PYENV_ROOT="/.pyenv" \
#     PATH="/.pyenv/bin:/.pyenv/shims:$PATH"

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends git ca-certificates curl && \
#     curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash && \
#     apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# RUN set -x; apt-get update && \
#     apt-get install -y --no-install-recommends \
#     make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
#     libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev \
#     libxml2-dev libxmlsec1-dev libffi-dev \
#     ca-certificates && \
#     apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
#     libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
#     xz-utils tk-dev libffi-dev liblzma-dev python-openssl git && \
#     apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# COPY python-versions.txt /
# RUN set -x; pyenv update && \
#     xargs -P 4 -n 1 pyenv install < /python-versions.txt && \
#     pyenv global $(pyenv versions --bare) && \
#     find $PYENV_ROOT/versions -type d '(' -name '__pycache__' -o -name 'test' -o -name 'tests' ')' -exec rm -rfv '{}' + && \
#     find $PYENV_ROOT/versions -type f '(' -name '*.py[co]' -o -name '*.exe' ')' -exec rm -fv '{}' + && \
#     mv -v -- /python-versions.txt $PYENV_ROOT/version

# COPY bin/startup.sh .
# RUN "./startup.sh"

# RUN mkdir /var/task

RUN pip install -U pip setuptools --no-cache-dir && \
    pip install -U virtualenv pipenv --no-cache-dir && \
    pip install -U virtualenvwrapper --no-cache-dir

RUN git config --global user.name "Jarvis" && \
    git config --global user.email jarvis@theblacktonystark.com && \
    git config --global core.editor vim && \
    git config --global credential.helper 'store --file ~/.git-credentials'
