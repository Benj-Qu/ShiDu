#!/usr/bin/env python3
"""Reduce 1."""
import sys
import itertools
import math


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def reduce_one_group(key, group):
    """Reduce one group."""
    nk_count = 0
    docs = {}
    for line in group:
        doc_id = line.partition("\t")[2].split(" ")[0]
        term_frequency = line.partition("\t")[2].split(" ")[1]
        docs[doc_id] = term_frequency
        nk_count += 1
        document_count = int(line.partition("\t")[2].split(" ")[2])
    idf = math.log(document_count/nk_count, 10)
    for doc_id, doc in docs.items():
        print(f"{key} {idf} {doc_id} {doc}")


if __name__ == "__main__":
    main()
