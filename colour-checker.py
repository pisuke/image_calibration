#!/usr/bin/env python

import colour
import numpy as np
import pprint
import cv2
import glob
import matplotlib.pyplot as plt
import os
from collections import OrderedDict

from colour_checker_detection import (
    EXAMPLES_RESOURCES_DIRECTORY,
    colour_checkers_coordinates_segmentation,
    detect_colour_checkers_segmentation)
from colour_checker_detection.detection.segmentation import (
    adjust_image)

colour.plotting.colour_style()

colour.utilities.describe_environment();

COLOUR_CHECKER_IMAGE_PATHS = glob.glob(
    os.path.join(EXAMPLES_RESOURCES_DIRECTORY, 'detection', '*.png'))

COLOUR_CHECKER_IMAGES = [
    colour.cctf_decoding(colour.io.read_image(path))
    for path in COLOUR_CHECKER_IMAGE_PATHS
]

for image in COLOUR_CHECKER_IMAGES:
    colour.plotting.plot_image(colour.cctf_encoding(image));

pp = pprint.PrettyPrinter(indent=4, width=41, depth=1)
#pp.pprint(colour.CCS_COLOURCHECKERS.keys)
for k in colour.CCS_COLOURCHECKERS.keys():
    pp.pprint(k)

colour_checker_reference = colour.CCS_COLOURCHECKERS[
    'ColorChecker24 - After November 2014']

