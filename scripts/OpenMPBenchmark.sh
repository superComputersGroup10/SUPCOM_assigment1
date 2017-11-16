#!/bin/bash

# Set this varible to supermuc to run it in the supermuc, otherwise it will run without calling modules or
# llrun
#MODE="supermuc"
MODE = "AnibalSuperFunComputer"

COMPILER="g++" # Two possible values, g++ or icc
MAX_NUM_TASKS=4
SUPERMUC_PHASE=1

PYTHON_GEN_BATCH="BatchScripGenerator.py"
PYTHON_PARSER="ParselElapsedAndGrindTime.py"
FLAGS_FILE="flags_combination"

SCRIPT_DIRECTORY="$(pwd) "
CODE_DIRECTORY="$(dirname $(pwd))"
MAKE_FILE="$CODE_DIRECTORY/OpenMPMakefile"
BATCH_FILE="$CODE_DIRECTORY/OPENMPRunBatch"
BINARY="$CODE_DIRECTORY/lulesh2.0"
OUTPUT_DIRECTORY="$CODE_DIRECTORY/5_1_OpenMP/phase$SUPERMUC_PHASE/$COMPILER"
OUTPUT_FILES_SUFIX="output_"
OUTPUT_CVS_FILENAME="benchmark_output.csv"

echo "Starting..."
echo "Results will be saved in $OUTPUT_DIRECTORY directory"

if [ "$COMPILER" = "g++" ]; then
    NUM_COMBINATIONS=127
    if [ "$MODE" = "supermuc" ]; then
        module unload gcc
        module load gcc/6
    fi
elif [ "$COMPILER" = "icc" ]; then
    NUM_COMBINATIONS=15
else
    (>&2 echo "ERROR: Unknown compiler")
    exit
fi

if ["$MODE" = "supermuc"]; then
    module load lrztools
fi

mkdir -p -v $OUTPUT_DIRECTORY

make --directory=$CODE_DIRECTORY clean
make --directory=$CODE_DIRECTORY --file=$MAKE_FILE

# Since the first line of the comb_flags is a blank line, we have to loop over $NUM_COMBINATIONS + 1
for (( c=1; c<=$MAX_NUM_TASKS; c++  ))
do
    echo ""
    echo "*****************************************************"
    echo "Running with $c threads."
    python $PYTHON_GEN_BATCH -n $c -o $BATCH_FILE

    if [ "$MODE" = "supermuc" ]; then
        llsubmit $BATCH_FILE
    else
        export OMP_NUM_THREADS=c
        $BINARY > $OUTPUT_DIRECTORY/$OUTPUT_FILES_SUFIX$c
    fi
done

#python $PYTHON_PARSER -r $OUTPUT_FILES_SUFIX -d $OUTPUT_DIRECTORY -f $FLAGS_FILE -o $OUTPUT_DIRECTORY/$OUTPUT_CVS_FILENAME -b $OUTPUT_FILES_SUFIX0
#cp $SCRIPT_DIRECTORY/$FLAGS_FILE $OUTPUT_DIRECTORY
