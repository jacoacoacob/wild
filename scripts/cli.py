import click

from . import retr


@click.group()
def cli():
  pass


@cli.command()
@click.option(
  "--verbose",
  default=0,
  type=int,
  help="""By default, all messages level WARNING and above will be 
          logged stdout. Choose 1 to log messages level INFO and above 
          to stdout. Choose 2 to log all messages to stdout."""
)
@click.option("--job-id")
def sync_retr(verbose, job_id):
  job = retr.SyncRetr(verbose=verbose, job_id=job_id)
  job.execute()
