# This script accepts a data file in json form containing pairs of friends in a social network and outputs count of friends for each person using MapReduce
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
    count = 1
    mr.emit_intermediate(p1, count)

def reducer(key, list_of_values):
    total = 0
    for count in list_of_values:
        total = total + count
    mr.emit((key, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
