#!/usr/bin/env python3
"""Word count reducer."""
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
    word_count = 0
    for line in group:
        count = line.partition("\t")[2]
        word_count += int(count)
    print(f"{key} {word_count}")

# Multiple iteration
# def reduce_one_group(key, group):
#     group = list(group)  # iterable to list
#     for line in group:
#         pass  # Do something
#     for line in group:
#         pass  # Do something

if __name__ == "__main__":
    main()
