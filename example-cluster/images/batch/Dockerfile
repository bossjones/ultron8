FROM ubuntu:trusty

RUN apt-get update > /dev/null && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        debhelper \
        dpkg-dev \
        devscripts \
        faketime \
        wget \
        gdebi-core \
        git \
        gcc \
        python-dev \
        coffeescript \
        libdb5.3-dev \
        libyaml-dev \
        libssl-dev \
        libffi-dev \
        ssh \
        rsyslog \
        && apt-get clean > /dev/null

RUN useradd -ms /bin/bash ultron && mkdir -p /home/ultron/.ssh
ADD example-cluster/images/batch/insecure_key.pub /home/ultron
RUN cat /home/ultron/insecure_key.pub > /home/ultron/.ssh/authorized_keys

RUN wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
RUN python /tmp/get-pip.py
RUN pip install -U tox wheel setuptools PyYAML

WORKDIR /work
