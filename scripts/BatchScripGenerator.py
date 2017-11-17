import argparse

def writeBashFile(numThreads, output, luleshOutput):
        bashString="""#!/bin/bash
#@ wall_clock_limit = 00:20:00
#@ job_name = pos-lulesh-openmp
#@ job_type = MPICH
# #####################################
# for fat node we need class = micro
# #@ class = micro
# #####################################
# // for thin node we need class = fat
#@ class = fat
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
export OMP_NUM_THREADS=%i
./../lulesh2.0 > %s""" % (16, numThreads, luleshOutput)
        f = open(output, 'w')
        f.write(bashString)
        f.closed
 
def main():
    parser = argparse.ArgumentParser(description="Generates a Batchspript for a jon with n threads")
    parser.add_argument("-n", "--numThreads", help="Number of threads to run")
    parser.add_argument("-o", "--output", help="Output name for the Makefile")
    parser.add_argument("-l", "--luleshOutput", help="Output name for the Makefile")
    args = parser.parse_args()

    numThreads = int(args.numThreads )
    output = args.output 
    luleshOutput = args.luleshOutput

    writeBashFile(numThreads, output, luleshOutput)

if __name__ == "__main__":
        main()
