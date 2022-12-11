"""
This module contains code to download, clean, and copy Real Estate Transfer 
Return data (https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx) to a 
postgres database.
"""
import csv
import os
import re
import zipfile
from datetime import datetime

import dotenv
import requests

from .lib import Job, auto_log, query, copy_csv_to_table

dotenv.load_dotenv()


def retr_date_to_postgres_date(row, column, row_number, logger):
  value = row.get(column)
  if value:
    try:
      d = value.zfill(8)
      d = datetime.strptime(d, "%m%d%Y")
      d = datetime.strftime(d, "%Y-%m-%d")
      return d
    except Exception as exc:
      logger.warn(f"{column} {row_number} {type(exc)} {exc}")
  

def numeric_value(row, column, row_number, logger):
  value = row.get(column)
  if value:
    try:
      return re.sub(r"[^\d\.]", "", value)
    except Exception as exc:
      logger.warn(f"{column} {row_number} {type(exc)} {exc}")


class SyncRetr(Job):
  def __init__(self, job_id=None, verbose=0) -> None:
    super().__init__(job_id, verbose)
    zip_loc, raw_loc, clean_loc = [
      os.path.join(self.artifacts_path, dirname)
      for dirname
      in ("zip", "raw", "clean")
    ]
    if not job_id:
      for location in [zip_loc, raw_loc, clean_loc]:
        os.mkdir(location)
    self.zip_loc = zip_loc
    self.raw_loc = raw_loc
    self.clean_loc = clean_loc

  def execute(self, *args, **kwargs):
    # available_links = self.fetch_available_links()
    # months_to_fetch = self.get_months_to_fetch(available_links)
    # self.download_csv_zip_files(months_to_fetch)
    # self.unpack_csv_data()
    self.clean_csv_data()
    self.copy_cleaned_data_to_database()

  @auto_log
  @query(fetch="all")
  def select_stored_months(self):
    return """
      SELECT
        DISTINCT
          DATE_PART('year', date_recorded)::TEXT ||
          LPAD(DATE_PART('month', date_recorded)::TEXT, 2, '0')
      FROM
        fmc.retr
    """

  @auto_log
  def get_available_months(self, available_links):
    return [
      { "date": re.search(r"(\d+)CSV\.zip", link).group(1), "link": link }
      for link
      in available_links
    ]

  @auto_log
  def get_months_to_fetch(self, available_links):
    available_months = self.get_available_months(available_links)
    stored_months = self.select_stored_months()
    return [
      month
      for month
      in available_months
      if month.get("date") not in stored_months
    ]

  @auto_log
  def fetch_available_links(self):
    """
    Fetch a list of currently available data download URIs
    from https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx
    """
    dor_root_url = "https://www.revenue.wi.gov"
    try:
      response = requests.get(dor_root_url + "/Pages/ERETR/data-home.aspx")
    except Exception as exc:
      self.logger.warn({
        "message": "There was an error fetching download links",
        "type": type(exc).__name__,
        "data": exc
      })
    return [
      dor_root_url + path
      for path 
      in re.findall(r"/SLFReportsHistSales/\w*\.zip", response.text)
    ]

  @auto_log
  def download_csv_zip_files(self, available_months):
    for month in available_months:
      link = month.get("link")
      self.logger.info(f"Fetching {link}")
      response = requests.get(link)
      self.logger.debug({ "response_status_code": response.status_code })
      out_path = os.path.join(self.zip_loc, month.get("date"))
      self.logger.info(f"Saving response to {out_path}.zip")
      with open(out_path + ".zip", "wb") as out:
        out.write(response.content)

  @auto_log
  def unpack_csv_data(self):
    for file_name in os.listdir(self.zip_loc):
      with zipfile.ZipFile(os.path.join(self.zip_loc, file_name)) as zip_ref:
        # So this we coulllld just do `zip_ref.exractall(self.raw_loc)` here
        # but given that we don't really have control over the zip archive origin,
        # I thinnnnk doing what we're doing below (doing some kind of filename 
        # validation before extraction) is what the docs recommend...
        # https://docs.python.org/3/library/zipfile.html?highlight=zipfile#zipfile.ZipFile.extractall
        for archive_member in zip_ref.namelist():
          if archive_member.startswith(file_name[:6]):
            zip_ref.extract(archive_member, self.raw_loc)
          else:
            self.logger.warn(
              f"Detected suspicious zip archive member '{archive_member}'. Extraction from zip arcive not attempted."
            )

  @auto_log
  def clean_csv_data(self):
    for file in os.listdir(self.raw_loc)[:5]:
      try:
        in_file_path = os.path.join(self.raw_loc, file)
        out_file_path = os.path.join(self.clean_loc, file)
        with open(in_file_path, "r", encoding="cp1250", newline="") as in_file:
          with open(out_file_path, "w") as out_file:
            reader = csv.DictReader(in_file)
            writer = csv.DictWriter(
              out_file,
              fieldnames=[name for name in reader.fieldnames if len(name.strip()) > 0]
            )
            self.logger.info(f"Writing {out_file.name}")
            writer.writeheader()
            for index, row in enumerate(reader):
              writer.writerow({
                **{
                  col: row[col].strip()
                  for col
                  in row if len(col) > 0 
                },
                **{
                  col: numeric_value(row, col, index + 1, self.logger)
                  for col
                  in [
                    "MultiGrantors"
                  ]
                },
                **{
                  col: retr_date_to_postgres_date(row, col, index + 1, self.logger)
                  for col
                  in [
                    "CertificationDate",
                    "DateConveyed",
                    "DateRecorded",
                    "DeedDate",
                    "GranteeCertificationDate",
                  ]
                }
              })
            self.logger.info(f"Write complete")
      except Exception as exc:
        self.logger.warn(f"{type(exc)} {exc}")

  @auto_log
  def copy_cleaned_data_to_database(self):
    for file_name in os.listdir(self.clean_loc)[:5]:
      try:
        # cp1250 is encoding used by Windows https://docs.python.org/3.10/library/codecs.html
        with open(os.path.join(self.clean_loc, file_name), "r", encoding="cp1250") as file:
          self.logger.info(f"Copying {file_name} to database")
          copy_csv_to_table(file, "fmc.retr")
          self.logger.info(f"Copy complete")
      except Exception as exc:
        self.logger.warn(f"{type(exc)} {exc}")