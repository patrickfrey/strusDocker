FROM patrickfrey/strus-ub1604-m32-env
MAINTAINER patrickpfrey@yahoo.com

# Project textwolf
RUN wget https://github.com/patrickfrey/textwolf/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project hyperscan
RUN wget https://github.com/01org/hyperscan/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project fmt
RUN wget https://github.com/fmtlib/fmt/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project lua
RUN wget https://github.com/lua/lua/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project papuga
RUN wget https://github.com/patrickfrey/papuga/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd papuga-master/3rdParty && cp -Rf ../../textwolf-master/* textwolf/
RUN cd papuga-master/3rdParty && cp -Rf ../../fmt-master/* fmt/
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

# Project strusPattern
RUN wget https://github.com/patrickfrey/strusPattern/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd strusPattern-master/3rdParty && cp -Rf ../../textwolf-master/* textwolf/ && cd ../..
RUN cd strusPattern-master/3rdParty && cp -Rf ../../hyperscan-master/* hyperscan/ && cd ../..

# Project strusVector
RUN wget https://github.com/patrickfrey/strusVector/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project strusUtilities
RUN wget https://github.com/patrickfrey/strusUtilities/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project strusBindings
RUN wget https://github.com/patrickfrey/strusBindings/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd strusBindings-master/3rdParty && cp -Rf ../../textwolf-master/* textwolf/ && cd ../..
RUN cd strusBindings-master/3rdParty && cp -Rf ../../papuga-master/* papuga/ && cd ../..

# Build:
RUN cd strusBase-master/ && cmake -DCPP_LANGUAGE_VERSION=11 -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS="-pthread -m32" -DCMAKE_CXX_FLAGS="-pthread -m32" -DBOOST_ROOT=/boost_1_58_0 . && make && make install
RUN cd strus-master/ && cmake -DCPP_LANGUAGE_VERSION=11 -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS="-pthread -m32" -DCMAKE_CXX_FLAGS="-pthread -m32" -DBOOST_ROOT=/boost_1_58_0 -DLEVELDB_ROOT=/leveldb-master . && make && make install
RUN cd strusAnalyzer-master/ && cmake -DCPP_LANGUAGE_VERSION=11 -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS="-pthread -m32" -DCMAKE_CXX_FLAGS="-pthread -m32" -DBOOST_ROOT=/boost_1_58_0 . && make && make install
RUN cd strusTrace-master/ && cmake -DCPP_LANGUAGE_VERSION=11 -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS="-pthread -m32" -DCMAKE_CXX_FLAGS="-pthread -m32" -DBOOST_ROOT=/boost_1_58_0 . && make && make install
RUN cd strusModule-master/ && cmake -DCPP_LANGUAGE_VERSION=11 -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS="-pthread -m32" -DCMAKE_CXX_FLAGS="-pthread -m32" -DBOOST_ROOT=/boost_1_58_0 . && make && make install && cd ..
RUN cd strusRpc-master/ && cmake -DCPP_LANGUAGE_VERSION=11 -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS="-pthread -m32" -DCMAKE_CXX_FLAGS="-pthread -m32" -DBOOST_ROOT=/boost_1_58_0 . && make && make install && cd ..
RUN cd strusUtilities-master/ && cmake -DCPP_LANGUAGE_VERSION=11 -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS="-pthread -m32" -DCMAKE_CXX_FLAGS="-pthread -m32" -DBOOST_ROOT=/boost_1_58_0 . && make && make install && cd ..
RUN cd strusBindings-master/ && cmake -DCPP_LANGUAGE_VERSION=11 -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS="-pthread -m32" -DCMAKE_CXX_FLAGS="-pthread -m32" -DBOOST_ROOT=/boost_1_58_0 -DWITH_PHP=NO -DWITH_PYTHON=NO -DWITH_STRUS_VECTOR=NO -DWITH_STRUS_PATTERN=NO . && make && make install && cd ..

COPY test.sh /


