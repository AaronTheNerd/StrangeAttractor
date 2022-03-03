"""Contains all the childen of the Attractor and DifferentialAttractor ABCs.

Written by Aaron Barge
Copyright 2022
"""


import math
import sys
from abc import ABC, abstractmethod
from typing import Tuple

import numpy

from src.configs import CONFIGS


Vector = Tuple[float, float, float]


class Attractor(ABC):
    """Represents attractors which are governed by discrete functions.
    i.e. $$\hat{v}_{n+1} = f(\hat{v}_n)$$
    """
    @abstractmethod
    def iterate(self, x: float, y: float, z: float) -> Vector:
        pass


class DifferentialAttractor(Attractor, ABC):
    """Represents attractors which are governed by differential functions using a fourth-order Runge Kutta method to approximate the positions of the particle. i.e.
    $$\\frac{d\hat{v}}{dt} = f(\hat{v})$$
    which is discretely approximated by 
    $$\hat{v}_{n+1} = \\frac{\Delta t}{6}(\hat{k}_1+2\hat{k}_2+2\hat{k}_3+\hat{k}_4)$$
    where
    $$\hat{k}_1 = f(\hat{v}_n)$$
    $$\hat{k}_2 = f(\hat{v}_n + 0.5\Delta t\hat{k}_1)$$
    $$\hat{k}_3 = f(\hat{v}_n + 0.5\Delta t\hat{k}_2)$$
    $$\hat{k}_4 = f(\hat{v}_n + \Delta t\hat{k}_3)$$
    """
    @abstractmethod
    def slope(self, x: float, y: float, z: float) -> Vector:
        pass

    def iterate(self, x: float, y: float, z: float) -> Vector:
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
    """$$x_{n+1} = \sin(ay_n)+c\cos(a x_n)$$
    $$y_{n+1} = \sin(bx_n) + d\cos(by_n)$$
    """
    def __init__(self, a: float, b: float, c: float, d: float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def iterate(self, x: float, y: float, z: float) -> Vector:
        return (numpy.sin(self.a * y) + self.c * numpy.cos(self.a * x),
            numpy.sin(self.b * x) + self.d * numpy.cos(self.b * y),
            0.0
        )


class Dejong(Attractor):
    """$$x_{n+1} = \sin(ay_n) - \cos(bx_n)$$
    $$y_{n+1} = \sin(cx_n) - \cos(dy_n)$$
    """
    def __init__(self, a: float, b: float, c: float, d: float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def iterate(self, x: float, y: float, z: float) -> Vector:
        return (numpy.sin(self.a * y) - numpy.cos(self.b * x),
            numpy.sin(self.c * x) - numpy.cos(self.d * y),
            0.0
        )


class Thomas(DifferentialAttractor):
    """$$\\frac{dx}{dt} = \sin(y) - bx$$
    $$\\frac{dy}{dt} = \sin(z) - by$$
    $$\\frac{dz}{dt} = \sin(x) - bz$$
    """
    def __init__(self, b: float):
        self.b = b

    def slope(self, x: float, y: float, z: float) -> Vector:
        return (
            numpy.sin(y) - self.b * x,
            numpy.sin(z) - self.b * y,
            numpy.sin(x) - self.b * z
        )


class ThomasEuler(Thomas):
    """A special version of the Thomas Attractor which uses Euler Integration instead of Runge-Kutta
    $$x_{n+1} = x_n + \sin(y_n) - bx_n$$
    $$y_{n+1} = y_n + \sin(z_n) - by_n$$
    $$z_{n+1} = z_n + \sin(x_n) - bz_n$$
    """
    def __init__(self, b: float):
        self.b = b
    
    def iterate(self, x: float, y: float, z: float) -> Vector:
        (dx, dy, dz) = super().slope(x, y, z)
        return (x + dx, y + dy, z + dz)


class Aizawa(DifferentialAttractor):
    """$$\\frac{dx}{dt} = (z-b)x-dy$$
    $$\\frac{dy}{dt} = dx + (z-b)y$$
    $$\\frac{dz}{dt} = c+az - \\frac{z^3}{3}-(x^2+y^2)(1+ez)+fzx^3$$
    """
    def __init__(self, a: float, b: float, c: float, d: float, e: float, f: float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def slope(self, x: float, y: float, z: float) -> Vector:
        return (
            (z - self.b) * x - self.d * y,
            self.d * x + (z - self.b) * y,
            (self.c + self.a * z - math.pow(z, 3) / 3 - (math.pow(x, 2) + math.pow(y, 2))
                * (1 + self.e * z) + self.f * z * math.pow(x, 3)
            )
        )


class Lorenz(DifferentialAttractor):
    """$$\\frac{dx}{dt} = \sigma * (y-x)$$
    $$\\frac{dy}{dt} = -xz+x\\rho-y$$
    $$\\frac{dz}{dt} = xy-z\\beta$$
    """
    def __init__(self, sigma: float, rho: float, beta: float):
        self.sigma = sigma
        self.rho = rho
        self.beta = beta

    def slope(self, x: float, y: float, z: float) -> Vector:
        return (
            self.sigma * (y - x),
            -x * z + self.rho * x - y,
            x * y - self.beta * z
        )


class Dadras(DifferentialAttractor):
    """$$\\frac{dx}{dt} = y-ax+byz$$
    $$\\frac{dy}{dt} = cy-xz+z$$
    $$\\frac{dz}{dt} = dxy-ez$$
    """
    def __init__(self, a: float, b: float, c: float, d: float, e: float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def slope(self, x: float, y: float, z: float) -> Vector:
        return (
            y - self.a * x + self.b * y * z,
            self.c * y - x * z + z,
            self.d * x * y - self.e * z
        )


class Chen(DifferentialAttractor):
    """$$\\frac{dx}{dt} = \\alpha x-yz$$
    $$\\frac{dy}{dt} = \\beta y+xz$$
    $$\\frac{dz}{dt} = \delta z+xy/3$$
    """
    def __init__(self, alpha: float, beta: float, delta: float):
        self.alpha = alpha
        self.beta = beta
        self.delta = delta

    def slope(self, x: float, y: float, z: float) -> Vector:
        return (
            self.alpha * x - y * z,
            self.beta * y + x * z,
            self.delta * z + x * y / 3
        )


class Lorenz83(DifferentialAttractor):
    """$$\\frac{dx}{dt} = -ax-y^2-z^2+af$$
    $$\\frac{dy}{dt} = -y+xy-bxz+g$$
    $$\\frac{dz}{dt} = -z+bxy+xz$$
    """
    def __init__(self, a: float, b: float, f: float, g: float):
        self.a = a
        self.b = b
        self.f = f
        self.g = g

    def slope(self, x: float, y: float, z: float) -> Vector:
        return (
            -self.a * x - y ** 2 - z ** 2 + self.a * self.f,
            -y + x * y - self.b * x * z + self.g,
            -z + self.b * x * y + x * z
        )


class Rossler(DifferentialAttractor):
    """$$\\frac{dx}{dt} = -y-z$$
    $$\\frac{dy}{dt} = x+ay$$
    $$\\frac{dz}{dt} = b+z(x-c)$$
    """
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def slope(self, x: float, y: float, z: float) -> Vector:
        return (
            -y - z,
            x + self.a * y,
            self.b + z * (x - self.c)
        )


class Halvorsen(DifferentialAttractor):
    """$$\\frac{dx}{dt} = -ax-4y-4z-y^2$$
    $$\\frac{dy}{dt} = -ay-4z-4x-z^2$$
    $$\\frac{dz}{dt} = -az-4x-4y-x^2$$
    """
    def __init__(self, a: float):
        self.a = a

    def slope(self, x: float, y: float, z: float) -> Vector:
        return (
            -self.a * x - 4 * y - 4 * z - y ** 2,
            -self.a * y - 4 * z - 4 * x - z ** 2,
            -self.a * z - 4 * x - 4 * y - x ** 2
        )


class RabinovichFabrikant(DifferentialAttractor):
    """$$\\frac{dx}{dt} = y(z-1+x^2)+\gamma x$$
    $$\\frac{dy}{dt} = x(3z+1-x^2)+\gamma y$$
    $$\\frac{dz}{dt} = -2z(\\alpha+xy)$$
    """
    def __init__(self, alpha: float, gamma: float):
        self.alpha = alpha
        self.gamma = gamma

    def slope(self, x: float, y: float, z: float) -> Vector:
        return (
            y * (z - 1 + x ** 2) + self.gamma * x,
            x * (3 * z + 1 - x ** 2) + self.gamma * y,
            -2 * z * (self.alpha + x * y)
        )


class TSUCS(DifferentialAttractor):
    """Three-Scroll unified Chaotic System
    $$\\frac{dx}{dt} = a(y-x)+dxz$$
    $$\\frac{dy}{dt} = bx-xz+fy$$
    $$\\frac{dz}{dt} = cz+xy-ex^2$$
    """
    def __init__(self, a: float, b: float, c: float, d: float, e: float, f: float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def slope(self, x: float, y: float, z: float) -> Vector:
        return (
            self.a * (y - x) + self.d * x * z,
            self.b * x - x * z + self.f * y,
            self.c * z + x * y - self.e * x ** 2
        )


class Sprott(DifferentialAttractor):
    """$$\\frac{dx}{dt} = y+axy+xz$$
    $$\\frac{dy}{dt} = 1-bx^2+yz$$
    $$\\frac{dz}{dt} = x-x^2-y^2$$
    """
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def slope(self, x: float, y: float, z: float) -> Vector:
        return (
            y + self.a * x * y + x * z,
            1 - self.b * x ** 2 + y * z,
            x - x ** 2 - y ** 2
        )


class FourWing(DifferentialAttractor):
    """$$\\frac{dx}{dt} = ax+yz$$
    $$\\frac{dy}{dt} = bx+cy-xz$$
    $$\\frac{dz}{dt} = -z-xy$$
    """
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def slope(self, x: float, y: float, z: float) -> Vector:
        return (
            self.a * x + y * z,
            self.b * x + self.c * y - x * z,
            -z - x * y
        )


def get_attractor(name):
    """Returns a class defined in this module from its name."""
    return getattr(sys.modules[__name__], name)
