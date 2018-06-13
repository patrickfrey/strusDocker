FROM jaschac/debian-gcc:latest
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update \
 && apt-get --yes install \
	unzip wget git cmake gcc-8 \
	debhelper

ENV LANG "en_US.UTF-8"
ENV LC_ALL "en_US.UTF-8"

RUN apt-get -y --yes install \
	libboost-all-dev \
	libleveldb-dev \
	libtre-dev \
	libuv-dev \
	ragel \
	libatlas-dev \
	liblapack-dev \
	libblas-dev \
	python3-dev \
	zlib1g-dev \
	libxml2-dev

