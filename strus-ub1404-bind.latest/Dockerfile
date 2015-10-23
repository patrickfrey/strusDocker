FROM patrickfrey/strus-ub1404:latest
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update \
 && apt-get -y --force-yes install \
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
	&& cp swig/php/strus_php.so `php-config --extension-dir`/strus.so \
	&& cp swig/php/strus.php /usr/share/php/ \
	&& cp swig/python/strus.py /usr/share/python/


