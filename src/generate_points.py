"""Contains a method to generate points uniformly within a sphere.

Written by Aaron Barge
Copyright 2022
"""


import random

import numpy


def generate_points(CONFIGS):
    """Generates random points uniformly within a sphere."""
    points = []
    for _ in range(CONFIGS.POINTS_CONFIGS["NUM_OF_POINTS"]):
        r = CONFIGS.POINTS_CONFIGS["RADIUS"] * numpy.cbrt(random.random())
        x1 = random.normalvariate(0.0, 1.0)
        x2 = random.normalvariate(0.0, 1.0)
        x3 = random.normalvariate(0.0, 1.0)
        mag = numpy.sqrt(x1 ** 2 + x2 ** 2 + x3 ** 2)
        points += [(
            CONFIGS.POINTS_CONFIGS["INIT_COORDS"]["X0"] + x1 * r / mag,
            CONFIGS.POINTS_CONFIGS["INIT_COORDS"]["Y0"] + x2 * r / mag,
            CONFIGS.POINTS_CONFIGS["INIT_COORDS"]["Z0"] + x3 * r / mag
        )]
    return points

if __name__ == "__main__":
    from src.configs import CONFIGS
    print(generate_points(CONFIGS))
