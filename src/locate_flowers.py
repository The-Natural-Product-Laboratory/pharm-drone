# -*- coding: utf-8 -*-

"""
This module provides a function to locate flowers in a top-down image taken
by a UAV.
"""

import os
import cv2 as cv
import numpy as np

CONTOUR_COLOR = (0, 0, 255)
CONTOUR_WIDTH = 3
KERNEL = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))


def locate_flowers(file, colors, out_dir):
    """
    Locates flowers in the image specified by a file path. Uses
    a color palette for identification. Outputs the image to a specified
    directory.
    """
    img = cv.imread(file)

    edges_img = perform_edge_detection(img)
    mask = apply_color_threshold(edges_img, colors)
    clean_mask = perform_noise_removal(mask)

    contours, _ = cv.findContours(
        clean_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
    )

    cv.drawContours(img, contours, -1, CONTOUR_COLOR, CONTOUR_WIDTH)

    cv.imwrite(out_dir + "/" + os.path.basename(file), img)


def perform_edge_detection(img):
    """
    Generates an image including only prominent edges in the image
    given as input.
    """
    lower, upper = get_canny_thresholds(img)

    blur_img = cv.GaussianBlur(img, (7, 7), cv.BORDER_DEFAULT)

    edges_img = cv.Canny(blur_img, lower, upper)
    edges_img = cv.dilate(edges_img, KERNEL, iterations=1)

    return cv.copyTo(img, edges_img)


def get_canny_thresholds(img):
    """
    Determines the ideal threshold to use
    for the Canny edge detector.
    """
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    v = np.median(gray)

    lower = int(max(0, (1.0 - 0.33) * v))
    upper = int(min(255, (1.0 + 0.33) * v))

    return lower, upper


def apply_color_threshold(img, colors):
    """
    Thresholds an image according to a color palette.
    The color palette should include a mean color value
    in HSV, and its standard deviation.
    """
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV_FULL)

    height, width, _ = img.shape

    mask = np.zeros((height, width, 1), dtype=np.uint8)

    for _, color in colors.iterrows():
        submask = cv.inRange(
            hsv,
            (
                color["m0"] - color["std0"],
                color["m1"] - color["std1"],
                color["m2"] - color["std2"],
            ),
            (
                color["m0"] + color["std0"],
                color["m1"] + color["std1"],
                color["m2"] + color["std2"],
            ),
        )

        mask = cv.bitwise_or(mask, submask)

    return mask


def perform_noise_removal(mask):
    """
    Remove potential noise from mask. Noise is
    defined as white pixels with no neighbours.
    """
    trans1 = cv.dilate(mask, KERNEL, iterations=4)
    trans1 = cv.erode(trans1, KERNEL, iterations=5)
    return cv.dilate(trans1, KERNEL, iterations=7)
