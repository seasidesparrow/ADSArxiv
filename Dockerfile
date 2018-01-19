FROM phusion/baseimage:0.9.22

RUN \
    DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
        wget \
        bzip2 \
        net-tools \
        curl \
        nano \
        build-essential \
        python \
        ipython \
        python-dev \
        python-pip \
        python-setuptools \
        libpq-dev && \
    DEBIAN_FRONTEND=noninteractive apt-get clean && \
    DEBIAN_FRONTEND=noninteractive apt-get autoremove --purge -y && \
    rm -rf /root/.cache/* /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --upgrade setuptools

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

ADD crontab /app/crontab
RUN crontab /app/crontab

CMD ["/sbin/my_init"]
