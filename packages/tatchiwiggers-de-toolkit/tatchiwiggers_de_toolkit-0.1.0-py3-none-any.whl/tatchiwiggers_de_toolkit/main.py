import click
from de_toolkit.vm import start, stop, connect

@click.group()
def cli():
    cli.add_command(start)
    cli.add_command(stop)
    cli.add_command(connect)


if __name__ == '__main__':
    cli()
