# This script accepts a data file in json form containing pairs of friends in a social network and outputs asymmetric friendship pairs using MapReduce
import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    p1 = record[0]
    p2 = record[1]
    if p1 > p2:
        mr.emit_intermediate(p2, p1)
    else:
        mr.emit_intermediate(p1, p2)
def reducer(key, list_of_values):
    new_pairs = []
    for value in list_of_values:
        new_pairs.append((key, value))
    for value in new_pairs:
        if new_pairs.count(value) == 1:
            k, v = value
            mr.emit((k, v))
            mr.emit((v, k))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
