# Written by Aaron Barge
# Copyright 2022


import random

import numpy

from configs import POINTS_CONFIGS


def generate_points():
    points = []
    for _ in range(POINTS_CONFIGS["NUM_OF_POINTS"]):
        r = POINTS_CONFIGS["RADIUS"] * numpy.cbrt(random.random())
        x1 = random.normalvariate(0.0, 1.0)
        x2 = random.normalvariate(0.0, 1.0)
        x3 = random.normalvariate(0.0, 1.0)
        mag = numpy.sqrt(x1 ** 2 + x2 ** 2 + x3 ** 2)
        points += [(
            POINTS_CONFIGS["INIT_COORDS"]["X0"] + x1 * r / mag,
            POINTS_CONFIGS["INIT_COORDS"]["Y0"] + x2 * r / mag,
            POINTS_CONFIGS["INIT_COORDS"]["Z0"] + x3 * r / mag
        )]
    return points

if __name__ == "__main__":
    print(generate_points())
