FROM patrickfrey/strus-arch-env
MAINTAINER patrickpfrey@yahoo.com

# Install scripts to test all
COPY test.sh /

# Project textwolf
RUN wget https://github.com/patrickfrey/textwolf/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project Lua
RUN wget https://github.com/lua/lua/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project papuga
RUN wget https://github.com/patrickfrey/papuga/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd papuga-master/3rdParty && cp -Rf ../../textwolf-master/* textwolf/
RUN cd papuga-master/3rdParty && cp -Rf ../../lua-master/* lua/

# Project strusBase
RUN wget https://github.com/patrickfrey/strusBase/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project strus
RUN wget https://github.com/patrickfrey/strus/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project strusAnalyzer
RUN wget https://github.com/patrickfrey/strusAnalyzer/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd strusAnalyzer-master/3rdParty && cp -Rf ../../textwolf-master/* textwolf/

# Project strusTrace
RUN wget https://github.com/patrickfrey/strusTrace/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project strusModule
RUN wget https://github.com/patrickfrey/strusModule/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project strusRpc
RUN wget https://github.com/patrickfrey/strusRpc/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project strusUtilities
RUN wget https://github.com/patrickfrey/strusUtilities/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project strusBindings
RUN wget https://github.com/patrickfrey/strusBindings/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd strusBindings-master/3rdParty && cp -Rf ../../textwolf-master/* textwolf/
RUN cd strusBindings-master/3rdParty && cp -Rf ../../papuga-master/* papuga/

# Project strusAll
# Build
RUN cd strusBase-master/ && cmake -DCMAKE_C_COMPILER="clang" -DCMAKE_CXX_COMPILER="clang++" -DCMAKE_BUILD_TYPE=Release . && make -j 6 && make install
RUN cd strus-master/ && cmake -DCMAKE_C_COMPILER="clang" -DCMAKE_CXX_COMPILER="clang++" -DCMAKE_BUILD_TYPE=Release . && make -j 6 && make install
RUN cd strusAnalyzer-master/ && cmake -DCMAKE_C_COMPILER="clang" -DCMAKE_CXX_COMPILER="clang++" -DCMAKE_BUILD_TYPE=Release . && make -j 6 && make install
RUN cd strusTrace-master/ && cmake -DCMAKE_C_COMPILER="clang" -DCMAKE_CXX_COMPILER="clang++" -DCMAKE_BUILD_TYPE=Release . && make -j 6 && make install
RUN cd strusModule-master/ && cmake -DCMAKE_C_COMPILER="clang" -DCMAKE_CXX_COMPILER="clang++" -DCMAKE_BUILD_TYPE=Release . && make -j 6 && make install
RUN cd strusRpc-master/ && cmake -DCMAKE_C_COMPILER="clang" -DCMAKE_CXX_COMPILER="clang++" -DCMAKE_BUILD_TYPE=Release . && make -j 6 && make install
RUN cd strusUtilities-master/ && cmake -DCMAKE_C_COMPILER="clang" -DCMAKE_CXX_COMPILER="clang++" -DCMAKE_BUILD_TYPE=Release . && make -j 6 && make install
RUN cd strusBindings-master/ && cmake -DCMAKE_C_COMPILER="clang" -DCMAKE_CXX_COMPILER="clang++" -DCMAKE_BUILD_TYPE=Release -DWITH_PHP=YES -DWITH_PYTHON=YES -DWITH_STRUS_VECTOR=NO -DWITH_STRUS_PATTERN=NO -DWITH_WEBREQUEST=NO . && make -j 6 && make install

# Set library search path
RUN echo /usr/local/lib/strus > /etc/ld.so.conf.d/strus.conf
RUN ldconfig


