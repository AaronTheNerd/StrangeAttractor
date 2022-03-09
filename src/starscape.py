"""Methods needed to add a simple star scape to the background of images

Written by Aaron Barge
Copyright 2022
"""


import random
from typing import Tuple

import cv2
import datashader
import matplotlib
import numpy
import pandas

from src.configs import Configs


def generate_starscape(
    CONFIGS: Configs,
    x_range: Tuple[float, float],
    y_range: Tuple[float, float]
):
    num_stars = round(
        CONFIGS.IMAGE_CONFIGS["WIDTH"]
        * CONFIGS.IMAGE_CONFIGS["HEIGHT"]
        * CONFIGS.STARSCAPE_CONFIGS["DENSITY"]
    )
    d = {'x': [], 'y': [], 'weight': []}
    for _ in range(num_stars):
        d['x'] += [random.uniform(*x_range)]
        d['y'] += [random.uniform(*y_range)]
        d['weight'] += [random.uniform(*CONFIGS.STARSCAPE_CONFIGS["WEIGHT_RANGE"])]
    df = pandas.DataFrame(d)
    cvs = datashader.Canvas(
        plot_width = CONFIGS.IMAGE_CONFIGS["WIDTH"],
        plot_height = CONFIGS.IMAGE_CONFIGS["HEIGHT"],
        x_range = x_range,
        y_range = y_range
    )
    agg = cvs.points(df, 'x', 'y', datashader.sum('weight'))
    cmap = matplotlib.colormaps['Greys'].reversed()
    img = datashader.transfer_functions.shade(
        agg,
        cmap = cmap,
        how = "eq_hist"
    )
    datashader.utils.export_image(
        img,
        f"starscape",
        export_path = f"{CONFIGS.FILE_CONFIGS['PATH']}/{CONFIGS.FILE_CONFIGS['ID']}",
        background = "black"
    )


def combine_starscape(CONFIGS: Configs):
    path = f"{CONFIGS.FILE_CONFIGS['PATH']}/{CONFIGS.FILE_CONFIGS['ID']}"
    attractor = cv2.imread(f"{path}/{CONFIGS.IMAGE_CONFIGS['NAME']}.png")
    starscape = cv2.imread(f"{path}/starscape.png")
    for x in range(CONFIGS.IMAGE_CONFIGS["WIDTH"]):
        for y in range(CONFIGS.IMAGE_CONFIGS["HEIGHT"]):
            pixel = attractor[y, x]
            if numpy.all(pixel == [0, 0, 0]):
                attractor[y, x] = starscape[y, x]
    cv2.imwrite(f"{path}/{CONFIGS.IMAGE_CONFIGS['NAME']}.png", attractor)
