FROM patrickfrey/strus-ub1604:v0_15
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update \
 && apt-get -y --force-yes install nginx php7.1 php7.1-cli php7.1-cgi php7.1-fpm vim
RUN rm -v /etc/nginx/nginx.conf

COPY ./strus.ini /etc/php/7.1/mods-available/strus.ini
RUN phpenmod strus

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./test.html /usr/share/nginx/html/index.html
COPY ./test.php /usr/share/nginx/html/test.php
COPY ./phpinfo.php /usr/share/nginx/html/phpinfo.php
COPY ./strusloaded.php /usr/share/nginx/html/strusloaded.php
COPY ./entrypoint.sh /srv/entrypoint.sh

RUN useradd strus

RUN mkdir /srv/strus
RUN chown strus:strus /srv/strus
RUN mkdir /etc/strus

RUN chown www-data:www-data /usr/share/nginx/html/*

RUN mkdir /home/strus
RUN chown strus:strus home/strus

# Strus server:
# -------------
USER strus
COPY ./strus_storage.conf /etc/strus/storage.conf
ENTRYPOINT ["/srv/entrypoint.sh"]
CMD ["strusRpcServer", "-c", "-S", "/etc/strus/storage.conf"]

# Permissions for start in shell:
# -------------------------------
WORKDIR /home/strus
USER root

# Mapped ports:
# -------------
EXPOSE 80


