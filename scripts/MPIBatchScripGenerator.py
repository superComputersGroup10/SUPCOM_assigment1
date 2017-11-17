import argparse

def writeBashFile(numProcesses, output, luleshOutput):
        bashString="""#!/bin/bash
#@ wall_clock_limit = 00:20:00
#@ job_name = pos-lulesh-openmp
#@ job_type = MPICH
# #####################################
#@ class = test
# ######################################@ output = pos_lulesh_openmp_$(jobid).out
#@ error = pos_lulesh_openmp_$(jobid).out
#@ node = 1
#@ total_tasks = %i
#@ node_usage = not_shared
#@ energy_policy_tag = lulesh
#@ minimize_time_to_solution = yes
#@ island_count = 1
#@ queue
. /etc/profile
. /etc/profile.d/modules.sh
$HOME/.bashrc

# load the correct MPI library
module unload mpi.ibm
module load mpi.intel

exec -n %i ./lulesh2.0> %s""" % (16, numProcesses, luleshOutput)
        f = open(output, 'w')
        f.write(bashString)
        f.closed
 
def main():
    parser = argparse.ArgumentParser(description="Generates a Batchspript for a jon with n threads")
    parser.add_argument("-c", "--cubeRoot", help="The root for the number of processes so if you chose n the number of processes with be n*n*n")
    parser.add_argument("-o", "--output", help="Output name for the Makefile")
    parser.add_argument("-l", "--luleshOutput", help="Output name for the Makefile")
    args = parser.parse_args()

    cubeRoot = int(args.cubeRoot )
    output = args.output 
    luleshOutput = args.luleshOutput

    writeBashFile(cubeRoot*cubeRoot*cubeRoot, output, luleshOutput)

if __name__ == "__main__":
        main()
