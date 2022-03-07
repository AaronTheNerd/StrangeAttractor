"""The main process for generating images of Strange Attractors.

Written by Aaron Barge
Copyright 2022
"""


import functools

import datashader
import matplotlib
import numpy
import pandas
import yaml

from src.attractors import get_attractor
from src.colormaps import register_custom_colormaps
from src.configs import Configs
from src.generate_points import generate_points
from src.loading_bar import LoadingBar
from src.particle_blur import particle_blur
from src.post_processing import post_processing
from src.rotation_matrix import degrees_to_radians, generate_rotation_matrix


def main(CONFIGS):
    img_map = functools.partial(
        datashader.utils.export_image,
        export_path = f'{CONFIGS.FILE_CONFIGS["PATH"]}/{CONFIGS.FILE_CONFIGS["ID"]}',
        background = CONFIGS.IMAGE_CONFIGS["BACKGROUND_COLOR"]
    )
    attractor = get_attractor(CONFIGS.ATTRACTOR_CONFIGS["NAME"])(*CONFIGS.ATTRACTOR_CONFIGS["ARGS"])
    loading_bar = LoadingBar(CONFIGS.CONFIGS["ITERATIONS"] - 1, width=40)
    if CONFIGS.CONFIGS["CUSTOM_COLORMAPS"]:
        print("Loading custom colormaps")
        register_custom_colormaps()
    print("Generating initial points")
    particles = generate_points(CONFIGS)
    print("Generating rotation matrix")
    alpha = degrees_to_radians(CONFIGS.PERSPECTIVE_CONFIGS["X_ROTATION_DEG"])
    beta = degrees_to_radians(CONFIGS.PERSPECTIVE_CONFIGS["Y_ROTATION_DEG"])
    gamma = degrees_to_radians(CONFIGS.PERSPECTIVE_CONFIGS["Z_ROTATION_DEG"])
    matrix = generate_rotation_matrix(alpha, beta, gamma)
    print("Iterating points")
    d = {'x': [], 'y': [], 'weight': []}
    for i in range(CONFIGS.CONFIGS["ITERATIONS"]):
        for index, (x, y, z) in enumerate(particles):
            x, y, z = attractor.iterate(CONFIGS.CONFIGS["TIME_STEP"], x, y, z)
            particles[index] = (x, y, z)
            (x, y, _) = tuple(matrix.dot(numpy.array( (x, y, z) )))
            d_append = particle_blur(CONFIGS, x, y)
            d['x'] += d_append['x']
            d['y'] += d_append['y']
            d['weight'] += d_append['weight']
        loading_bar.loading(i)
    print("\nFinished iterating points")
    print("Converting point history to dataframe")
    df1 = pandas.DataFrame(d)
    print("Converting dataframe to datashader")
    x_range = (min(d['x']), max(d['x']))
    y_range = (min(d['y']), max(d['y']))
    cvs1 = datashader.Canvas(
        plot_width = CONFIGS.IMAGE_CONFIGS["WIDTH"],
        plot_height = CONFIGS.IMAGE_CONFIGS["HEIGHT"],
        x_range = x_range,
        y_range = y_range
    )
    print("Aggregating points")
    agg1 = cvs1.points(df1, 'x', 'y', datashader.sum('weight'))
    print("Shading datashader")
    cmap = matplotlib.colormaps[CONFIGS.SHADER_CONFIGS["COLOR_MAP"]]
    if CONFIGS.SHADER_CONFIGS["REVERSED"]:
        cmap = cmap.reversed()
    img = datashader.transfer_functions.shade(
        agg1,
        cmap = cmap,
        span = None if CONFIGS.SHADER_CONFIGS["HOW"] == "eq_hist" else CONFIGS.SHADER_CONFIGS["SPAN"],
        how = CONFIGS.SHADER_CONFIGS["HOW"]
    )
    print("Spreading pixels")
    img = datashader.transfer_functions.dynspread(
        img,
        threshold = CONFIGS.SPREAD_CONFIGS["THRESHOLD"],
        max_px = CONFIGS.SPREAD_CONFIGS["MAX_PX"],
        shape = CONFIGS.SPREAD_CONFIGS["SHAPE"],
        how = CONFIGS.SPREAD_CONFIGS["HOW"]
    )
    print("Exporting Image")
    img_map(img, CONFIGS.IMAGE_CONFIGS["NAME"])
    print("Dumping configs")
    with open(f'{CONFIGS.FILE_CONFIGS["PATH"]}/{CONFIGS.FILE_CONFIGS["ID"]}/configs.yml', 'w+') as output_configs:
        yaml.dump(CONFIGS.CONFIGS, output_configs, sort_keys = False)
    print("Post processing")
    post_processing(CONFIGS)
    print("COMPLETE")


if __name__ == "__main__":
    main(Configs('configs.yml'))
