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
    matrix = record[0]
    row = record[1]
    col = record[2]
    val = record[3]
    mr.emit_intermediate("", (matrix, row, col, val))

def reducer(key, list_of_values):
    rows = 5
    cols = 5
    a_matrix = [[0 for j in range(cols)] for i in range(rows)] # Declare a 5x5 matrix
    b_matrix = [[0 for j in range(cols)] for i in range(rows)]
    result = [[0 for j in range(cols)] for i in range(rows)]
    for value in list_of_values:
        m, c, r, v = value
        if m == 'a':
            a_matrix[r][c] = v
        else:
            b_matrix[r][c] = v
    # Algorithm
    # |A|x|B| = Sum(1 to m) {a(i,k) * b(k,i)}
    
    # For each cell, find products
    '''
    for i in range (0, rows):
        for j in range(0, cols):
            for k in range(0, cols):
                result[i][j] = result[i][j] + (a_matrix[i][k] * b_matrix[k][j])
    for i in range (0, rows):
        mr.emit(result[i])
    '''
    for i in range (0, rows):
        for j in range (0, rows):
            for k in range(0, cols):
                result[i][j] = result[i][j] + (b_matrix[i][k] * a_matrix[k][j])
    for i in range (0, rows):
        for j in range (0, cols):
            mr.emit((i, j, result[j][i]))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
