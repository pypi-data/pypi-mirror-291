import click
from ac.version import __version__

from ac.cli import deployment
from ac.cli import dataset
from ac.cli.util import click_group

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.version_option(__version__, "-v", "--version")
@click_group(context_settings=CONTEXT_SETTINGS)
def main():
    pass


deployment.add_command(main)
dataset.add_command(main)

if __name__ == "__main__":
    main()