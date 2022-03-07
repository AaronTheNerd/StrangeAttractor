"""Contains a method for placing multiple data points to effectively blur the image.

Written by Aaron Barge
Copyright 2022
"""


import numpy

from typing import Dict, List


def particle_blur(CONFIGS, x: float, y: float) -> Dict[str, List[float]]:
    """Generates multiple data points to effectively blur particles."""
    d = {'x': [], 'y': [], 'weight': []}
    for i_x in range(-CONFIGS.PARTICLE_BLUR_CONFIGS["X_RADIUS"], CONFIGS.PARTICLE_BLUR_CONFIGS["X_RADIUS"] + 1):
        for i_y in range(-CONFIGS.PARTICLE_BLUR_CONFIGS["Y_RADIUS"], CONFIGS.PARTICLE_BLUR_CONFIGS["Y_RADIUS"] + 1):
            d['x'].append(x + i_x * CONFIGS.PARTICLE_BLUR_CONFIGS["DISTANCE"])
            d['y'].append(y + i_y * CONFIGS.PARTICLE_BLUR_CONFIGS["DISTANCE"])
            if i_x == 0 and i_y == 0:
                d['weight'].append(1.0)
            else:
                dropoff = i_x ** 2 + i_y ** 2
                if CONFIGS.PARTICLE_BLUR_CONFIGS["WEIGHT_FORMULA"] == "dist":
                    dropoff = numpy.sqrt(dropoff)
                d['weight'].append(
                    1.0 / (CONFIGS.PARTICLE_BLUR_CONFIGS["SCALE"] * dropoff)
                )
    return d
