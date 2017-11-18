#!/urs/bin/python3

import argparse

def writeMakeFile(flags, compiler, output):
    makefilestring="""#default build suggestion of MPI + OPENMP with gcc on Livermore machines you might have to change the compiler name
    
SHELL = /bin/sh
.SUFFIXES: .cc .o

LULESH_EXEC = lulesh2.0

MPI_INC = /opt/local/include/openmpi
MPI_LIB = /opt/local/lib

SERCXX = %s -DUSE_MPI=0
MPICXX = mpig++ -DUSE_MPI=1
CXX = $(SERCXX)

SOURCES2.0 = \\
	lulesh.cc \\
	lulesh-comm.cc \\
	lulesh-viz.cc \\
	lulesh-util.cc \\
	lulesh-init.cc
OBJECTS2.0 = $(SOURCES2.0:.cc=.o)

#Default build suggestions with OpenMP for g++
CXXFLAGS = -O3 %s
LDFLAGS = -O3

#Below are reasonable default flags for a serial build
#CXXFLAGS = -g -O3 -I. -Wall 
#LDFLAGS = -g -O3 

#common places you might find silo on the Livermore machines.
#SILO_INCDIR = /opt/local/include
#SILO_LIBDIR = /opt/local/lib
#SILO_INCDIR = ./silo/4.9/1.8.10.1/include
#SILO_LIBDIR = ./silo/4.9/1.8.10.1/lib

#If you do not have silo and visit you can get them at:
#silo:  https://wci.llnl.gov/codes/silo/downloads.html
#visit: https://wci.llnl.gov/codes/visit/download.html

#below is and example of how to make with silo, hdf5 to get vizulization by default all this is turned off.  All paths are Livermore specific.
#CXXFLAGS = -g -DVIZ_MESH -I${SILO_INCDIR} -Wall -Wno-pragmas
#LDFLAGS = -g -L${SILO_LIBDIR} -Wl,-rpath -Wl,${SILO_LIBDIR} -lsiloh5 -lhdf5

.cc.o: lulesh.h
	@echo "Building $<"
	$(CXX) -c $(CXXFLAGS) -o $@  $<

all: $(LULESH_EXEC)

lulesh2.0: $(OBJECTS2.0)
	@echo "Linking"
	$(CXX) $(OBJECTS2.0) $(LDFLAGS) -lm -o $@

clean:
	/bin/rm -f *.o *~ $(OBJECTS) $(LULESH_EXEC)
	/bin/rm -rf *.dSYM

tar: clean
	cd .. ; tar cvf lulesh-2.0.tar LULESH-2.0 ; mv lulesh-2.0.tar LULESH-2.0
""" % (compiler, flags)
    f = open(output, 'w')
    f.write(makefilestring)
    f.closed
    print('Generated Makefile with flags: %s  ' % (flags.replace('\n','')))
    

def main():
    parser = argparse.ArgumentParser(description="Generates a Makefile with the flags indicated flags")
    parser.add_argument("-i", "--input_file", help="Text files with flag list as rows")
    parser.add_argument("-r", "--row", help="Row of the flag file to write in the Makefile")
    parser.add_argument("-c", "--compiler", help="Compiler name to use in the Makefile")
    parser.add_argument("-o", "--output", help="Output name for the Makefile")
    args = parser.parse_args()

    filepath = args.input_file
    row = int(args.row)
    compiler = args.compiler 
    output = args.output 

    fp=open(filepath) 
    flags=fp.readlines()
    
    writeMakeFile(flags[row], compiler, output)

if __name__ == "__main__":
        main()
