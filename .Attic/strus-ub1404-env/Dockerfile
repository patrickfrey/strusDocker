FROM ubuntu:14.04
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update \
 && apt-get -y --force-yes install \
	unzip wget git cmake \
	make g++ build-essential \
	debhelper

RUN apt-get -y --force-yes install \
	libboost1.54-dev \
	libboost-filesystem-dev \
	libboost-system-dev \
	libboost-regex1.54-dev \
	libboost-thread-dev

RUN apt-get -y --force-yes install \
	google-perftools libsnappy-dev libleveldb-dev

RUN apt-get -y --force-yes install \
	libevent-dev

