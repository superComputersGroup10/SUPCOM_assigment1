#!/bin/sh

PYTHON_GEN_SCRIPT="comb_generator.py"
PYTHON_GEN_MAKE="Makefiles_generator.py"
COMPILER="gcc"
FLAGS_FILE="flags_combination"
SUPERMUC_PHASE=1
SCRIPT_DIRECTORY="$(pwd) "
CODE_DIRECTORY="$(dirname $(pwd))"
OUTPUT_DIRECTORY="$CODE_DIRECTORY/4_2_compile_flags/phase$SUPERMUC_PHASE/$COMPILER"


if [ "$COMPILER" = "gcc" ]; then
    NUM_COMBINATIONS=127
elif [ "$COMPILER" = "icc" ]; then
    NUM_COMBINATIONS=15
else
    (>&2 echo "ERROR: Unknown compiler")
    exit
fi

echo "Starting..."

python $PYTHON_GEN_SCRIPT -c $COMPILER -o $FLAGS_FILE
mkdir -p -v $OUTPUT_DIRECTORY

#for i in {1..127};
#do
#make -f Makefile$i
#mv lulesh2.0_$i Binaries/
#make -f Makefile$i clean
