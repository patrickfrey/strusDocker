FROM patrickfrey/strus-ub1404-bind:v0_2
MAINTAINER patrickpfrey@yahoo.com

COPY ./countries.ana /home/strus/
COPY ./countries.xml /home/strus/
COPY ./search_error_html.tpl /home/strus/
COPY ./search_html.tpl /home/strus/
COPY ./searchlink_html.tpl /home/strus/
COPY ./strusIR.py /home/strus/
COPY ./strusServer.py /home/strus/

# Permissions for start in shell:
# -------------------------------
WORKDIR /home/strus
USER root

# Mapped ports:
# -------------
EXPOSE 80

