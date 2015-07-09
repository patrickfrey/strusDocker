FROM patrickfrey/strus-ub1404-bind
MAINTAINER patrickpfrey@yahoo.com

RUN apt-get update \
 && apt-get -y --force-yes install nginx php5-fpm
RUN rm -v /etc/nginx/nginx.conf

RUN echo "# Extension module for strus:\nextension=strus.so" >> /etc/php5/fpm/php.ini
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./test.html /usr/share/nginx/html/index.html
COPY ./test.php /usr/share/nginx/html/test.php
COPY ./entrypoint.sh /srv/entrypoint.sh

RUN chown www-data:www-data /usr/share/nginx/html/*

ENTRYPOINT ["/srv/entrypoint.sh"]
CMD ["strusRpcServer", "-s", "path=/srv/storage"]

EXPOSE 80


