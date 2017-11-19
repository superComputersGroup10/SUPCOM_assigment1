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

    ElapsedTimeString = re.search(r'Elapsed time\s+=\s+\d+\.\d+', fileStr)
    GrindTimeString = re.search(r'(\s+\d+.\d+\s+overall)', fileStr)

    if(not(ElapsedTimeString) or not(GrindTimeString)):
        Elapsed_time = 'Empty or corrudted file'
        Grind_time = 'Empty or corruepted file'
    else:
        Elapsed_time=float(re.findall("\d+\.\d+", ElapsedTimeString.group(0))[0])
        Grind_time=float(re.findall("\d+\.\d+", GrindTimeString.group(0))[0])
    return Elapsed_time, Grind_time

def main():
    parser = argparse.ArgumentParser(description="Generates a .csv with the Elapsed and Grind time")
    parser.add_argument("-r", "--root_name", help="Root name from output files")
    parser.add_argument("-d", "--directory", help="Directory where the output files are")
    parser.add_argument("-f", "--flags_file", help="File with the list of flags or auto to intex from 1 to N files found")
    parser.add_argument("-b", "--baseline_data", help="File with the baseline run to compute the speed-up")
    parser.add_argument("-o", "--ouptut_cvs", help="Name of cvs output")
    args = parser.parse_args()

    root_name = args.root_name
    directory = args.directory   
    flags_file = args.flags_file
    baselineFile = args.baseline_data
    ouptut_cvs = args.ouptut_cvs

    if (flags_file == "auto"):
        onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]

        baseElapsed_time, baseGrind_time = readElapsedAndGrindTime(baselineFile)

        index=[None] * len(onlyfiles )
        Elapsed_time=[None] * len(onlyfiles)
        Grind_time=[None] * len(onlyfiles)

        Elapsed_time_speed_up=[None] * len(onlyfiles)
        Grind_time_speed_up=[None] * len(onlyfiles)

        for i in range(0, len(onlyfiles)):
            index[i]=i+1
            file_name = directory + '/' + root_name + str(i+1)
            print(file_name)
            if os.path.isfile(file_name):
                Elapsed_time[i], Grind_time[i] = readElapsedAndGrindTime(file_name)
                if (isinstance(Elapsed_time[i], float) and isinstance(Grind_time[i], float)):
                    Elapsed_time_speed_up [i] = baseElapsed_time / Elapsed_time[i]
                    Grind_time_speed_up [i] = baseGrind_time / Grind_time[i]
            else:
                Elapsed_time[i]='The file was not found'
                Grind_time[i]='The file was not found'

        import csv
        with open(ouptut_cvs, 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(index)
            spamwriter.writerow(onlyfiles)
            spamwriter.writerow(Elapsed_time)
            spamwriter.writerow(Grind_time)
            spamwriter.writerow(Elapsed_time_speed_up)
            spamwriter.writerow(Grind_time_speed_up)

    else:
        fp=open(flags_file) 
        flags=fp.readlines()

        baseElapsed_time, baseGrind_time = readElapsedAndGrindTime(baselineFile)

        index=[None] * len(flags)
        Elapsed_time=[None] * len(flags)
        Grind_time=[None] * len(flags)

        Elapsed_time_speed_up=[None] * len(flags)
        Grind_time_speed_up=[None] * len(flags)

        for i in range(0, len(flags)):
            index[i]=i+1
            file_name = directory + '/' + root_name + str(i+1)
            if os.path.isfile(file_name):
                Elapsed_time[i], Grind_time[i] = readElapsedAndGrindTime(file_name)
                if (isinstance(Elapsed_time[i], float) and isinstance(Grind_time[i], float)):
                    Elapsed_time_speed_up [i] = baseElapsed_time / Elapsed_time[i]
                    Grind_time_speed_up [i] = baseGrind_time / Grind_time[i]
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
            spamwriter.writerow(Elapsed_time_speed_up)
            spamwriter.writerow(Grind_time_speed_up)

if __name__ == "__main__":
        main()
