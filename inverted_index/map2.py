#!/usr/bin/env python3
"""Map 2."""
import sys


for line in sys.stdin:
    line = line[:-1]
    elements = line.split(" ")
    # {key} {idf} {doc_id} {docs[doc_id]}
    print(f"{elements[2]}\t{elements[0]} {elements[1]} {elements[3]}")
