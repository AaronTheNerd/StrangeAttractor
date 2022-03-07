"""Main test file.

Written by Aaron Barge
Copyright 2022
"""


import random

from src.configs import Configs
from src.main import main


if __name__ == "__main__":
    CONFIGS = Configs('src/test/configs.yml')
    step = CONFIGS.ATTRACTOR_CONFIGS["DIFF"]
    bounds = CONFIGS.ATTRACTOR_CONFIGS["BOUNDS"]
    for id in range(CONFIGS.CONFIGS["NUM"]):
        CONFIGS.FILE_CONFIGS["ID"] = id
        CONFIGS.CONFIGS["GENERATE_SEED"] = True
        CONFIGS.generate_seed()
        for i, bound in enumerate(bounds):
            lower = bound[0]
            upper = bound[1]
            CONFIGS.ATTRACTOR_CONFIGS["ARGS"][i] = random.randint(
                0, 
                int(round((upper - lower) / step))
            ) * step + lower

        print(f"Arguments: {CONFIGS.ATTRACTOR_CONFIGS['ARGS']}")
        main(CONFIGS)
        CONFIGS.CONFIGS["CUSTOM_COLORMAPS"] = False
