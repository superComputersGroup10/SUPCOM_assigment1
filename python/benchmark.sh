#!/bin/sh

PYTHON_GEN_SCRIPT="comb_generator.py"
PYTHON_GEN_MAKE="Makefiles_generator.py"
COMPILER="gcc"
FLAGS_FILE="flags_combination"

echo "Starting..."


chmod +x $PYTHON_GEN_SCRIPT $PYTHON_GEN_MAKE
./$PYTHON_GEN_SCRIPT -c $COMPILER -o $FLAGS_FILE

#for i in {1..127};
#do
#make -f Makefile$i 
#mv lulesh2.0_$i Binaries/
#make -f Makefile$i clean

chmod -x $PYTHON_GEN_SCRIPT $PYTHON_GEN_MAKE
