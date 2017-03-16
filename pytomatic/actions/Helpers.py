from matplotlib import pyplot
from time import sleep
import sys


def show_matrix(matrix):
    pyplot.imshow(matrix,cmap='hot')
    pyplot.show()

def waiting_bar(time, steps = 20):
    print("Waiting {}".format(time))
    for step in range(steps+1):
        sys.stdout.write("[{}{}]".format("#"*step,'.'*(steps - step)))
        sys.stdout.flush()
        sleep(time/steps)
        sys.stdout.write('\r')
    print("")
