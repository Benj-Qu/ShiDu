#!/usr/bin/env python3
"""Map 3."""
import sys


for line in sys.stdin:
    line = line[:-1]
    elements = line.split(" ")
    res_string = f"{int(elements[0])%3}\t{elements[2]}"
    res_string += f" {elements[3]} {elements[0]}"
    res_string += f" {elements[4]} {elements[1]}"
    print(res_string)
