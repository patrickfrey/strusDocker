FROM patrickfrey/strus-ub1404-bind:v0_2_4
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update \
	&& apt-get -y --force-yes install \
	python-tornado curl

COPY src/step4/strusServer.py /home/strus/src/step4/strusServer.py
COPY src/step5/search_error_html.tpl /home/strus/src/step5/search_error_html.tpl
COPY src/step5/search_base_html.tpl /home/strus/src/step5/search_base_html.tpl
COPY src/step5/search_nblnk_html.tpl /home/strus/src/step5/search_nblnk_html.tpl
COPY src/step5/search_bm25_html.tpl /home/strus/src/step5/search_bm25_html.tpl
COPY src/step6/strusIR.py /home/strus/src/step6/strusIR.py
COPY src/step6/strusServer.py /home/strus/src/step6/strusServer.py
COPY src/step8/strusIR.py /home/strus/src/step8/strusIR.py
COPY countries.xml /home/strus/countries.xml

ENV PYTHONPATH /usr/local/lib/strus/python

# Permissions for start in shell:
# -------------------------------
WORKDIR /home/strus
USER root

# Mapped ports:
# -------------
EXPOSE 80

