#!/bin/bash
set -e

# -- start required services:
service php5-fpm start
service nginx start

echo "$@"
exec "$@"


