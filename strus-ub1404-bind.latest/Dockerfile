FROM patrickfrey/strus-ub1404:latest
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update \
 && apt-get -y --force-yes install \
	libboost-python1.54-dev \
	swig php5-dev openjdk-7-jdk \
	openjdk-7-jre-lib \
	python2.7 python2.7-dev

# Get around a bug in CMAKE FindJava:
ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64
# There does not seem to exist a python standard path for extensions:
ENV PYTHONPATH /usr/share/python/:/usr/local/lib/strus/python

RUN wget https://github.com/patrickfrey/strusBindings/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd strusBindings-master/\
	&& cmake CMakeLists.txt -DWITH_PHP=YES -DWITH_PYTHON=YES -DWITH_JAVA=YES && make && make install\
	&& cp lang/php/strus.so `php-config --extension-dir`/strus.so \
	&& cp lang/php/strus.php /usr/share/php/


