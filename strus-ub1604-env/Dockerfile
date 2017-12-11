FROM ubuntu:16.04
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update
RUN apt-get --yes install software-properties-common
RUN add-apt-repository universe

RUN apt-get update \
 && apt-get --yes install \
	unzip wget git cmake \
	make g++ build-essential \
	debhelper

ENV LANG "en_US.UTF-8"
ENV LC_ALL "en_US.UTF-8"

RUN apt-get -y --yes install \
	libboost1.58-dev \
	libboost-filesystem1.58-dev \
	libboost-system1.58-dev \
	libboost-regex1.58-dev \
	libboost-thread1.58-dev \
	libsnappy-dev \
	libleveldb-dev \
	libtre-dev \
	libuv-dev \
	ragel \
	libatlas-dev \
	liblapack-dev \
	libblas-dev \
	python3-dev \
	zlib1g-dev \
	libxml2-dev \
	language-pack-en-base

RUN locale-gen en_US.UTF-8
RUN add-apt-repository -y ppa:ondrej/php
RUN apt-get update
RUN apt-get install -y php7.1 php7.1-dev

