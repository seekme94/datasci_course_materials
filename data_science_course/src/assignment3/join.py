# This script accepts a data file containing data tables in CSV format and performs an SQL join using MapReduce
import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    table = record[1]
    mr.emit_intermediate(table, record)

def reducer(key, list_of_values):
    order = list_of_values[0]
    for i in range(1,len(list_of_values)):
        mr.emit((order + list_of_values[i]))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
