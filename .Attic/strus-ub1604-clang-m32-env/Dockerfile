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
	g++-multilib gcc-multilib \
	debhelper python \
	autotools-dev autoconf libtool

RUN update-alternatives --install /usr/bin/clang clang /usr/bin/clang-3.8 380 \
	--slave /usr/bin/clang++ clang++ /usr/bin/clang++-3.8 \
	--slave	/usr/bin/clang-check clang-check /usr/bin/clang-check-3.8 \
	--slave /usr/bin/clang-query clang-query /usr/bin/clang-query-3.8 \
	--slave /usr/bin/clang-rename clang-rename /usr/bin/clang-rename-3.8


ENV LANG "en_US.UTF-8"
ENV LC_ALL "en_US.UTF-8"

RUN apt-get -y --yes install \
	ragel \
	language-pack-en-base

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
RUN cd leveldb-master/ && make OPT="-m32 -O2 -DNDEBUG" LDFLAGS="-pthread -m32 -L../snappy-master" && make
RUN cd leveldb-master/ && mv out-shared lib


