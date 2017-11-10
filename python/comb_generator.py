#!/usr/bin/python3

import itertools


def main():
    flags = ["-march=native", "-fomit-frame-pointer", "-floop-block", "-floop-interchange",
            "-floop-strip-mine", "-funroll-loops", "-flto"]

    print("Generating combination of following flags:")
    print(" ".join(flags))

    with open("flags_combination", "w") as f:
        for c in range(1, len(flags) + 1):
            for c_flag in list(itertools.combinations(flags, c)):
                f.write(' '.join(c_flag) + "\n")

if __name__ == "__main__":
    main()
