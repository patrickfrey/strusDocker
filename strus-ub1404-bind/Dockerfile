FROM patrickfrey/strus-ub1404
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update \
 && apt-get -y --force-yes install \
	swig php5-dev

RUN wget https://github.com/patrickfrey/strusBindings/archive/v0.1.5.zip
RUN unzip v0.1.5.zip && rm v0.1.5.zip
RUN cd strusBindings-0.1.5/\
	&& cmake CMakeLists.txt && make && make install\
	&& cp swig/php/strus.so `php-config --extension-dir`/\
	&& cp swig/strus.php /usr/share/php/


