import click

from . import queries, retr


@click.group()
def cli():
  pass


@cli.command()
def ping(*args, **kwargs):
  print(queries.ping(*args, **kwargs))


@cli.command()
@click.option(
  "--verbose",
  default=0,
  type=int,
  help="""By default, all messages level WARNING and above will be 
          logged stdout. Choose 1 to log messages level INFO and above 
          to stdout. Choose 2 to log all messages to stdout."""
)
def sync_retr(verbose):
  job = retr.SyncRetr(verbose)
  job.execute()

