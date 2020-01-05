# -*- coding: utf-8 -*-

"""
This module provides a function to generate a color palette from
a collection of images
"""

import math
import cv2 as cv
from sklearn.cluster import MeanShift, estimate_bandwidth
import pandas as pd

IMAGE_SIZE = 5
QUANTILE = 0.05


def generate_color_palette(files):
    """
    Find mean and std. dev. of colors found in a directory of sample images.
    """

    xyz = pd.DataFrame()
    hsv = pd.DataFrame()

    for file in files:
        img = cv.imread(file)
        img = cv.resize(img, (IMAGE_SIZE, IMAGE_SIZE))

        xyz = pd.concat([xyz, get_hsv_cart_values_from_image(img)])
        hsv = pd.concat([hsv, get_hsv_polar_values_from_images(img)])

    labels, label_count = find_clusters(xyz)

    hsv["labels"] = labels

    return get_palette(hsv, label_count)


def find_clusters(df):
    """
    Apply clustering to a dataframe of hsv values in cartesian
    form. Returns an array of labels applies to each row in the
    dataframe.
    """

    bandwidth = estimate_bandwidth(df, quantile=QUANTILE)
    clt = MeanShift(bandwidth=bandwidth)
    clt.fit(df)

    label_count = clt.labels_.max()

    return clt.labels_, label_count


def get_palette(df, num_clusters):
    """
    Generate a list of means and std.dev. for each clusters.
    """

    clusters = pd.DataFrame(columns=["mean", "std"])
    for i in range(num_clusters):
        filtered = df[df["labels"] == i]

        mean = filtered.mean(axis=0)
        std = filtered.std(axis=0)

        clusters = clusters.append(
            {
                "m0": mean[0],
                "m1": mean[1],
                "m2": mean[2],
                "std0": std[0],
                "std1": std[1],
                "std2": std[2]
            },
            ignore_index=True
        )

    return clusters


def get_hsv_polar_values_from_images(img):
    """
    Reads an image in BGR color space and returns a dataframe containing
    all hue, saturation, and value pixels in polar form.
    """

    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV_FULL)
    channels = cv.split(img_hsv)

    df = pd.DataFrame()
    df["h"] = channels[0].flatten()
    df["s"] = channels[1].flatten()
    df["v"] = channels[2].flatten()

    return df


def get_hsv_cart_values_from_image(img):
    """
    Reads an image in BGR color space and returns a dataframe containing
    all hue, saturation, and value pixels in cartesian form.
    """

    height, width, channels_count = img.shape

    if channels_count != 3:
        raise Exception("img does not contain 3 channels")

    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV_FULL)
    channels = cv.split(img_hsv)

    x_vals = []
    y_vals = []
    z_vals = []

    for i in range(width):
        for j in range(height):

            # Values are stored in image in 8 bit, from 0 to 255
            # We need to represent them in their correct format
            h = channels[0][j][i] / 255 * 360
            s = channels[1][j][i] / 255 * 100
            v = channels[2][j][i] / 255 * 100

            x, y, z = hsv_polar_to_cartesian(h, s, v)

            x_vals.append(x)
            y_vals.append(y)
            z_vals.append(z)

    df = pd.DataFrame()
    df["x"] = x_vals
    df["y"] = y_vals
    df["z"] = z_vals

    return df


def hsv_polar_to_cartesian(h, s, v):
    """
    Converts an hsv color value from a polar representation to
    a cartesian representation.

    - Hue is a value from 0 to 360 degrees.
    - Saturation is a value from 0 to 100.
    - Value is a value from 0 to 100.

    Cartesian coordinates are returned as a tupple, in the form(x, y, z).
    """

    angle_rad = math.radians(h)
    radius = s / 100
    value = v / 100

    return (radius * math.cos(angle_rad), radius * math.sin(angle_rad), value)
