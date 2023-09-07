#!/usr/bin/env python3
"""Reduce 3."""
import sys
import itertools


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def reduce_one_group(group):
    """Reduce one group."""
    results = {}
    for line in group:
        elements = line.partition("\t")[2].split(" ")
        term = elements[0]
        if term not in results:
            results[term] = {"term": term, "idf": elements[1]}
            results[term]["doc_id"] = []
            results[term]["doc_info"] = {}
        results[term]["doc_id"].append(str(elements[2]))
        doc_info_list = [elements[3], elements[4][:-1]]
        results[term]["doc_info"][elements[2]] = doc_info_list
    for term in sorted(results):
        result = results[term]["term"] + " " + results[term]["idf"]
        for doc_id in sorted(results[term]["doc_id"]):
            result += " " + doc_id + " " + results[term]["doc_info"][doc_id][0]
            result += " " + results[term]["doc_info"][doc_id][1]
        print(result)


if __name__ == "__main__":
    main()
