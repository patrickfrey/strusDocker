FROM patrickfrey/strus-ub1604-pattern
MAINTAINER patrickpfrey@yahoo.com

COPY ./createNameRules.pl /home/strus/createNameRules.pl
COPY ./createNameRules.orig.pl /home/strus/createNameRules.orig.pl
COPY ./run.sh /home/strus/run.sh
COPY ./names.txt /home/strus/names.txt
COPY ./inputlist.txt /home/strus/inputlist.txt
ADD data /home/strus/data

RUN apt-get update
RUN apt-get --yes install perl

# Permissions for start in shell:
# -------------------------------
WORKDIR /home/strus
USER root



