# -*- coding: utf-8 -*-

"""
Entry module for pharm-drone
"""

import click

from src import color_palette


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
