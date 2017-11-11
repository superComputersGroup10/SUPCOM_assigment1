#!/bin/sh

PYTHON_GEN_SCRIPT="comb_generator.py"
PYTHON_GEN_MAKE="Makefiles_generator.py"
COMPILER="gcc"
FLAGS_FILE="flags_combination"

if [ "$COMPILER" = "gcc" ]; then
    NUM_COMBINATIONS=127
elif [ "$COMPILER" = "icc" ]; then
    NUM_COMBINATIONS=15
else
    (>&2 echo "ERROR: Unknown compiler")
    exit
fi

echo "Starting..."
echo "$NUM_COMBINATIONS"

python $PYTHON_GEN_SCRIPT -c $COMPILER -o $FLAGS_FILE

#for i in {1..127};
#do
#make -f Makefile$i
#mv lulesh2.0_$i Binaries/
#make -f Makefile$i clean
