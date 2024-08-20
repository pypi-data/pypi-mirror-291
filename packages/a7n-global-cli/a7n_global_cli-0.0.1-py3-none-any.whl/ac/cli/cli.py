import click
from xxxai.version import __version__

from . import deployment
from . import infer
from .util import click_group

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.version_option(__version__, "-v", "--version")
@click_group(context_settings=CONTEXT_SETTINGS)
def main():
    pass


deployment.add_command(main)
infer.add_command(main)
