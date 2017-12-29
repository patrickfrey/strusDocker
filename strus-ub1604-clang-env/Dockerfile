FROM ubuntu:16.04
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update
RUN apt-get --yes install software-properties-common
RUN add-apt-repository universe

RUN apt-get update \
 && apt-get --yes install \
	unzip wget git \
	cmake make \
	llvm build-essential clang-3.8 lldb-3.8 \
	debhelper

RUN update-alternatives --install /usr/bin/clang clang /usr/bin/clang-3.8 380 \
	--slave /usr/bin/clang++ clang++ /usr/bin/clang++-3.8 \
	--slave /usr/bin/lldb lldb /usr/bin/lldb-3.8 \
	--slave /usr/bin/lldb-server lldb-server /usr/bin/lldb-server-3.8 \
	--slave	/usr/bin/clang-check clang-check /usr/bin/clang-check-3.8 \
	--slave /usr/bin/clang-query clang-query /usr/bin/clang-query-3.8 \
	--slave /usr/bin/clang-rename clang-rename /usr/bin/clang-rename-3.8

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
	php7.0-dev
