#!/usr/bin/python3

import itertools
import argparse

def gen_combinations(flags, output_file):
    with open(output_file, "w") as f:
        for c in range(1, len(flags) + 1):
            for c_flag in list(itertools.combinations(flags, c)):
                f.write(' '.join(c_flag) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Generates combination of compiling flags")
    parser.add_argument("-o", "--output",
            help="Output file",
            default="flags_combination")
    parser.add_argument("-c", "--compiler",
            help="Compiler to use",
            default="gcc")
    args = parser.parse_args()

    if args.compiler == "gcc":
        flags = ["-march=native", "-fomit-frame-pointer", "-floop-block", "-floop-interchange",
                "-floop-strip-mine", "-funroll-loops", "-flto"]
    else:
        flags = ["-march=native", "-xHost", "-unroll", "-ipo"]

    print("Generating combination of following flags:")
    print(" ".join(flags))

    gen_combinations(flags, args.output)


if __name__ == "__main__":
    main()
