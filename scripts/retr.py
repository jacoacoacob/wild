"""
This module contains code to download, clean, and copy Real Estate Transfer 
Return data (https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx) to a 
postgres database.
"""
import re
import json
from typing import List

import dotenv
import requests

from . import queries
from .lib import Job

dotenv.load_dotenv()


class SyncRetr(Job):
  def execute(self, *args, **kwargs):
    self.logger.info("Begin")
    available_links = self.fetch_available_links()
    links_to_fetch = self.get_links_to_fetch(available_links)


  def get_links_to_fetch(self, available_links):
    self.logger.info("Computing available months")
    self.logger.debug({ "available_links": available_links })
    available_months = [
      { "month": re.search(r"(\d+)CSV\.zip", link).group(1), "link": link }
      for link
      in available_links
    ]
    self.logger.info("Computed available months")
    self.logger.debug({ "available_months": available_months })
    self.logger.info("Selecting recorded months")
    stored_months = queries.select_recorded_months()
    self.logger.info("Selected recorded months")
    self.logger.debug({ "stored_months": stored_months })
    self.logger.info("Computing links to fetch")
    links_to_fetch = [
      month.get("link")
      for month
      in available_months
      if month.get("month") not in stored_months
    ]
    self.logger.info("Computed links to fetch")
    self.logger.debug({ "links_to_fetch": links_to_fetch })
    return links_to_fetch


  def fetch_available_links(self):
    """
    Fetch a list of currently available data download URIs
    from https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx
    """
    dor_root_url = "https://www.revenue.wi.gov"
    try:
      self.logger.info("Fetching data download links.")
      response = requests.get(dor_root_url + "/Pages/ERETR/data-home.aspx")
    except Exception as exc:
      self.logger.warn({
        "message": "There was an error fetching download links",
        "type": type(exc).__name__,
        "data": exc
      })
    data = [
      dor_root_url + path
      for path 
      in re.findall(r"/SLFReportsHistSales/\w*\.zip", response.text)
    ]
    self.logger.info("Fetched data download links.")
    self.logger.debug({ "data": data })
    return data

