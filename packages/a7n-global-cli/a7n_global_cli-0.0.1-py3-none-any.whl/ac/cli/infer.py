import click

from xxxai.cli.util import click_group


@click_group()
def infer():
    pass


@infer.command()
@click.option("--name", "-n", type=str, help="Name of the inference to run.")
@click.option("--model", "-m", type=str, help="Model spec of the inference.")
@click.option("--file", "-f", "path", type=str, help="Path to the specific a file to run.")
@click.pass_context
def run(ctx, name, model, path):
    print("test run", name, model, path)
    pass

@infer.command()
@click.option("--name", "-n", help="Name of the inference to delete",)
def remove(name):
    print("test remove", name)
    pass

@infer.command()
@click.option("--name", "-n", help="Name of the inference", required=True)
def push(name):
    """
    Push a photon to the workspace.
    """
    print("test push", name)
    pass


def add_command(cli_group):
    cli_group.add_command(infer)
