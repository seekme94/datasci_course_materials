# This script calculates terms in tweet stream file (# of occurrences of the term in all tweets]/[# of occurrences of all terms in all tweets)

from random import randrange

def generate_data():
#    out_file = open(sys.argv[1])
    out_file = "regimen.txt"
    regimens = ['HE','EH','RHE','HRE','RHZE','HRZE','HERZ','RHZES','HRZES','HERZS']
    x = 0
    while x < 206300000:
        buffered = []
        n = randrange(10000)
        for i in range (0,n):
            buffered.append(regimens[randrange(len(regimens))])
        with open(out_file, mode='a') as my_file:
            my_file.write(str(buffered).replace("'", "") + "\n")
            buffered = []
        x = x + n
        print (x)

if __name__ == '__main__':
    generate_data()
