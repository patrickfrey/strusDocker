#!/bin/bash
set -e

# -- start required services:
service php5-fpm start
service postgresql start
service strusRpcServer start

echo "$@"
exec "$@"


