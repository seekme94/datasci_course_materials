# This script accepts a data file in json form containing file names and text in it and builds an inverted index in key-value pairs using MapReduce
import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
        mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # Extract unique documents
    unique_list = []
    for doc in list_of_values:
        if doc in unique_list:
            continue
        unique_list.append(doc)
    mr.emit((key, unique_list))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
