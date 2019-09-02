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
RUN update-ca-certificates

ENV GPG_KEY 0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D
ENV PYTHON_VERSION 3.7.4

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
    --enable-optimizations \
		--enable-shared \
		--with-system-expat \
		--with-system-ffi \
		--without-ensurepip \
	&& make -j "$(nproc)" \
# set thread stack size to 1MB so we don't segfault before we hit sys.getrecursionlimit()
# https://github.com/alpinelinux/aports/commit/2026e1259422d4e0cf92391ca2d3844356c649d0
		EXTRA_CFLAGS="-DTHREAD_STACK_SIZE=0x100000" \
    # setting PROFILE_TASK makes "--enable-optimizations" reasonable: https://bugs.python.org/issue36044 / https://github.com/docker-library/python/issues/160#issuecomment-509426916
    PROFILE_TASK='-m test.regrtest --pgo \
      test_array \
      test_base64 \
      test_binascii \
      test_binhex \
      test_binop \
      test_bytes \
      test_c_locale_coercion \
      test_class \
      test_cmath \
      test_codecs \
      test_compile \
      test_complex \
      test_csv \
      test_decimal \
      test_dict \
      test_float \
      test_fstring \
      test_hashlib \
      test_io \
      test_iter \
      test_json \
      test_long \
      test_math \
      test_memoryview \
      test_pickle \
      test_re \
      test_set \
      test_slice \
      test_struct \
      test_threading \
      test_time \
      test_traceback \
      test_unicode \
    ' \
	&& make install \
	\
	&& find /usr/local -type f -executable -not \( -name '*tkinter*' \) -exec scanelf --needed --nobanner --format '%n#p' '{}' ';' \
		| tr ',' '\n' \
		| sort -u \
		| awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
		| xargs -rt apk add --no-cache --virtual .python-rundeps \
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

RUN apk add --no-cache --update \
  bash \
  build-base \
  bzip2-dev \
  ca-certificates \
  curl \
  git \
  jq \
  linux-headers \
  ncurses-dev \
  openssl \
  openssl-dev \
  patch \
  readline-dev \
  sqlite-dev \
  tmux \
  unzip \
  vim \
  zsh \
    && \
  rm -rf /var/cache/apk/*

# # RUN zsh -c exit

# RUN apt-get update && \
#     apt-get install -y locales ca-certificates && \
#     apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
#     localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
# ENV LANG en_US.UTF-8

# # RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
# # RUN locale-gen

ENV PYENV_ROOT="/.pyenv" \
    PATH="/.pyenv/bin:/.pyenv/shims:$PATH"

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends git ca-certificates curl && \
#     curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash && \
#     apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash && \
    git clone https://github.com/pyenv/pyenv-virtualenvwrapper ${PYENV_ROOT}/plugins/pyenv-virtualenvwrapper && \
    git clone https://github.com/pyenv/pyenv-pip-migrate ${PYENV_ROOT}/plugins/pyenv-pip-migrate && \
    git clone https://github.com/jawshooah/pyenv-default-packages ${PYENV_ROOT}/plugins/pyenv-default-packages

COPY default-packages ${PYENV_ROOT}/default-packages

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

ENV CI true
ENV PYTHON_CONFIGURE_OPTS="--enable-shared"
ENV PYTHONDONTWRITEBYTECODE 1


# ----------------------------------------------------------------------------------------------
# https://github.com/alpinelinux/aports/pull/6980/files
# https://bugs.alpinelinux.org/issues/10209
# https://stackoverflow.com/questions/55475157/pam-authentication-failure-when-running-chpasswd-on-alpine-linux
# FIXME: `PAM: Authentication failure` when running `chpasswd` on Alpine Linux
# ----------------------------------------------------------------------------------------------
# echo "auth     sufficient pam_rootok.so" | tee /etc/pam.d/chpasswd
# echo "account  include    base-account" | tee -a /etc/pam.d/chpasswd
# echo "password include    base-password" | tee -a /etc/pam.d/chpasswd
# ----------------------------------------------------------------------------------------------

# echo "auth		include		base-auth" | tee /etc/pam.d/login && \
# echo "account		include		base-account" | tee -a /etc/pam.d/login && \
# echo "password	include		base-password" | tee -a /etc/pam.d/login && \
# echo "session		include		base-session" | tee -a /etc/pam.d/login && \

RUN apk add --no-cache --update tree shadow sudo bash linux-pam && \
    echo -e "\n\n\n" && \
    cat /etc/pam.d/chpasswd && \
    echo -e "BEFORE" && \
    echo -e "\n\n\n" && \
    ls -lta /etc/pam.d && \
    echo -e "\n\n\n" && \
    echo "auth     sufficient pam_rootok.so" > /etc/pam.d/chpasswd && \
    echo "account  include    base-account" >> /etc/pam.d/chpasswd && \
    echo "password include    base-password" >> /etc/pam.d/chpasswd && \
    echo -e "\n\n\n" && \
    echo -e "AFTER - chpasswd" && \
    cat /etc/pam.d/chpasswd && \
    echo -e "\n\n\n" && \
    echo -e "BEFORE - login" && \
    cat /etc/pam.d/login && \
    echo "auth		include		base-auth" > /etc/pam.d/login && \
    echo "account		include		base-account" >> /etc/pam.d/login && \
    echo "password	include		base-password" >> /etc/pam.d/login && \
    echo "session		include		base-session" >> /etc/pam.d/login && \
    echo -e "AFTER - login" && \
    cat /etc/pam.d/login && \
    echo -e "\n\n\n" && \

    echo -e "\n\n\n" && \
    echo -e "BEFORE - useradd" && \
    cat /etc/pam.d/useradd && \
    sed -i "s,account		required	pam_permit.so,account		include		base-account,g" /etc/pam.d/useradd && \
    sed -i "s,password	include		system-auth,password	include		base-password,g" /etc/pam.d/useradd && \
    echo -e "AFTER - useradd" && \
    cat /etc/pam.d/useradd && \
    echo -e "\n\n\n" && \
    \
    if [ -z "`getent group $CONTAINER_GID`" ]; then \
      addgroup -S -g $CONTAINER_GID $CONTAINER_USER; \
    else \
      groupmod -n $CONTAINER_USER `getent group $CONTAINER_GID | cut -d: -f1`; \
    fi && \
    if [ -z "`getent passwd $CONTAINER_UID`" ]; then \
      adduser -S -h /home/${CONTAINER_USER} -u $CONTAINER_UID -G $CONTAINER_USER -s /bin/sh $CONTAINER_USER; \
    else \
      usermod -l $CONTAINER_USER -g $CONTAINER_GID -d /home/$CONTAINER_USER -m `getent passwd $CONTAINER_UID | cut -d: -f1`; \
    fi && \
    echo "${CONTAINER_USER} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$CONTAINER_USER && \
    chmod 0440 /etc/sudoers.d/$CONTAINER_USER && \
    mkdir /home/${CONTAINER_USER}/.ssh && \
    chmod og-rwx /home/${CONTAINER_USER}/.ssh && \
    echo 'export PATH="~/.local/bin:${PATH}"' >> /etc/profile.d/${CONTAINER_USER}.sh && \
    echo 'export PATH="/home/${CONTAINER_USER}/.local/bin:${PATH}"' >> /etc/profile.d/${CONTAINER_USER}.sh && \
    chown -R ${CONTAINER_USER}:${CONTAINER_USER} /home/${CONTAINER_USER}


COPY vagrant_insecure_key /home/${CONTAINER_USER}
COPY vagrant_insecure_key.pub /home/${CONTAINER_USER}
RUN cat /home/${CONTAINER_USER}/vagrant_insecure_key > /home/${CONTAINER_USER}/.ssh/id_rsa
RUN cat /home/${CONTAINER_USER}/vagrant_insecure_key.pub > /home/${CONTAINER_USER}/.ssh/id_rsa.pub

# COPY python-versions.txt /
COPY --chown=developer:developer python-versions.txt /
RUN set -x; pyenv update && \
    xargs -P 4 -n 1 pyenv install < /python-versions.txt && \
    pyenv global $(pyenv versions --bare) && \
    find $PYENV_ROOT/versions -type d '(' -name '__pycache__' -o -name 'test' -o -name 'tests' ')' -exec rm -rfv '{}' + && \
    find $PYENV_ROOT/versions -type f '(' -name '*.py[co]' -o -name '*.exe' ')' -exec rm -fv '{}' + && \
    mv -v -- /python-versions.txt $PYENV_ROOT/version && \
    chown -R ${CONTAINER_USER}:${CONTAINER_USER} ${PYENV_ROOT}

COPY pyenv-init.sh /pyenv-init.sh

# COPY bin/startup.sh .
# RUN "./startup.sh"

# RUN mkdir /var/task

# RUN set -xe \
#     && apk add --no-cache shadow sudo \
#     && cat /etc/group \
#     && addgroup -g ${CONTAINER_GID} ${CONTAINER_USER} \
#     && adduser -s /bin/bash -h /home/${CONTAINER_USER} -G ${CONTAINER_USER} ${CONTAINER_USER} \
#     && mkdir /home/${CONTAINER_USER}/.ssh \
#     && chmod og-rwx /home/${CONTAINER_USER}/.ssh \
#     && echo "${CONTAINER_USER}     ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/${CONTAINER_USER} \
#     && echo "%${CONTAINER_USER}     ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/${CONTAINER_USER} \
#     && cat /etc/sudoers


    # && addgroup ${CONTAINER_USER} adm \
    # && addgroup ${CONTAINER_USER} tty \
    # && addgroup ${CONTAINER_USER} daemon \

    #  \
    # && echo "password:password" | chpasswd

RUN pip install -U pip setuptools --no-cache-dir && \
    pip install -U virtualenv pipenv --no-cache-dir && \
    pip install -U virtualenvwrapper --no-cache-dir

RUN find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

RUN git config --global user.name "Jarvis" && \
    git config --global user.email jarvis@theblacktonystark.com && \
    git config --global core.editor vim && \
    git config --global credential.helper 'store --file ~/.git-credentials'
