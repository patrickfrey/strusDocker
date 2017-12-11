FROM patrickfrey/strus-ub1404-env
MAINTAINER patrickpfrey@yahoo.com

# Project strus
RUN wget https://github.com/patrickfrey/strus/archive/0.3.4.zip
RUN unzip 0.3.4.zip && rm 0.3.4.zip
RUN cd strus-0.3.4/ && cmake CMakeLists.txt && make && make install

# Project strusAnalyzer
RUN wget https://github.com/patrickfrey/strusAnalyzer/archive/0.3.1.zip
RUN unzip 0.3.1.zip && rm 0.3.1.zip
RUN cd strusAnalyzer-0.3.1/ && cmake CMakeLists.txt && make && make install

# Project strusModule
RUN wget https://github.com/patrickfrey/strusModule/archive/0.3.1.zip
RUN unzip 0.3.1.zip && rm 0.3.1.zip
RUN cd strusModule-0.3.1/ && cmake CMakeLists.txt && make && make install

# Project strusRpc with subproject libuv
RUN wget https://github.com/patrickfrey/strusRpc/archive/0.3.1.zip
RUN unzip 0.3.1.zip && rm 0.3.1.zip
RUN cd strusRpc-0.3.1/ && cmake CMakeLists.txt && make && make install

# Project strusUtilities
RUN wget https://github.com/patrickfrey/strusUtilities/archive/0.3.2.zip
RUN unzip 0.3.2.zip && rm 0.3.2.zip
RUN cd strusUtilities-0.3.2/ && cmake CMakeLists.txt && make && make install

# Set library search path
RUN echo /usr/local/lib/strus > /etc/ld.so.conf.d/strus.conf
RUN ldconfig

