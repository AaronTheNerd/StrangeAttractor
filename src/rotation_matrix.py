"""Contains some methods for generating a rotation matrix for the points of the Strange Attractor simulation.

Written by Aaron Barge
Copyright 2022
"""


import numpy


def degrees_to_radians(deg: float) -> float:
    """Converts an angle in degrees to radians."""
    return deg / 180 * numpy.pi


def generate_rotation_matrix(alpha: float, beta: float, gamma: float) -> numpy.array:
    """Creates a rotation matrix."""
    return numpy.array((
        (
            numpy.cos(beta) * numpy.cos(gamma),
            numpy.sin(alpha) * numpy.sin(beta) * numpy.cos(gamma) - numpy.cos(alpha) * numpy.sin(gamma),
            numpy.cos(alpha) * numpy.sin(beta) * numpy.cos(gamma) + numpy.sin(alpha) * numpy.sin(gamma)
        ),
        (
            numpy.cos(beta) * numpy.sin(gamma),
            numpy.sin(alpha) * numpy.sin(beta) * numpy.sin(gamma) + numpy.cos(alpha) * numpy.cos(gamma),
            numpy.cos(alpha) * numpy.sin(beta) * numpy.sin(gamma) - numpy.sin(alpha) * numpy.cos(gamma)
        ),
        (
            -numpy.sin(beta),
            numpy.sin(alpha) * numpy.cos(beta),
            numpy.cos(alpha) * numpy.cos(beta)
        )
    ))
