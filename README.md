# Strange Attractor

> Program for generating images based on paths traced by particles controlled by a strange attractor.

## Installation

With pipenv, `make install` can be run in the root of the project to install all the necessary dependencies. 

## Notes on Usage

The only file which needs to be modified is order to customize the images in `configs.yaml`. Changing the file structure or `configs.yaml` structure will have unintended effects on the output.

## File Structure

```
.
├── maps
│   ├── 1
│   │   ├── configs.yml
│   │   └── image.png
│   ├── 2
│   │   ├── configs.yml
│   │   └── image.png
│   ├── 3
│   │   ├── configs.yml
│   │   └── image.png
│   ├── 4
│   │   ├── configs.yml
│   │   └── image.png
│   ├── 5
│   │   ├── configs.yml
│   │   └── image.png
│   ├── 6
│   │   ├── configs.yml
│   │   └── image.png
│   ├── 7
│   │   ├── configs.yml
│   │   └── image.png
│   ├── 8
│   │   ├── configs.yml
│   │   └── image.png
│   └── 9
│       ├── configs.yml
│       └── image.png
├── src
│   ├── attractors.py
│   ├── colormaps.py
│   ├── configs.py
│   ├── generate_points.py
│   ├── loading_bar.py
│   ├── main.py
│   ├── particle_blur.py
│   ├── post_processing.py
│   └── rotation_matrix.py
├── Pipfile
├── Pipfile.lock
├── README.md
├── configs.yml
└── Makefile
```

