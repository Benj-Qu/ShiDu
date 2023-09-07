#!/usr/bin/env python3
"""Map 0."""
import sys
import csv


csv.field_size_limit(sys.maxsize)
documents = set()
for line in csv.reader(sys.stdin):
    if line[0] not in documents:
        documents.add(line[0])
        print("document\t1")
