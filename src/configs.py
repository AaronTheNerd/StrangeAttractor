"""Contains the loaded configs.yaml file as CONFIGS along with some shortcuts.

Written by Aaron Barge
Copyright 2022
"""


import random

import yaml


class Configs:
    def __init__(self, filename):
        self.CONFIGS = {}
        self.PARTICLE_BLUR_CONFIGS = {}
        self.IMAGE_CONFIGS = {}
        self.SHADER_CONFIGS = {}
        self.SPREAD_CONFIGS = {}
        self.FILTER_CONFIGS = {}
        self.GAUSSIAN_FILTER_CONFIGS = {}
        self.MEDIAN_FILTER_CONFIGS = {}
        self.DENOISE_CONFIGS = {}
        self.TV_DENOISE_CONFIGS = {}
        self.BILATERAL_DENOISE_CONFIGS = {}
        self.FILE_CONFIGS = {}
        self.POINTS_CONFIGS = {}
        self.PERSPECTIVE_CONFIGS = {}
        self.ATTRACTOR_CONFIGS = {}
        self.load_configs(filename)


    def generate_seed(self):
        if self.CONFIGS["GENERATE_SEED"]:
            self.CONFIGS["GENERATE_SEED"] = False
            self.CONFIGS["SEED"] = random.randint(-2147483648, 2147483647)

        # Seed RNG
        random.seed(self.CONFIGS["SEED"])


    def load_configs(self, filename):
        with open(filename, 'r') as file:
            self.CONFIGS = yaml.safe_load(file)

        # Generate seed
        self.generate_seed()

        # Create shortcuts
        self.PARTICLE_BLUR_CONFIGS = self.CONFIGS["PARTICLE_BLUR_CONFIGS"]
        self.IMAGE_CONFIGS = self.CONFIGS["IMAGE_CONFIGS"]
        self.SHADER_CONFIGS = self.CONFIGS["SHADER_CONFIGS"]
        self.SPREAD_CONFIGS = self.CONFIGS["SPREAD_CONFIGS"]
        self.FILTER_CONFIGS = self.CONFIGS["FILTER_CONFIGS"]
        self.GAUSSIAN_FILTER_CONFIGS = self.FILTER_CONFIGS["GAUSSIAN"]
        self.MEDIAN_FILTER_CONFIGS = self.FILTER_CONFIGS["MEDIAN"]
        self.DENOISE_CONFIGS = self.CONFIGS["DENOISE_CONFIGS"]
        self.TV_DENOISE_CONFIGS = self.DENOISE_CONFIGS["TV"]
        self.BILATERAL_DENOISE_CONFIGS = self.DENOISE_CONFIGS["BILATERAL"]
        self.FILE_CONFIGS = self.CONFIGS["FILE_CONFIGS"]
        self.POINTS_CONFIGS = self.CONFIGS["POINTS_CONFIGS"]
        self.PERSPECTIVE_CONFIGS = self.CONFIGS["PERSPECTIVE_CONFIGS"]
        self.ATTRACTOR_CONFIGS = self.CONFIGS["ATTRACTOR_CONFIGS"]
