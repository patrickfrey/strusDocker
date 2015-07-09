FROM patrickfrey/strus-ub1404-env
MAINTAINER patrickpfrey@yahoo.com

RUN wget https://github.com/patrickfrey/strus/archive/v0.1.1.zip
RUN unzip v0.1.1.zip && rm v0.1.1.zip
RUN cd strus-0.1.1/ && cmake CMakeLists.txt && make && make install

RUN wget https://github.com/patrickfrey/strusAnalyzer/archive/v0.1.1.zip
RUN unzip v0.1.1.zip && rm v0.1.1.zip
RUN cd strusAnalyzer-0.1.1/ && cmake CMakeLists.txt && make && make install

RUN wget https://github.com/patrickfrey/strusModule/archive/v0.1.1.zip
RUN unzip v0.1.1.zip && rm v0.1.1.zip
RUN cd strusModule-0.1.1/ && cmake CMakeLists.txt && make && make install

RUN wget https://github.com/patrickfrey/strusRpc/archive/v0.1.1.zip
RUN unzip v0.1.1.zip && rm v0.1.1.zip
RUN cd strusRpc-0.1.1/ && cmake CMakeLists.txt && make && make install

RUN wget https://github.com/patrickfrey/strusUtilities/archive/v0.1.1.zip
RUN unzip v0.1.1.zip && rm v0.1.1.zip
RUN cd strusUtilities-0.1.1/ && cmake CMakeLists.txt && make && make install

RUN echo /usr/local/lib/strus > /etc/ld.so.conf.d/strus.conf
RUN ldconfig

