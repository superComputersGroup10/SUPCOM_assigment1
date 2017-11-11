#!/bin/bash

COMPILER="g++"
NUM_TASKS=1

PYTHON_GEN_SCRIPT="comb_generator.py"
PYTHON_GEN_MAKE="Makefiles_generator.py"
PYTHON_PARSER="ParselElapsedAndGrindTime.py"
FLAGS_FILE="flags_combination"
SUPERMUC_PHASE=1

SCRIPT_DIRECTORY="$(pwd) "
CODE_DIRECTORY="$(dirname $(pwd))"
MAKE_FILE="$CODE_DIRECTORY/MakefileBenchmark"
BINARY="$CODE_DIRECTORY/lulesh2.0"
OUTPUT_DIRECTORY="$CODE_DIRECTORY/4_2_compile_flags/phase$SUPERMUC_PHASE/$COMPILER"
OUTPUT_FILES_SUFIX="output_"
OUTPUT_CVS_FILENAME="test.cvs"

echo "Starting..."
echo "Results will be saved in $OUTPUT_DIRECTORY directory"

if [ "$COMPILER" = "g++" ]; then
    NUM_COMBINATIONS=127
    module unload gcc
    module load gcc/6
elif [ "$COMPILER" = "icc" ]; then
    NUM_COMBINATIONS=15
    module
else
    (>&2 echo "ERROR: Unknown compiler")
    exit
fi

module load lrztools

python $PYTHON_GEN_SCRIPT -c $COMPILER -o $FLAGS_FILE
mkdir -p -v $OUTPUT_DIRECTORY

make --directory=$CODE_DIRECTORY clean
for (( c=0; c<$NUM_COMBINATIONS; c++  ))
do
    echo ""
    echo "*****************************************************"
    echo "Running case $c...."
    python $PYTHON_GEN_MAKE -i $FLAGS_FILE -r $c -c $COMPILER -o $MAKE_FILE
    make --directory=$CODE_DIRECTORY --file=$MAKE_FILE
    llrun -n $NUM_TASKS $BINARY > $OUTPUT_DIRECTORY/$OUTPUT_FILES_SUFIX$((c+1))
    make --directory=$CODE_DIRECTORY --file=$MAKE_FILE clean
done

python $PYTHON_PARSER -r $OUTPUT_FILES_SUFIX -d $OUTPUT_DIRECTORY -f $FLAGS_FILE -o $OUTPUT_DIRECTORY/$OUTPUT_CVS_FILENAME
#cp $SCRIPT_DIRECTORY/$FLAGS_FILE $OUTPUT_DIRECTORY
