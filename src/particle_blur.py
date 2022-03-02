# Written by Aaron Barge
# Copyright 2022


import numpy
import pandas

from configs import PARTICLE_BLUR_CONFIGS


def particle_blur(x, y):
    d = {'x': [], 'y': [], 'weight': []}
    for i_x in range(-PARTICLE_BLUR_CONFIGS["X_RADIUS"], PARTICLE_BLUR_CONFIGS["X_RADIUS"] + 1):
        for i_y in range(-PARTICLE_BLUR_CONFIGS["Y_RADIUS"], PARTICLE_BLUR_CONFIGS["Y_RADIUS"] + 1):
            d['x'].append(x + i_x * PARTICLE_BLUR_CONFIGS["DISTANCE"])
            d['y'].append(y + i_y * PARTICLE_BLUR_CONFIGS["DISTANCE"])
            if i_x == 0 and i_y == 0:
                d['weight'].append(1.0)
            else:
                dropoff = i_x ** 2 + i_y ** 2
                if PARTICLE_BLUR_CONFIGS["WEIGHT_FORMULA"] == "dist":
                    dropoff = numpy.sqrt(dropoff)
                d['weight'].append(
                    1.0 / (PARTICLE_BLUR_CONFIGS["SCALE"] * dropoff)
                )
    return d
