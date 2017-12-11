FROM patrickfrey/strus-arch-env
MAINTAINER patrickpfrey@yahoo.com

# Project textwolf
RUN wget https://github.com/patrickfrey/textwolf/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project fmt
RUN wget https://github.com/fmtlib/fmt/archive/master.zip
RUN unzip master.zip && rm master.zip

RUN wget https://github.com/lua/lua/archive/master.zip
RUN unzip master.zip && rm master.zip

# Project papuga
RUN wget https://github.com/patrickfrey/papuga/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd papuga-master/3rdParty && cp -Rf ../../textwolf-master/* textwolf/
RUN cd papuga-master/3rdParty && cp -Rf ../../fmt-master/* fmt/
RUN cd papuga-master/3rdParty && cp -Rf ../../lua-master/* lua/

# Project hyperscan
RUN wget https://github.com/01org/hyperscan/archive/master.zip
RUN unzip master.zip && rm master.zip

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
RUN cd strusPattern-master/3rdParty && cp -Rf ../../hyperscan-master/* hyperscan/

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

# Project strusAll
RUN wget https://github.com/patrickfrey/strusAll/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd strusAll-master && cp -Rf ../strusBase-master/* strusBase/
RUN cd strusAll-master && cp -Rf ../strus-master/* strus/
RUN cd strusAll-master && cp -Rf ../strusAnalyzer-master/* strusAnalyzer/
RUN cd strusAll-master && cp -Rf ../strusTrace-master/* strusTrace/
RUN cd strusAll-master && cp -Rf ../strusModule-master/* strusModule/
RUN cd strusAll-master && cp -Rf ../strusRpc-master/* strusRpc/
RUN cd strusAll-master && cp -Rf ../strusPattern-master/* strusPattern/
RUN cd strusAll-master && cp -Rf ../strusVector-master/* strusVector/
RUN cd strusAll-master && cp -Rf ../strusUtilities-master/* strusUtilities/
RUN cd strusAll-master && cp -Rf ../strusBindings-master/* strusBindings/
RUN cd strusAll-master \
	&& mkdir -p build \
	&& cd build \
	&& cmake -DCMAKE_BUILD_TYPE=Release \
		-DWITH_PYTHON=YES \
		-DWITH_PHP=YES \
		-DWITH_STRUS_VECTOR=YES \
		-DWITH_STRUS_PATTERN=YES \
		.. \
	&& make -j 7 \
	&& CTEST_OUTPUT_ON_FAILURE=1 make test \
	&& make install

# Set library search path
RUN echo /usr/local/lib/strus > /etc/ld.so.conf.d/strus.conf
RUN ldconfig

