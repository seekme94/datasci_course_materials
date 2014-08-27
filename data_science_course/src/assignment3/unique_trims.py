# This script accepts a data file in json form containing DNA sequences and outputs unique sequences after clipping off last 10 characters; uses MapReduce
import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    trimmed = str(record[1]).strip()
    trimmed = trimmed[0:len(trimmed) - 10]
    mr.emit_intermediate("", trimmed)

def reducer(key, list_of_values):
    unique = set(list_of_values)
    for value in unique:
        mr.emit((value))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
