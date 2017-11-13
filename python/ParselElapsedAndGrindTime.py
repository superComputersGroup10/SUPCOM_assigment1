#!/urs/bin/python3

import argparse
import re
from os import listdir
from os.path import isfile, join
import os

def readElapsedAndGrindTime(file_name):
    f=open(file_name)
    fileStr=f.read().replace('(us/z/c)', '')
    f.close()

    print(fileStr)
    ElapsedTimeString = re.search(r'Elapsed time\s+=\s+\d+\.\d+', fileStr)
    GrindTimeString = re.search(r'Grind time\s+=\s+\d+.\d+', fileStr)
    print(ElapsedTimeString.group(0))

    if(not(ElapsedTimeString) or not(GrindTimeString)):
        Elapsed_time = 'Empty or corrudted file'
        Grind_time = 'Empty or corruepted file'
    else:
        Elapsed_time=float(re.findall("\d+\.\d+", ElapsedTimeString.group(0))[0])
        Grind_time=float(re.findall("\d+\.\d+", Grind_time.group(0))[0])
    return Elapsed_time, Grind_time

def main():
    parser = argparse.ArgumentParser(description="Generates a .csv with the Elapsed and Grind time")
    parser.add_argument("-r", "--root_name", help="Root name from output files")
    parser.add_argument("-d", "--directory", help="Directory where the output files are")
    parser.add_argument("-f", "--flags_file", help="File with the list of flags")
    parser.add_argument("-o", "--ouptut_cvs", help="Name of cvs output")
    args = parser.parse_args()

    root_name = args.root_name
    directory = args.directory   
    flags_file = args.flags_file
    ouptut_cvs = args.ouptut_cvs

    fp=open(flags_file) 
    flags=fp.readlines()

    index=[None] * len(flags)
    Elapsed_time=[None] * len(flags)
    Grind_time=[None] * len(flags)

    for i in range(0, len(flags)):
        index[i]=i+1
        file_name = directory + '/' + root_name + str(i+1)
        if os.path.isfile(file_name):
            Elapsed_time[i], Grind_time[i] = readElapsedAndGrindTime(file_name)
        else:
            Elapsed_time[i]='The file was not found'
            Grind_time[i]='The file was not found'

    import csv
    with open(ouptut_cvs, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(index)
        spamwriter.writerow(flags)
        spamwriter.writerow(Elapsed_time)
        spamwriter.writerow(Grind_time)

if __name__ == "__main__":
        main()
