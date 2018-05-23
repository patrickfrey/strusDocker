FROM ubuntu:16.04
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update
RUN apt-get --yes install software-properties-common
RUN add-apt-repository universe

RUN apt-get update \
 && apt-get --yes install \
	unzip wget git \
	make g++ build-essential libc6-dev-x32 \
	g++-multilib gcc-multilib \
	debhelper python \
	autotools-dev autoconf libtool \
	ragel

RUN wget https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/cmake/3.9.0-1/cmake_3.9.0.orig.tar.gz
RUN tar -xvzf cmake_3.9.0.orig.tar.gz 
RUN cd cmake-3.9.0 && ./configure --prefix=/usr --bindir=/usr/bin && make && make install

RUN wget https://sourceforge.net/projects/boost/files/boost/1.58.0/boost_1_58_0.tar.gz
RUN tar -xvzf boost_1_58_0.tar.gz && rm boost_1_58_0.tar.gz
RUN cd boost_1_58_0 && ./bootstrap.sh --with-libraries=atomic,chrono,date_time,filesystem,program_options,regex,system,thread,timer
RUN cd boost_1_58_0 && ./b2 cxxflags=-m32 cflags=-m32 .; exit 0
RUN cd boost_1_58_0 && mkdir lib && mv stage/lib/* lib/

RUN wget https://github.com/google/snappy/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd snappy-master && cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS="-m32" -DCMAKE_CXX_FLAGS="-m32" . && make

RUN wget https://github.com/google/leveldb/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd leveldb-master/ && cmake . && make OPT="-m32 -O2 -DNDEBUG" LDFLAGS="-pthread -m32 -L../snappy-master" && make
RUN cd leveldb-master/ && mv out-shared lib


