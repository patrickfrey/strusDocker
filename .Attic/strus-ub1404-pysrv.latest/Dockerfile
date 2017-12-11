FROM patrickfrey/strus-ub1404:latest
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update \
 && apt-get -y --force-yes install \
	swig \
	python2.7 python2.7-dev \
	python-distribute python-pip

RUN pip install tornado

RUN wget https://github.com/patrickfrey/strusBindings/archive/master.zip
RUN unzip master.zip && rm master.zip
RUN cd strusBindings-master/\
	&& cmake CMakeLists.txt -DWITH_PYTHON=YES && make && make install \
	&& cp swig/python/strus.py /usr/share/python/

COPY ./strusServer.py /home/strus/strusServer.py
COPY ./strusIR.py /home/strus/strusIR.py
COPY ./strus.css /home/strus/strus.css
COPY ./search.html /home/strus/search.html
COPY ./search_error.html /home/strus/search_error.html
COPY ./search_button.jpg /home/strus/search_button.jpg
COPY ./strus_logo.ico /home/strus/favicon.ico
COPY ./strus_logo.jpg /home/strus/strus_logo.jpg
COPY ./arrow-down.png /home/strus/arrow-down.png
COPY ./arrow-up.png /home/strus/arrow-up.png
COPY ./irregular_verbs_en.txt /home/strus/irregular_verbs_en.txt

# There does not seem to exist a python standard path for extensions:
ENV PYTHONPATH /usr/share/python/:/usr/local/lib/strus/python

# Permissions for start in shell:
# -------------------------------
WORKDIR /home/strus
USER root

# Mapped ports:
# -------------
EXPOSE 80


