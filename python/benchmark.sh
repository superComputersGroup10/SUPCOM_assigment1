#!/bin/bash

PYTHON_GEN_SCRIPT="comb_generator.py"
PYTHON_GEN_MAKE="Makefiles_generator.py"
COMPILER="g++"
FLAGS_FILE="flags_combination"
SUPERMUC_PHASE=1

SCRIPT_DIRECTORY="$(pwd) "
CODE_DIRECTORY="$(dirname $(pwd))"
MAKE_FILE="$CODE_DIRECTORY/MakefileBenchmark"
BINARY="$CODE_DIRECTORY/lulesh2.0"
OUTPUT_DIRECTORY="$CODE_DIRECTORY/4_2_compile_flags/phase$SUPERMUC_PHASE/$COMPILER/"
OUTPUT_FILES_SUFIX="output_"

if [ "$COMPILER" = "g++" ]; then
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

make --directory=$CODE_DIRECTORY clean
#for (( c=0; c<$NUM_COMBINATIONS; c++  ))
for (( c=0; c<1; c++  ))
do
    python $PYTHON_GEN_MAKE -i $FLAGS_FILE -r $c -c $COMPILER -o $MAKE_FILE
    make --directory=$CODE_DIRECTORY --file=$MAKE_FILE
    $BINARY > $OUTPUT_DIRECTORY$OUTPUT_FILES_SUFIX$((c+1))
    make --directory=$CODE_DIRECTORY --file=$MAKE_FILE clean
done
