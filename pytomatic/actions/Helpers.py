import logging

from matplotlib import pyplot
from time import sleep
import sys


def show_matrix(matrix):
    pyplot.imshow(matrix, cmap='hot')
    pyplot.show()


def waiting_bar(time, steps=20):
    print("Waiting {}".format(time))
    for step in range(steps + 1):
        sys.stdout.write("[{}{}]".format("#" * step, '.' * (steps - step)))
        sys.stdout.flush()
        sleep(time / steps)
        sys.stdout.write('\r')
    print("")


def to_pixel(coords, bbox) -> tuple:
    """
    Args:
        coords (tuple): a pair of floating point numbers between 0.0 and 1.0
            representing a percentage of the screen in the x/y directions
        bbox (tuple):
    Returns:
        touple: a pair of integers representing the actual coordinates in
            the form of pixels
    """

    if len(coords) != 2:
        raise ValueError("To Pixel takes only pairs")

    if len(bbox) == 4:
        size_vertical = bbox[2] - bbox[0]
        size_horizontal = bbox[3] - bbox[1]
    else:
        size_vertical = bbox[0]
        size_horizontal = bbox[1]

    x, y = coords[0] * size_vertical, coords[1] * size_horizontal

    logging.debug("To Pixel: {} -> {} in the box {}".format(coords, (x, y), bbox))

    return int(x), int(y)
