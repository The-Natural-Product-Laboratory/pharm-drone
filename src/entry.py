import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--output', '-o', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def locate(input, output):
    """Locates flowers present in an image."""
    click.echo("Hello world!")


@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True, ))
@click.option('--output', '-o', type=click.Path(exists=True))
def palette(input, output):
    """Generates a color palette from a collection of images."""
    click.echo("Hello world!")
