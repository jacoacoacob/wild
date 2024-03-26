"""
This module contains code to download, clean, and copy Real Estate Transfer 
Return data (https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx) to a 
postgres database.
"""
import os
import typing

from ..lib import Job, stage
from . import utils as retr_utils
  
RERUN_STAGES = typing.List[typing.Literal[
  "download_csv_zip_files",
  "unpack_csv_data",
  "clean_csv_data",
  "copy_cleaned_data_to_database",
]]

class SyncRetr(Job):
  def __init__(
    self,
    rerun_job = None,
    verbose = 0,
    rerun_stages: RERUN_STAGES = None
  ) -> None:
    super().__init__(rerun_job, verbose)
    zip_loc, raw_loc, clean_loc = [
      os.path.join(self.artifacts_path, dirname)
      for dirname
      in ("zip", "raw", "clean")
    ]
    if not rerun_job:
      for location in (zip_loc, raw_loc, clean_loc):
        os.mkdir(location)
    self.rerun_job = rerun_job
    self.rerun_stages = rerun_stages
    self.zip_loc = zip_loc
    self.raw_loc = raw_loc
    self.clean_loc = clean_loc

  def execute(self, *args, **kwargs):
    if self.rerun_job:
      if "download_csv_zip_files" in self.rerun_stages:
        self.download_csv_zip_files()
      if "unpack_csv_data" in self.rerun_stages:
        self.unpack_csv_data()
      if "clean_csv_data" in self.rerun_stages:
        self.clean_csv_data()
      if "copy_cleaned_data_to_database" in self.rerun_stages:
        self.copy_cleaned_data_to_database()
    else:
      self.download_csv_zip_files()
      self.unpack_csv_data()
      self.clean_csv_data()
      self.copy_cleaned_data_to_database()

  @stage
  def download_csv_zip_files(self):
    urls = retr_utils.get_urls_to_fetch(self)
    for index, url in enumerate(urls):
      self.logger.info(f"{index + 1} of {len(urls)}")
      retr_utils.download_retr_csv_zip(self, url, self.zip_loc)

  @stage
  def unpack_csv_data(self):
    filenames = os.listdir(self.zip_loc)
    for index, filename in enumerate(filenames):
      self.logger.info(f"{index + 1} of {len(filenames)}")
      retr_utils.unpack_retr_csv(
        self,
        filename,
        zip_loc=self.zip_loc,
        unpack_loc=self.raw_loc
      )

  @stage
  def clean_csv_data(self):
    filenames = os.listdir(self.raw_loc)
    for index, filename in enumerate(filenames):
      self.logger.info(f"{index + 1} of {len(filenames)}")
      retr_utils.clean_retr_csv(self, filename, self.raw_loc, self.clean_loc)

  @stage
  def copy_cleaned_data_to_database(self):
    filenames = os.listdir(self.clean_loc)
    for index, filename in enumerate(filenames):
      self.logger.info(f"{index + 1} of {len(filenames)}")
      retr_utils.copy_retr_csv_to_database_table(
        self,
        self.clean_loc,
        filename
      )
