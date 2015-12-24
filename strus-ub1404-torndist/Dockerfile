FROM patrickfrey/strus-ub1404-bind:v0_3
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update \
	&& apt-get -y --force-yes install \
	python-tornado python-snappy python-pip curl

RUN pip install websocket-client

COPY search_base_html.tpl /home/strus/search_base_html.tpl
COPY search_bm25_html.tpl /home/strus/search_bm25_html.tpl
COPY search_error_html.tpl /home/strus/search_error_html.tpl
COPY strusIR.py /home/strus/strusIR.py
COPY strusMessage.py /home/strus/strusMessage.py
COPY strusHttpServer.py /home/strus/strusHttpServer.py
COPY strusStatisticsServer.py /home/strus/strusStatisticsServer.py
COPY strusStorageServer.py /home/strus/strusStorageServer.py
COPY storage.conf /home/strus/storage.conf
COPY document.ana /home/strus/document.ana
COPY prepare.sh /home/strus/prepare.sh
COPY insert_docs.sh /home/strus/insert_docs.sh
COPY query.sh /home/strus/query.sh

ENV PYTHONPATH /usr/local/lib/strus/python

# Permissions for start in shell:
# -------------------------------
WORKDIR /home/strus
USER root

# Mapped ports:
# -------------
EXPOSE 80

