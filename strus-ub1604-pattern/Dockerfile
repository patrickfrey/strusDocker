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

# Project strusBase
RUN wget https://github.com/patrickfrey/strusBase/archive/0.15.4.zip
RUN unzip 0.15.4.zip && rm 0.15.4.zip
RUN cd strusBase-0.15.4/ && cmake CMakeLists.txt && make && make install

# Project strus
RUN wget https://github.com/patrickfrey/strus/archive/0.15.4.zip
RUN unzip 0.15.4.zip && rm 0.15.4.zip
RUN cd strus-0.15.4/ && cmake CMakeLists.txt && make && make install

# Project strusAnalyzer
RUN wget https://github.com/patrickfrey/strusAnalyzer/archive/0.15.4.zip
RUN unzip 0.15.4.zip && rm 0.15.4.zip
RUN cd strusAnalyzer-0.15.4/3rdParty && cp -Rf ../../textwolf-master/* textwolf/
RUN cd strusAnalyzer-0.15.4/ && cmake CMakeLists.txt && make && make install

# Project strusTrace
RUN wget https://github.com/patrickfrey/strusTrace/archive/0.15.4.zip
RUN unzip 0.15.4.zip && rm 0.15.4.zip
RUN cd strusTrace-0.15.4/ && cmake CMakeLists.txt && make && make install

# Project strusModule
RUN wget https://github.com/patrickfrey/strusModule/archive/0.15.4.zip
RUN unzip 0.15.4.zip && rm 0.15.4.zip
RUN cd strusModule-0.15.4/ && cmake CMakeLists.txt && make && make install

# Project strusRpc
RUN wget https://github.com/patrickfrey/strusRpc/archive/0.15.4.zip
RUN unzip 0.15.4.zip && rm 0.15.4.zip
RUN cd strusRpc-0.15.4/ && cmake CMakeLists.txt && make && make install

# Project strusPattern
RUN wget https://github.com/patrickfrey/strusPattern/archive/0.15.4.zip
RUN unzip 0.15.4.zip && rm 0.15.4.zip
RUN cd strusPattern-0.15.4/3rdParty && cp -Rf ../../textwolf-master/* textwolf/
RUN cd strusPattern-0.15.4/ && cmake CMakeLists.txt && make && make install

# Project strusUtilities
RUN wget https://github.com/patrickfrey/strusUtilities/archive/0.15.4.zip
RUN unzip 0.15.4.zip && rm 0.15.4.zip
RUN cd strusUtilities-0.15.4/ && cmake CMakeLists.txt && make && make install

# Set library search path
RUN echo /usr/local/lib/strus > /etc/ld.so.conf.d/strus.conf
RUN ldconfig


