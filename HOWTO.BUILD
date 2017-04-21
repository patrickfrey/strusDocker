If you want to build your own versions of the docker images, build them
in the following order:

First replace the 'FROM' and the 'MAINTAINER' lines in all docker files
with:

find . -name Dockerfile -exec sed -i 's/^FROM patrickfrey/FROM <your name>/g' {} \;
find . -name Dockerfile -exec sed -i 's/^MAINTAINER patrickpfrey@yahoo.com/MAINTAINER <your email>/g' {} \;

Remember to substitute back if you want to generate a pull-request!

For the Codeproject tutorial
"Building a search engine with Python, Tornado and Strus" do:

docker build -t <yourname>/strus-ub1404-env strus-ub1404-env
docker build -t <yourname>/strus-ub1404 strus-ub1404.latest
docker build -t <yourname>/strus-ub1404-bind strus-ub1404-bind.latest
docker build -t <yourname>/strus-ub1404-torntuto strus-ub1404-torntuto.latest

TODO FROM HER
