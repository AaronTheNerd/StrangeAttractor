"""Contains all the necessary methods for performing some post processing on the Strange Attractor image.

Written by Aaron Barge
Copyright 2022
"""


import numpy
import skimage

from src.configs import (BILATERAL_DENOISE_CONFIGS, FILE_CONFIGS,
                     GAUSSIAN_FILTER_CONFIGS, MEDIAN_FILTER_CONFIGS,
                     TV_DENOISE_CONFIGS)


def post_processing():
    """Filters/Denoises the image based on the configs.yaml."""
    image = skimage.io.imread(
        fname = f'{FILE_CONFIGS["PATH"]}/{FILE_CONFIGS["ID"]}/image.png'
    )
    image = apply_denoise(image)
    image = apply_filters(image)
    skimage.io.imsave(
        fname=f'{FILE_CONFIGS["PATH"]}/{FILE_CONFIGS["ID"]}/image.png',
        arr=image
    )


def apply_denoise(image):
    if TV_DENOISE_CONFIGS["DENOISE"]:
        image = skimage.restoration.denoise_tv_chambolle(
            image,
            weight = TV_DENOISE_CONFIGS["WEIGHT"],
            channel_axis = TV_DENOISE_CONFIGS["CHANNEL_AXIS"]
        )
    if BILATERAL_DENOISE_CONFIGS["DENOISE"]:
        image = skimage.restoration.denoise_bilateral(
            image,
            sigma_color = BILATERAL_DENOISE_CONFIGS["SIGMA_COLOR"],
            sigma_spatial = BILATERAL_DENOISE_CONFIGS["SIGMA_SPATIAL"],
            channel_axis = BILATERAL_DENOISE_CONFIGS["CHANNEL_AXIS"]
        )
    return image


def apply_filters(image):
    if GAUSSIAN_FILTER_CONFIGS["FILTER"]:
        image = skimage.filters.gaussian(
            image,
            sigma=(GAUSSIAN_FILTER_CONFIGS["SIGMA_Y"], GAUSSIAN_FILTER_CONFIGS["SIGMA_X"]),
            truncate=GAUSSIAN_FILTER_CONFIGS["TRUNCATE"],
            multichannel=True
        )
    if MEDIAN_FILTER_CONFIGS["FILTER"]:
        image = skimage.filters.median(
            image,
            numpy.ones(tuple(MEDIAN_FILTER_CONFIGS["FOOTPRINT"] + [3]))
        )
    return image
