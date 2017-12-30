#!/bin/sh

cd /strusBase-master/; make test
cd /strus-master/; make test
cd /strusAnalyzer-master; make test
cd /strusModule-master; make test
cd /strusPattern-master; make test
cd /strusVector-master; make test
cd /strusUtilities-master; make test
cd /strusBindings-master; make test


