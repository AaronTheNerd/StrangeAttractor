"""Contains all the necessary methods for performing some post processing on the Strange Attractor image.

Written by Aaron Barge
Copyright 2022
"""


import numpy
import skimage
from src.configs import Configs


def post_processing(CONFIGS: Configs):
    """Filters/Denoises the image based on the configs.yaml."""
    path = f'{CONFIGS.FILE_CONFIGS["PATH"]}/{CONFIGS.FILE_CONFIGS["ID"]}'
    image = skimage.io.imread(
        fname = f'{path}/image.png'
    )
    image = apply_denoise(CONFIGS, image)
    image = apply_filters(CONFIGS, image)
    skimage.io.imsave(
        fname=f'{path}/image.png',
        arr=image
    )


def apply_denoise(CONFIGS: Configs, image: 'ndarray'):
    if CONFIGS.TV_DENOISE_CONFIGS["DENOISE"]:
        image = skimage.restoration.denoise_tv_chambolle(
            image,
            weight = CONFIGS.TV_DENOISE_CONFIGS["WEIGHT"],
            channel_axis = CONFIGS.TV_DENOISE_CONFIGS["CHANNEL_AXIS"]
        )
    if CONFIGS.BILATERAL_DENOISE_CONFIGS["DENOISE"]:
        image = skimage.restoration.denoise_bilateral(
            image,
            sigma_color = CONFIGS.BILATERAL_DENOISE_CONFIGS["SIGMA_COLOR"],
            sigma_spatial = CONFIGS.BILATERAL_DENOISE_CONFIGS["SIGMA_SPATIAL"],
            channel_axis = CONFIGS.BILATERAL_DENOISE_CONFIGS["CHANNEL_AXIS"]
        )
    return image


def apply_filters(CONFIGS: Configs, image: 'ndarray'):
    if CONFIGS.GAUSSIAN_FILTER_CONFIGS["FILTER"]:
        image = skimage.filters.gaussian(
            image,
            sigma = (
                CONFIGS.GAUSSIAN_FILTER_CONFIGS["SIGMA_Y"],
                CONFIGS.GAUSSIAN_FILTER_CONFIGS["SIGMA_X"]
            ),
            truncate = CONFIGS.GAUSSIAN_FILTER_CONFIGS["TRUNCATE"],
            multichannel = True
        )
    if CONFIGS.MEDIAN_FILTER_CONFIGS["FILTER"]:
        image = skimage.filters.median(
            image,
            numpy.ones(tuple(CONFIGS.MEDIAN_FILTER_CONFIGS["FOOTPRINT"] + [3]))
        )
    return image
