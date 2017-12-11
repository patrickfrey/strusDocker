FROM patrickfrey/strus-ub1404-env
MAINTAINER patrickpfrey@yahoo.com

# Project strus
RUN wget https://github.com/patrickfrey/strus/archive/v0.1.6.zip
RUN unzip v0.1.6.zip && rm v0.1.6.zip
RUN cd strus-0.1.6/ && cmake CMakeLists.txt && make && make install

# Project strusAnalyzer
RUN wget https://github.com/patrickfrey/strusAnalyzer/archive/v0.1.6.zip
RUN unzip v0.1.6.zip && rm v0.1.6.zip
RUN cd strusAnalyzer-0.1.6/ && cmake CMakeLists.txt && make && make install

# Project strusModule
RUN wget https://github.com/patrickfrey/strusModule/archive/v0.1.5.zip
RUN unzip v0.1.5.zip && rm v0.1.5.zip
RUN cd strusModule-0.1.5/ && cmake CMakeLists.txt && make && make install

# Project strusRpc with subproject libuv
RUN wget https://github.com/patrickfrey/strusRpc/archive/v0.1.9.zip
RUN unzip v0.1.9.zip && rm v0.1.9.zip
RUN cd strusRpc-0.1.9/ && cmake CMakeLists.txt && make && make install

# Project strusUtilities
RUN wget https://github.com/patrickfrey/strusUtilities/archive/v0.1.6.zip
RUN unzip v0.1.6.zip && rm v0.1.6.zip
RUN cd strusUtilities-0.1.6/ && cmake CMakeLists.txt && make && make install

# Set library search path
RUN echo /usr/local/lib/strus > /etc/ld.so.conf.d/strus.conf
RUN ldconfig

