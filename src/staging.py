"""Modified the attractor's size and shape for final image.

Written by Aaron Barge
Copyright 2022
"""


from typing import Tuple

from src.configs import Configs


def stage(
    CONFIGS: Configs,
    x_range: Tuple[float, float],
    y_range: Tuple[float, float]
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    if CONFIGS.STAGING_CONFIGS["TYPE"] == "custom":
        x_range = CONFIGS.STAGING_CONFIGS["X_RANGE"]
        y_range = CONFIGS.STAGING_CONFIGS["Y_RANGE"]
    elif CONFIGS.STAGING_CONFIGS["TYPE"] == "fit_data":
        pass
    elif CONFIGS.STAGING_CONFIGS["TYPE"] == "ratio":
        x_length = (x_range[1] - x_range[0]) / CONFIGS.STAGING_CONFIGS["RATIO"]
        y_length = (y_range[1] - y_range[0]) / CONFIGS.STAGING_CONFIGS["RATIO"]
        x_mid = (x_range[0] + x_range[1]) / 2
        y_mid = (y_range[0] + y_range[1]) / 2
        x_range = (x_mid - x_length / 2, x_mid + x_length / 2)
        y_range = (y_mid - y_length / 2, y_mid + y_length / 2)
    else:
        raise Exception(
            f"Invalid STAGING_CONFIGS attribute TYPE received: {CONFIGS.STAGING_CONFIGS['TYPE']}"
        )
    if (CONFIGS.STAGING_CONFIGS["KEEP_ASPECT_RATIO"]
        and CONFIGS.STAGING_CONFIGS["TYPE"] != "custom"
    ):
        x_length = x_range[1] - x_range[0]
        y_length = y_range[1] - y_range[0]
        ratio_original = x_length / y_length
        ratio_final = CONFIGS.IMAGE_CONFIGS["WIDTH"] / CONFIGS.IMAGE_CONFIGS["HEIGHT"]
        scale = ratio_final / ratio_original
        if ratio_final < ratio_original:
            y_length /= scale
            y_mid = (y_range[0] + y_range[1]) / 2
            y_range = (y_mid - y_length / 2, y_mid + y_length / 2)
        elif ratio_final > ratio_original:
            x_length *= scale
            x_mid = (x_range[0] + x_range[1]) / 2
            x_range = (x_mid - x_length / 2, x_mid + x_length / 2)
    return (x_range, y_range)
