# Written by Aaron Barge
# Copyright 2022


import functools

import datashader
import matplotlib
import numpy
import pandas
import yaml

from attractors import get_attractor
from colormaps import register_custom_colormaps
from configs import (ATTRACTOR_CONFIGS, CONFIGS, FILE_CONFIGS, IMAGE_CONFIGS,
                     PERSPECTIVE_CONFIGS, SHADER_CONFIGS, SPREAD_CONFIGS)
from generate_points import generate_points
from loading_bar import LoadingBar
from particle_blur import particle_blur
from post_processing import post_processing
from rotation_matrix import degrees_to_radians, generate_rotation_matrix


def main():
    img_map = functools.partial(
        datashader.utils.export_image,
        export_path = f'{FILE_CONFIGS["PATH"]}/{FILE_CONFIGS["ID"]}',
        background = IMAGE_CONFIGS["BACKGROUND_COLOR"]
    )
    attractor = get_attractor(ATTRACTOR_CONFIGS["NAME"])(*ATTRACTOR_CONFIGS["ARGS"])
    loading_bar = LoadingBar(CONFIGS["ITERATIONS"] - 1, width=40)
    print("Loading custom colormaps")
    register_custom_colormaps()
    print("Generating initial points")
    particles = generate_points()
    print("Generating rotation matrix")
    alpha = degrees_to_radians(PERSPECTIVE_CONFIGS["X_ROTATION_DEG"])
    beta = degrees_to_radians(PERSPECTIVE_CONFIGS["Y_ROTATION_DEG"])
    gamma = degrees_to_radians(PERSPECTIVE_CONFIGS["Z_ROTATION_DEG"])
    matrix = generate_rotation_matrix(alpha, beta, gamma)
    print("Iterating points")
    d = {'x': [], 'y': [], 'weight': []}
    for i in range(CONFIGS["ITERATIONS"]):
        for index, (x, y, z) in enumerate(particles):
            x, y, z = attractor.iterate(x, y, z)
            particles[index] = (x, y, z)
            (x, y, _) = tuple(matrix.dot(numpy.array( (x, y, z) )))
            d_append = particle_blur(x, y)
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
        plot_width = IMAGE_CONFIGS["WIDTH"],
        plot_height = IMAGE_CONFIGS["HEIGHT"],
        x_range = x_range,
        y_range = y_range
    )
    print("Aggregating points")
    agg1 = cvs1.points(df1, 'x', 'y', datashader.sum('weight'))
    print("Shading datashader")
    img = datashader.transfer_functions.shade(
        agg1,
        cmap = matplotlib.colormaps[SHADER_CONFIGS["COLOR_MAP"]],
        span = None if SHADER_CONFIGS["HOW"] == "eq_hist" else SHADER_CONFIGS["SPAN"],
        how = SHADER_CONFIGS["HOW"]
    )
    print("Spreading pixels")
    img = datashader.transfer_functions.dynspread(
        img,
        threshold = SPREAD_CONFIGS["THRESHOLD"],
        max_px = SPREAD_CONFIGS["MAX_PX"],
        shape = SPREAD_CONFIGS["SHAPE"],
        how = SPREAD_CONFIGS["HOW"]
    )
    print("Exporting Image")
    img_map(img, "image")
    print("Dumping configs")
    with open(f'{FILE_CONFIGS["PATH"]}/{FILE_CONFIGS["ID"]}/configs.yml', 'w+') as output_configs:
        yaml.dump(CONFIGS, output_configs, sort_keys = False)
    print("Post processing")
    post_processing()
    print("COMPLETE")


if __name__ == "__main__":
    main()
