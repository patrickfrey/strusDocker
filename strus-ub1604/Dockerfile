FROM patrickfrey/strus-ub1604-env
MAINTAINER patrickpfrey@yahoo.com

# Install scripts to test all
COPY test.sh /

# Project textwolf
RUN wget https://github.com/patrickfrey/textwolf/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project hyperscan
RUN git clone https://github.com/intel/hyperscan.git
RUN cd hyperscan && git checkout tags/v4.7.0

# Project lua
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

# Project strusPattern
RUN wget https://github.com/patrickfrey/strusPattern/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd strusPattern-master/3rdParty && cp -Rf ../../textwolf-master/* textwolf/

# Project strusVector
RUN wget https://github.com/patrickfrey/strusVector/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project strusUtilities
RUN wget https://github.com/patrickfrey/strusUtilities/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project strusBindings
RUN wget https://github.com/patrickfrey/strusBindings/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd strusBindings-master/3rdParty && cp -Rf ../../textwolf-master/* textwolf/
RUN cd strusBindings-master/3rdParty && cp -Rf ../../papuga-master/* papuga/

# Build
RUN cd hyperscan/ && cmake -DBUILD_SHARED_LIBS=1 -DCMAKE_BUILD_TYPE=Release . && make -j 6 && make install
RUN cd strusBase-master/ && cmake -DCMAKE_BUILD_TYPE=Release . && make && make install
RUN cd strus-master/ && cmake -DCMAKE_BUILD_TYPE=Release . && make && make install
RUN cd strusAnalyzer-master/ && cmake -DCMAKE_BUILD_TYPE=Release . && make && make install
RUN cd strusTrace-master/ && cmake -DCMAKE_BUILD_TYPE=Release . && make && make install
RUN cd strusModule-master/ && cmake -DCMAKE_BUILD_TYPE=Release . && make && make install
RUN cd strusRpc-master/ && cmake -DCMAKE_BUILD_TYPE=Release . && make && make install
RUN cd strusPattern-master/ && cmake -DCMAKE_BUILD_TYPE=Release . && make && make install
RUN cd strusVector-master/ && cmake -DCMAKE_BUILD_TYPE=Release . && make && make install
RUN cd strusUtilities-master/ && cmake -DCMAKE_BUILD_TYPE=Release . && make && make install
RUN cd strusBindings-master/ && cmake -DCMAKE_BUILD_TYPE=Release -DWITH_PHP=YES -DWITH_PYTHON=YES -DWITH_STRUS_VECTOR=YES -DWITH_STRUS_PATTERN=YES . && make && make install

