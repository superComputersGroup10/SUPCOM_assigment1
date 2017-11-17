#!/bin/bash

# Set this varible to supermuc to run it in the supermuc, otherwise it will run without calling modules or
# llrun
MODE="jsupermuc"

COMPILER="g++" # Two possible values, g++ or icc
NUM_TASKS=1
SUPERMUC_PHASE=1

PYTHON_GEN_SCRIPT="comb_generator.py"
PYTHON_GEN_MAKE="Makefiles_generator.py"
PYTHON_PARSER="ParselElapsedAndGrindTime.py"
FLAGS_FILE="flags_combination"

SCRIPT_DIRECTORY="$(pwd) "
CODE_DIRECTORY="$(dirname $(pwd))"
MAKE_FILE="$CODE_DIRECTORY/MakefileBenchmark"
BINARY="$CODE_DIRECTORY/lulesh2.0"
OUTPUT_DIRECTORY="$CODE_DIRECTORY/4_2_compile_flags/phase$SUPERMUC_PHASE/$COMPILER"
OUTPUT_FILES_SUFIX="output_"
OUTPUT_CVS_FILENAME="test.csv"

echo "Starting..."
echo "Results will be saved in $OUTPUT_DIRECTORY directory"

if [ "$COMPILER" = "g++" ]; then
    if [ "$MODE" = "supermuc" ]; then
        module unload gcc
        module load gcc/6
    fi
elif [ "$COMPILER" != "icc" ]; then
    (>&2 echo "ERROR: Unknown compiler. Supported compilers: g++, icc")
    exit
fi

if ["$MODE" = "supermuc"]; then
    module load lrztools
fi

python $PYTHON_GEN_SCRIPT -c $COMPILER -o $FLAGS_FILE
NUM_COMBINATIONS=$(wc -l < $FLAGS_FILE)
mkdir -p -v $OUTPUT_DIRECTORY

make --directory=$CODE_DIRECTORY clean

# Since the first line of the comb_flags is a blank line, we have to loop over $NUM_COMBINATIONS + 1
for (( c=0; c<$NUM_COMBINATIONS; c++  ))
do
    echo ""
    echo "*****************************************************"
    echo "Running case $c...."
    python $PYTHON_GEN_MAKE -i $FLAGS_FILE -r $c -c $COMPILER -o $MAKE_FILE
    make --directory=$CODE_DIRECTORY --file=$MAKE_FILE

    if [ "$MODE" = "supermuc" ]; then
        llrun -n $NUM_TASKS $BINARY > $OUTPUT_DIRECTORY/$OUTPUT_FILES_SUFIX$c
    else
        $BINARY > $OUTPUT_DIRECTORY/$OUTPUT_FILES_SUFIX$c
    fi

    make --directory=$CODE_DIRECTORY --file=$MAKE_FILE clean
done

python $PYTHON_PARSER -r $OUTPUT_FILES_SUFIX -d $OUTPUT_DIRECTORY -f $FLAGS_FILE -o $OUTPUT_DIRECTORY/$OUTPUT_CVS_FILENAME -b $OUTPUT_FILES_SUFIX0
#cp $SCRIPT_DIRECTORY/$FLAGS_FILE $OUTPUT_DIRECTORY
