#!/bin/bash

unzip dblp.xml.zip dblp.xml

echo "Unzipped"
echo "Ccedil"

grep -n '\\"' dblp.xml
sed -i 's/\\"{C}/\&Ccedil;/' dblp.xml

echo "replaced"
echo ""
echo "i umlaut"

grep -n '\\"' dblp.xml
sed -i 's/\\"&#305;/\&iuml;/g' dblp.xml

echo "replaced"
echo ""
echo "o umlaut"

grep -n '\\"' dblp.xml
sed -i 's/\\"o/\&ouml;/g' dblp.xml

echo "replaced"
echo ""
echo "o umlaut"

grep -n '\\"' dblp.xml
sed -i 's/{\\"}o/\&ouml;/g' dblp.xml

echo "replaced"
echo ""
echo "u umlaut"

grep -n '\\"' dblp.xml
sed -i 's/{\\" u}/\&uuml;/g' dblp.xml

echo "replaced"
echo ""
echo "o umlaut"

grep -n '\\"' dblp.xml
sed -i 's/\\"{o}/\&ouml;/g' dblp.xml

echo "replaced"
echo ""
echo "a umlaut"

grep -n '\\"' dblp.xml
sed -i 's/\\"a/\&auml;/g' dblp.xml

echo "replaced"
echo ""
echo "escaped quot"

grep -n '\\"' dblp.xml
sed -i 's/\(>.*\)\\"\(.*\)\\"\(.*<\)/\1\&quot;\2\&quot;\3/g' dblp.xml

echo "replaced"
echo ""

# echo "pair of quotes"
# while grep -q '>[^<>\n]*\"[^<>\n]*\"[^<>\n]*<' dblp.xml; do
# 	sed -E -i 's/(>[^<>\n]*)\"([^<>\n]*)\"([^<>\n]*<)/\1\&quot;\2\&quot;\3</g' dblp.xml
# done

# echo "replaced"
# grep -n '>.*\".*\".*<' dblp.xml
# echo ""
# echo "quot"

# while grep -q '>[^<>\n]*\"[^<>\n]*<' dblp.xml; do
# 	sed -E -i 's/(>[^<>\n]*)\"\([^<>\n]*<)/\1\&quot;\2/g' dblp.xml
# done

# echo "replaced"
# grep -n '>.*\".*<' dblp.xml
# echo ""
# echo "apos"

# while grep -q ">[^<>\n]*'[^<>\n]*<" dblp.xml; do
# 	sed -E -i "s/(>[^<>\n]*)'([^<>\n]*<)/\1\&apos;\2/g" dblp.xml
# done

# grep -n ">.*'.*<" dblp.xml
# echo "replaced"
# echo ""
# echo ""

