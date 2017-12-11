#!/bin/sh

mkdir data
cd data
# [1] Fetch the musicbrainz data dump:
wget http://ftp.musicbrainz.org/pub/musicbrainz/data/fullexport/LATEST
LATEST=`cat LATEST`
wget http://ftp.musicbrainz.org/pub/musicbrainz/data/fullexport/$LATEST/mbdump-cdstubs.tar.bz2
bzip2 -d mbdump-cdstubs.tar.bz2
tar -xvf mbdump-cdstubs.tar

# [2] Generate the XML documents to insert:
cat mbdump/release_raw | sed 's/\&/\&amp;/g' | sed 's/</\&lt;/g' | sed 's/>/\&gt;/g' > dump.txt
ndocs=`cat dump.txt | awk -F"\t" '{if(min=="")min=max=$1; if($1>max) {max=$1}; if($1< min) {min=$1}; } END {print int((max+1)/10000)}'`
mkdir doc
idoc=0
while [ $idoc -le $ndocs ]
do
    echo "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?>" > doc/$idoc.xml
    echo "<list>" >> doc/$idoc.xml
    idoc=`expr $idoc + 1`
done
cat dump.txt \
  | awk -F"\t" '{FNAME=int($1/10000); print "<item><id>" $1 "</id><title>" $2 "</title><artist>" $3 "</artist><date>" $4 "</date><upc>" $9 "</upc><note>" $10 "</note></item>" >> "doc/"FNAME".xml" }'
idoc=0
while [ $idoc -le $ndocs ]
do
    echo "</list>" >> doc/$idoc.xml
    idoc=`expr $idoc + 1`
done

