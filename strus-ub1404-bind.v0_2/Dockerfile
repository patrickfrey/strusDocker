FROM patrickfrey/strus-ub1404:v0_2
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update \
 && apt-get -y --force-yes install \
	swig php5-dev openjdk-7-jdk \
	openjdk-7-jre-lib \
	python2.7 python2.7-dev libboost-python-dev

# Get around a bug in CMAKE FindJava:
ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64

RUN wget https://github.com/patrickfrey/strusBindings/archive/0.2.0.zip
RUN unzip 0.2.0.zip && rm 0.2.0.zip
RUN cd strusBindings-0.2.0/\
	&& cmake CMakeLists.txt -DWITH_PHP=YES -DWITH_PYTHON=YES -DWITH_JAVA=YES && make && make install


