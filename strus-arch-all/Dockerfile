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

# Project strusWebService
RUN wget https://github.com/patrickfrey/strusWebService/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project strusAll
RUN wget https://github.com/patrickfrey/strusAll/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd strusAll-master && cp -Rf ../strusBase-master/* strusBase/
RUN cd strusAll-master && cp -Rf ../strus-master/* strus/
RUN cd strusAll-master && cp -Rf ../strusAnalyzer-master/* strusAnalyzer/
RUN cd strusAll-master && cp -Rf ../strusTrace-master/* strusTrace/
RUN cd strusAll-master && cp -Rf ../strusModule-master/* strusModule/
RUN cd strusAll-master && cp -Rf ../strusRpc-master/* strusRpc/
RUN cd strusAll-master && cp -Rf ../strusVector-master/* strusVector/
RUN cd strusAll-master && cp -Rf ../strusUtilities-master/* strusUtilities/
RUN cd strusAll-master && cp -Rf ../strusBindings-master/* strusBindings/

RUN cd strusAll-master \
	&& mkdir -p build \
	&& cd build \
	&& cmake -DCMAKE_BUILD_TYPE=Release \
		-DWITH_LUA=YES \
		-DWITH_PYTHON=YES \
		-DWITH_PHP=YES \
		-DWITH_STRUS_VECTOR=YES \
		-DWITH_STRUS_PATTERN=NO \
		.. \
	&& make -j 7 \
	&& make install

RUN cd strusWebService-master \
	&& mkdir -p build \
	&& cd build \
	&& cmake -DCMAKE_C_COMPILER="clang" -DCMAKE_CXX_COMPILER="clang++" -DCMAKE_BUILD_TYPE=Release .. \
	&& make -j 6 && make install

# Set library search path
RUN echo /usr/local/lib/strus > /etc/ld.so.conf.d/strus.conf
RUN ldconfig


