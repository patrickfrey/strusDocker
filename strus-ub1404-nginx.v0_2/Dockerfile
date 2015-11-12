FROM patrickfrey/strus-ub1404-bind:v0_2
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update \
 && apt-get -y --force-yes install nginx php5-fpm
RUN rm -v /etc/nginx/nginx.conf

RUN echo "# Extension module for strus:\nextension=strus.so" >> /etc/php5/fpm/php.ini
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./test.html /usr/share/nginx/html/index.html
COPY ./test.php /usr/share/nginx/html/test.php
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


