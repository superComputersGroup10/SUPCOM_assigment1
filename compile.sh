#!/bin/sh

echo "compiling the files"

for i in {1..127};
do
make -f Makefile$i 
mv lulesh2.0_$i Binaries/
make -f Makefile$i clean
done
