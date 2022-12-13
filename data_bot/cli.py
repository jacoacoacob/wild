import click

from . import retr


@click.group()
def cli():
  pass


@cli.group()
def retr():
  """
  Commands for interacting with Real Estate Transaction Return (RETR) data
  """


@retr.command()
@click.option(
  "--verbose",
  default=0,
  type=int,
  help="""By default, all messages level WARNING and above will be 
          logged to stdout. Choose 1 to log messages level INFO and above 
          to stdout. Choose 2 to log all messages level DEBUG and above
          (all messages) to stdout."""
)
def sync(verbose, job_id):
  """
  This command checks the months for which RETR data is available and
  downloads, cleans, and copies into the database the data for those months
  which aren't already stored in the database.

  It will use the value of an environment variable named JOB_ARTIFACTS_ROOT to
  determine where to output artifacts like log files, downloaded .zip archives,
  raw .csv files extracted from those archives, and cleaned .csv files with 
  values formatted for our postgres database.
  
  If JOB_ARTIFACTS_ROOT is not defined, artifacts will use 'jobs'. Artifacts 
  will be output to the path JOB_ARTIFACTS_ROOT/<job_id> where `<job_id>` is
  a the result of `datetime.utcnow().strftime("%Y%m%d%H%M%S")`.
  """
  job = retr.SyncRetr(verbose=verbose, job_id=job_id)
  job.execute()
