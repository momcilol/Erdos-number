#!/bin/bash

echo "pair of quotes"
while grep -q '>.*\".*\".*<' dblp.xml; do
	sed -i 's/\(>.*\)\"\(.*\)\"\(.*<\)/\1\&quot;\2\&quot;\3/g' dblp.xml
done

echo "replaced"
grep -n '>.*\".*\".*<' dblp.xml
echo ""
echo "quot"

while grep -q '>.*\".*<' dblp.xml; do
	sed -i 's/\(>.*\)\"\(.*<\)/\1\&quot;\2/g' dblp.xml
done

echo "replaced"
grep -n '>.*\".*<' dblp.xml
echo ""
echo "apos"

while grep -q ">.*'.*<" dblp.xml; do
	sed -i "s/\(>.*\)'\(.*<\)/\1\&apos;\2/g" dblp.xml
done

grep -n ">.*'.*<" dblp.xml
echo "replaced"
echo ""
echo ""

