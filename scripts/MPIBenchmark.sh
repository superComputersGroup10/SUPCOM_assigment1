#!/bin/bash

# Set this varible to supermuc to run it in the supermuc, otherwise it will run without calling modules or
# llrun
#MODE="supermuc"
MODE = "AnibalSuperFunComputer"

COMPILER="mpiCC" # Two possible values, g++ or icc
MAX_TWO_POWER_PROCESS=3
SUPERMUC_PHASE=1

PYTHON_GEN_BATCH="MPIBatchScripGenerator.py"

SCRIPT_DIRECTORY="$(pwd) "
CODE_DIRECTORY="$(dirname $(pwd))"
MAKE_FILE="$CODE_DIRECTORY/MPIMakefile"
BATCH_FILE="$CODE_DIRECTORY/MPIRunBatch"
BINARY="$CODE_DIRECTORY/lulesh2.0"
OUTPUT_DIRECTORY="$CODE_DIRECTORY/5_2_MPI/phase$SUPERMUC_PHASE/$COMPILER"
OUTPUT_FILES_SUFIX="output_"

echo "Starting..."
echo "Results will be saved in $OUTPUT_DIRECTORY directory"


if ["$MODE" = "supermuc"]; then
    module load lrztools
    module unload mpi.ibm
    module load mpi.intel
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
    python $PYTHON_GEN_BATCH -n $c -o $BATCH_FILE -l $OUTPUT_DIRECTORY/$OUTPUT_FILES_SUFIX$c 

    if [ "$MODE" = "supermuc" ]; then
        llsubmit $BATCH_FILE
    else
        export OMP_NUM_THREADS=c
        $BINARY > $OUTPUT_DIRECTORY/$OUTPUT_FILES_SUFIX$c
    fi
done
