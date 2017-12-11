#!/bin/bash
set -e

# -- start required services:
service php7.1-fpm start
service nginx start

echo "$@"
exec "$@"


