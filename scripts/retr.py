"""
This module contains code to download, clean, and copy Real Estate Transfer 
Return data (https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx) to a 
postgres database.
"""
import re
import os
import csv
import zipfile

import dotenv
import requests

from .lib import Job, auto_log, query

dotenv.load_dotenv()

ENCODINGS = [
  "ascii",
  "big5",
  "big5hkscs",
  "cp037",
  "cp273",
  "cp424",
  "cp437",
  "cp500",
  "cp720",
  "cp737",
  "cp775",
  "cp850",
  "cp852",
  "cp855",
  "cp856",
  "cp857",
  "cp858",
  "cp860",
  "cp861",
  "cp862",
  "cp863",
  "cp864",
  "cp865",
  "cp866",
  "cp869",
  "cp874",
  "cp875",
  "cp932",
  "cp949",
  "cp950",
  "cp1006",
  "cp1026",
  "cp1125",
  "cp1040",
  "cp1250",
  "cp1251",
  "cp1252",
  "cp1253",
  "cp1254",
  "cp1255",
  "cp1256",
  "cp1257",
  "cp1258",
  "latin_1",
  "iso8859_15",
  "mac_roman",
  "utf_32",
  "utf_32_be",
  "utf_32_le",
  "utf_16",
  "utf_16_be",
  "utf_16_le",
  "utf_7",
  "utf_8",
  "utf_8_sig",
]


class SyncRetr(Job):
  def execute(self, *args, **kwargs):
    # available_links = self.fetch_available_links()
    # months_to_fetch = self.get_months_to_fetch(available_links)
    months_to_fetch = [
      {
        'date': '202201',
        'link': 'https://www.revenue.wi.gov/SLFReportsHistSales/202201CSV.zip'
      }
    ]
    self.download_csv_zip_files(months_to_fetch)

  @auto_log
  @query(fetch="all")
  def select_stored_months(self):
    return "SELECT DISTINCT date_recorded FROM fmc.retr"

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
      link = month.get("links")
      self.logger.debug(f"Fetching {link}")
      response = requests.get(link)
      out_path = os.path.join(self.artifacts_path, month.get("date"))
      self.logger.debug(f"Opening {out_path}.zip")
      with open(out_path + ".zip", "wb") as zip_file:
        self.logger.debug(f"Writing {out_path}.zip")
        zip_file.write(response.content)

  @auto_log
  def unzip_csv_zip_files(self):
    pass



