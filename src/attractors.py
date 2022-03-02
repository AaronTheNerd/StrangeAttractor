# Written by Aaron Barge
# Copyright 2022


import math
import sys
from abc import ABC, abstractmethod

import numpy

from configs import CONFIGS


class Attractor(ABC):
    @abstractmethod
    def iterate(self, x, y, z):
        pass


class DifferentialAttractor(Attractor, ABC):
    @abstractmethod
    def slope(self, x, y, z):
        pass

    def iterate(self, x, y, z):
        k1, j1, i1 = self.slope(x, y, z)
        k2, j2, i2 = self.slope(
            x + 0.5 * CONFIGS["TIME_STEP"] * k1,
            y + 0.5 * CONFIGS["TIME_STEP"] * j1,
            z + 0.5 * CONFIGS["TIME_STEP"] * i1
        )
        k3, j3, i3 = self.slope(
            x + 0.5 * CONFIGS["TIME_STEP"] * k2,
            y + 0.5 * CONFIGS["TIME_STEP"] * j2,
            z + 0.5 * CONFIGS["TIME_STEP"] * i2
        )
        k4, j4, i4 = self.slope(
            x + CONFIGS["TIME_STEP"] * k3,
            y + CONFIGS["TIME_STEP"] * j3,
            z + CONFIGS["TIME_STEP"] * i3
        )
        return (
            x + CONFIGS["TIME_STEP"] / 6 * (k1 + 2 * k2 + 2 * k3 + k4),
            y + CONFIGS["TIME_STEP"] / 6 * (j1 + 2 * j2 + 2 * j3 + j4),
            z + CONFIGS["TIME_STEP"] / 6 * (i1 + 2 * i2 + 2 * i3 + i4)
        )


class Clifford(Attractor):
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def iterate(self, x, y, z):
        return (numpy.sin(self.a * y) + self.c * numpy.cos(self.a * x),
            numpy.sin(self.b * x) + self.d * numpy.cos(self.b * y),
            0.0
        )


class Dejong(Attractor):
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def iterate(self, x, y, z):
        return (numpy.sin(self.a * y) - numpy.cos(self.b * x),
            numpy.sin(self.c * x) - numpy.cos(self.d * y),
            0.0
        )


class Thomas(DifferentialAttractor):
    def __init__(self, b):
        self.b = b

    def slope(self, x, y, z):
        return (
            numpy.sin(y) - self.b * x,
            numpy.sin(z) - self.b * y,
            numpy.sin(x) - self.b * z
        )


class ThomasEuler(Thomas):
    def __init__(self, b):
        self.b = b
    
    def iterate(self, x, y, z):
        (dx, dy, dz) = super().slope(x, y, z)
        return (x + dx, y + dy, z + dz)


class Aizawa(DifferentialAttractor):
    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def slope(self, x, y, z):
        return (
            (z - self.b) * x - self.d * y,
            self.d * x + (z - self.b) * y,
            (self.c + self.a * z - math.pow(z, 3) / 3
                - (math.pow(x, 2) + math.pow(y, 2)) * (1 + self.e * z) + self.f * z * math.pow(x, 3)
            )
        )


class Lorenz(DifferentialAttractor):
    def __init__(self, sigma, phi, beta):
        self.sigma = sigma
        self.phi = phi
        self.beta = beta

    def slope(self, x, y, z):
        return (
            self.sigma * (y - x),
            -x * z + self.phi * x - y,
            x * y - self.beta * z
        )


class Dadras(DifferentialAttractor):
    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def slope(self, x, y, z):
        return (
            y - self.a * x + self.b * y * z,
            self.c * y - x * z + z,
            self.d * x * y - self.e * z
        )


class Chen(DifferentialAttractor):
    def __init__(self, alpha, beta, gamma):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def slope(self, x, y, z):
        return (
            self.alpha * x - y * z,
            self.beta * y + x * z,
            self.gamma * z + x * y / 3
        )


class Lorenz83(DifferentialAttractor):
    def __init__(self, a, b, f, g):
        self.a = a
        self.b = b
        self.f = f
        self.g = g

    def slope(self, x, y, z):
        return (
            -self.a * x - y ** 2 - z ** 2 + self.a * self.f,
            -y + x * y - self.b * x * z + self.g,
            -z + self.b * x * z + x * z
        )


class Rossler(DifferentialAttractor):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def slope(self, x, y, z):
        return (
            -y - z,
            x + self.a * y,
            self.b + z * (x - self.c)
        )


class Halvorsen(DifferentialAttractor):
    def __init__(self, a):
        self.a = a

    def slope(self, x, y, z):
        return (
            -self.a * x - 4 * y - 4 * z - y ** 2,
            -self.a * y - 4 * z - 4 * x - z ** 2,
            -self.a * z - 4 * x - 4 * y - x ** 2
        )


class RabinovichFabrikant(DifferentialAttractor):
    def __init__(self, alpha, gamma):
        self.alpha = alpha
        self.gamma = gamma

    def slope(self, x, y, z):
        return (
            y * (z - 1 + x ** 2) + self.gamma * x,
            x * (3 * z + 1 - x ** 2) + self.gamma * y,
            -2 * z * (self.alpha + x * y)
        )


class TSUCS(DifferentialAttractor):
    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def slope(self, x, y, z):
        return (
            self.a * (y - x) + self.d * x * z,
            self.b * x - x * z + self.f * y,
            self.c * z + x * y - self.e * x ** 2
        )


class Sprott(DifferentialAttractor):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def slope(self, x, y, z):
        return (
            y + self.a * x * y + x * z,
            1 - self.b * x ** 2 + y * z,
            x - x ** 2 - y ** 2
        )


class FourWing(DifferentialAttractor):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def slope(self, x, y, z):
        return (
            self.a * x + y * z,
            self.b * x + self.c * y - x * z,
            -z - x * y
        )


def get_attractor(name):
    return getattr(sys.modules[__name__], name)
