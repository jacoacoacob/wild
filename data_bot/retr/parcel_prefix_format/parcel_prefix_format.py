"""
Generate a postgres INSERT statement to seed wild.retr_municipality_parcel_format
"""
import re
import json
from typing import List

import requests
from bs4 import BeautifulSoup, Tag

from .parsers import get_county_name, get_municipalities, get_panel_tags
from .transformers import Muni, muni_add, tvc_replace, tvc_replace_many


def fetch_parcel_prefix_format_html():
  # # PROD
  # response = requests.get("https://www.revenue.wi.gov/Pages/UST/parcels.aspx")
  # return response.text
  # DEV
  with open("sandbox_parcel_prefix_format.html") as html:
    return html.read()


def get_sql_values(municipalities):
  rv = []
  viewed = set()
  for muni in sorted(municipalities, key=lambda muni: muni["county"]):
    county_name = muni.get("county")
    muni_name = muni.get("name")
    muni_prefixes = muni.get("prefix")
    if (muni_name, county_name) not in viewed:
      rv.append(
        f"('{muni_name}', '{county_name}', ARRAY{muni_prefixes})"
      )
    viewed.add((muni_name, county_name))
  return rv


def write_sql(sql):
  tmpl_path = "sandbox_4-table-parcel-prefix-format.template.txt"
  out_path = "schema/deploy/4-create-table-retr-municipality-parcel-format.sql"
  with open(tmpl_path) as tmpl_file:
    template = tmpl_file.read()
    template = template.replace("%insert%", sql)
    with open(out_path, "w") as out_file:
      out_file.write(template)


def patch(county_name: str, municipalities: List[dict], config: dict):
  muni_add = config.get("muni_add", {})
  tvc_replace = config.get("tvc_replace", {})
  tvc_variant = config.get("tvc_variant", {})
  if muni_add.get(county_name):
    for muni_name, muni_prefix in muni_add.get(county_name):
      municipalities.append({
        "name": muni_name,
        "county": county_name,
        "prefix": muni_prefix,
      })
  if tvc_replace.get(county_name):
    for old, new in tvc_replace.get(county_name, []):
      municipalities = [
        { **muni, "name": new } if muni.get("name") == old else muni
        for muni
        in municipalities
      ]
  if tvc_variant.get(county_name):
    muni_names = [x.get("name") for x in municipalities if x]
    for orig_tvc, variant_tvc in tvc_variant.get(county_name, []):
      try:
        index_of_orig = muni_names.index(orig_tvc)
        if index_of_orig is not None:
          muni = municipalities[index_of_orig]
          municipalities.append({ **muni, "name": variant_tvc })
      except:
        pass
  for orig_county, variant_county in config.get("county_variant", []):
    if orig_county == county_name:
      return patch(variant_county, municipalities, {}) + [
        { **muni, "county": county_name }
        for muni
        in municipalities
      ]
  return [
    { **muni, "county": county_name }
    for muni
    in municipalities
  ]


def get_parcel_prefix_format():
  parcel_prefix_format_html = fetch_parcel_prefix_format_html()
  soup = BeautifulSoup(parcel_prefix_format_html, "html.parser")
  panel_tags: List[Tag] = get_panel_tags(soup)
  sql = """
INSERT INTO wild.retr_municipality_parcel_format
  (tvc_name, county_name, prefix)
VALUES\n  """
  municipalities = []
  for panel in panel_tags:
    municipalities += patch(
      get_county_name(panel),
      get_municipalities(panel),
      {
        "muni_add": {
          "BROWN": [
            ("DE PERE, CITY OF", ["ED-", "WD-"])
          ],
          "KENOSHA": [
            ("SALEM, TOWN OF", ["65-4-120-", "66-4-120-", "67-4-120-"]),
            ("SILVER LAKE, VILLAGE OF", ["75-4-120-"]),
          ],
          "MARATHON": [
            ("BROKAW, VILLAGE OF", ["106-"])
          ],
          "OUTAGAMIE": [
            ("GREENVILLE, TOWN OF", ["110"]),
          ],
          # "OZAUKEE": [
          #   ()
          # ],
          "WAUKESHA": [
            ("WAUKESHA, TOWN OF", ["WAKT"]),
          ],
        },
        "tvc_replace": {
          "CHIPPEWA": [
            ("LAKE HOLCOMBE,TOWN OF", "LAKE HOLCOMBE, TOWN OF"),
          ],
          "DOOR": [
            ("JACKSONPOST, TOWN OF", "JACKSONPORT, TOWN OF"),
          ],
          "MARINETTE": [
            ("NAGARA, CITY OF", "NIAGARA, CITY OF"),
          ],
        },
        "tvc_variant": {
          "FOND DU LAC": [
            ("NORTH FOND DU LAC, VILLAGE OF", "NORTH FOND DU LAC, VILLAGE"),
          ],
          "KENOSHA": [
            ("PLEASANT PRAIRIE, VILLAGE OF", "PLEASANT PRAIRIE, VILLAGE"),
          ],
          "WAUKESHA": [
            ("MENOMONEE FALLS, VILLAGE OF", "MENOMONEE FALLS, VILLAGE O"),
          ],
        },
        "county_variant": [
          ("SAINT CROIX", "ST. CROIX")
        ]
      }
    )
  sql += ",\n  ".join(get_sql_values(municipalities)) + ";"
  write_sql(sql)

