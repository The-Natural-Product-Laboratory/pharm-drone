# -*- coding: utf-8 -*-

"""
Entry module for pharm-drone
"""

import click
import pandas as pd

from src import color_palette, locate_flowers


@click.group()
def cli():
    """
    Entry point for cli application
    """


@cli.command()
@click.option(
    '--out', '-o',
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    nargs=1)
@click.argument(
    'src',
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    nargs=-1,
    required=True)
def palette(src, out):
    """Generates a color palette from a collection of images."""

    pal = color_palette.generate_color_palette(src).to_csv(out, header=True)
    if out is None:
        click.echo(pal)


@cli.command()
@click.argument(
    'palette_path',
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    nargs=1)
@click.argument(
    'out_dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    nargs=1)
@click.argument(
    'src',
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    nargs=-1,
    required=True)
def locate(palette_path, out_dir, src):
    """Locate flowers in a series of images."""

    colors = pd.read_csv(palette_path)

    with click.progressbar(src) as progressbar:
        for file in progressbar:
            locate_flowers.locate_flowers(file, colors, out_dir)
