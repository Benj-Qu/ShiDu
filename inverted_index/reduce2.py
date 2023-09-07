#!/usr/bin/env python3
"""Reduce 3."""
import sys
import itertools


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def reduce_one_group(key, group):
    """Reduce one group."""
    normalization_factor = 0
    lines = []
    for line in group:
        idf = line.partition("\t")[2].split(" ")[1]
        term_frequency = line.partition("\t")[2].split(" ")[2][:-1]
        normalization_factor += (float(term_frequency) * float(idf))**2
        lines.append(line)
    for line in lines:
        # doc_id normalization_factor term idf tf
        items = line.partition("\t")[2][:-1]
        print(f"{key} {normalization_factor} {items}")


if __name__ == "__main__":
    main()
