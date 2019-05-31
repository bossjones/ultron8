FROM docker:18.09.6-dind

# container user
ARG CONTAINER_GID=501
ARG CONTAINER_UID=501
ARG CONTAINER_USER=developer

# host ip address
ARG HOST_IP

# set container user as environment variable
ENV CONTAINER_USER=${CONTAINER_USER}

ENV DEBIAN_FRONTEND noninteractive

# SOURCE: https://github.com/bossjones/ubuntu-devtop-vm/blob/482474d8c4cb44f2389a5b314ee050fbecdbdc2b/bionic/Dockerfile

# ENV LC_CTYPE en_US.UTF-8

RUN apt-get update && apt-get install -y \
    git \
    vim \
    zsh \
    tmux \
    locales \
    curl \
    unzip \
    jq

# RUN zsh -c exit

RUN apt-get update && \
    apt-get install -y locales ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.UTF-8

# RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
# RUN locale-gen

ENV PYENV_ROOT="/.pyenv" \
    PATH="/.pyenv/bin:/.pyenv/shims:$PATH"

RUN apt-get update && \
    apt-get install -y --no-install-recommends git ca-certificates curl && \
    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN set -x; apt-get update && \
    apt-get install -y --no-install-recommends \
    make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
    libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev \
    libxml2-dev libxmlsec1-dev libffi-dev \
    ca-certificates && \
    apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY python-versions.txt /
RUN set -x; pyenv update && \
    xargs -P 4 -n 1 pyenv install < /python-versions.txt && \
    pyenv global $(pyenv versions --bare) && \
    find $PYENV_ROOT/versions -type d '(' -name '__pycache__' -o -name 'test' -o -name 'tests' ')' -exec rm -rfv '{}' + && \
    find $PYENV_ROOT/versions -type f '(' -name '*.py[co]' -o -name '*.exe' ')' -exec rm -fv '{}' + && \
    mv -v -- /python-versions.txt $PYENV_ROOT/version

COPY bin/startup.sh .
RUN "./startup.sh"

RUN mkdir /var/task

RUN pip install -U pip setuptools --no-cache-dir && \
    pip install -U virtualenv pipenv --no-cache-dir && \
    pip install -U virtualenvwrapper --no-cache-dir

RUN git config --global user.name "Jarvis" && \
    git config --global user.email jarvis@theblacktonystark.com && \
    git config --global core.editor vim && \
    git config --global credential.helper 'store --file ~/.git-credentials'
