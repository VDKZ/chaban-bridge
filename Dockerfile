FROM ubuntu:22.04 as deps

ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1

RUN useradd -m -N alex
WORKDIR /home/alex

RUN mkdir -p /var/log/supervisord
RUN chown -R alex:users /var/log/supervisord

RUN apt-get update \
    && apt-get install -y build-essential software-properties-common \
    && apt-get install -y libpq-dev curl nano postgresql-client git \
        python3.10 python3.10-dev libpython3.10-dev python3.10-distutils \
        python3.10-venv python3.10-venv \
        pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl \
    && apt clean -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man/?? /usr/share/man/??_*


RUN ln -sSL /usr/bin/python3.10 /usr/bin/python
RUN curl -s https://bootstrap.pypa.io/get-pip.py | python

USER alex
RUN python -m pip install virtualenv && rm -rf ~/.cache/pip
ENV PATH="/home/alex/.local/bin:$PATH"
RUN virtualenv env -p /usr/bin/python3.10
ENV VIRTUAL_ENV=/home/alex/env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python -m pip install --upgrade pip setuptools wheel && rm -rf ~/.cache/pip

CMD bash

FROM deps as dev

ENV APP_EXEC_MODE_RUNSERVER=1

# Needed for pre-commits
USER root
RUN add-apt-repository ppa:git-core/ppa -y && apt-get update \
    && apt-get install -y git \
    && apt clean -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man/?? /usr/share/man/??_*
USER alex

COPY --chown=alex:users requirements.txt .
COPY --chown=alex:users requirements-dev.txt .
RUN pip3 install -r requirements.txt -r requirements-dev.txt \
    && rm -rf ~/.cache/pip

COPY --chown=alex:users chaban_bridge ./chaban_bridge
COPY --chown=alex:users supervisord.conf ./supervisord.conf

CMD supervisord -c /home/alex/supervisord.conf