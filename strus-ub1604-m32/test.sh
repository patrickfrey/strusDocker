#!/bin/sh

cd strus-master/ && make test && cd ..
cd strusAnalyzer-master/ && make test && cd ..
cd strusModule-master/ && make test && cd ..
cd strusPattern-master/ && make test && cd ..
cd strusVector-master/ && make test && cd ..
cd strusUtilities-master/ && make test && cd ..
cd strusBindings-master/ && make test && cd ..

