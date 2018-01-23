FROM ubuntu:trusty

MAINTAINER steve@steven-west.com

RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository -y ppa:stebbins/handbrake-releases \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
        handbrake-cli
#    && apt-get remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) \
#    && rm -rf /var/lib/apt/lists/*

ADD handbrake-proc.py .
ADD presets/* /presets/

CMD python3 handbrake-proc.py
