import click
from ..lib import bchtracer

@click.group()
@click.version_option(version='0.1.0', message=click.style('bchtracer Version: 0.1.0'))
@click.pass_context
def main (ctx) -> None:
    """bchtracer."""
    ctx.obj = bchtracer.create_context()
