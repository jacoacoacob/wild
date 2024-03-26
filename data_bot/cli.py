import re

import click
import dotenv

dotenv.load_dotenv()

from .retr import SyncRetr, GeocodeRetr


@click.group()
def cli():
  pass


@cli.group()
def retr():
  """
  Real Estate Transfer Return (RETR) data commands.
  """


VERBOSE_OPTION_KWARGS = {
  "default": 0,
  "type": int,
  "help": """By default, all messages level WARNING and above will be 
          logged to stdout. Choose 1 to log messages level INFO and above
          to stdout. Choose 2 to log all messages level DEBUG and above
          (all messages) to stdout."""
}


@retr.command()
@click.option("-v", "--verbose", **VERBOSE_OPTION_KWARGS)
@click.option(
  "-r",
  "--rerun-job",
  type=str,
  help="""Provide the ID for a previously executed job to execute it again.
          You need to specify which stages to execute by providing  or none will be executed"""
)
@click.option("-s", "--rerun-stage", multiple=True)
def sync(verbose, rerun_job, rerun_stage):
  """
  Synchronize the database with available RETR data.

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
  job = SyncRetr(
    verbose=verbose,
    rerun_job=rerun_job,
    rerun_stages=rerun_stage
  )
  job.execute()


def validate_month(ctx, param, value):
  if re.match(r"^\d{6}$", value):
    return value
  raise click.BadArgumentUsage(
    f"Format of {param.name.upper()} must be YYYYMM (e.g. 202205)",
    ctx
  )

@retr.command()
@click.option(
  "-o",
  "--output",
  type=click.Path(exists=False, resolve_path=True),
  help="""Filepath to where a directory for storing artifacts should be created.
          If none is provided, artifacts will be stored at 'os.getcwd()/month_{MONTH}'"""
)
@click.option("-v", "--verbose", **VERBOSE_OPTION_KWARGS)
@click.argument("month", callback=validate_month)
def download_month(output, verbose, month):
  """
  Download data for MONTH

  MONTH should be formatted as YYYYMM (e.g. 202007 would download all Real 
  Estate Transfer Return data recorded in the month of July in the year 2020).
  """
  print(output, verbose, month)


@retr.command()
@click.option("-v", "--verbose", **VERBOSE_OPTION_KWARGS)
def copy_csv_to_db(vervise):
  """
  Copy a CSV file located at FILEPATH to the database.

  The CSV file columns and data types must conform to the constraints of the Postgres table `wild.retr`.
  """


@retr.command()
@click.option("-v", "--verbose", **VERBOSE_OPTION_KWARGS)
def geocode(verbose):
  job = GeocodeRetr(verbose=verbose)
  job.execute()