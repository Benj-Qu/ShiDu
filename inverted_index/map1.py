#!/usr/bin/env python3
"""Map 1."""
import sys
import csv
import re


stopwords = set()
with open("stopwords.txt", "r", encoding="utf-8") as f:
    for stopword_line in f.readlines():
        stopwords.add(stopword_line[:-1])

with open("total_document_count.txt", "r", encoding="utf-8") as f:
    for line in f.readlines():
        document_count = int(line)

csv.field_size_limit(sys.maxsize)
for line in csv.reader(sys.stdin):
    doc_id = line[0]
    text = line[1] + " " + line[2]
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
    text = text.casefold()
    terms = text.split()
    preprocessed_terms = []
    for term in terms:
        if term not in stopwords:
            preprocessed_terms.append(term)
    for term in set(preprocessed_terms):
        # term \t document_id term_frequency document_count
        res_string = f"{term}\t{doc_id}"
        res_string += f" {preprocessed_terms.count(term)}"
        res_string += f" {document_count}"
        print(res_string)
