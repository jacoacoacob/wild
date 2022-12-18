"""
Generate a postgres INSERT statement to seed wild.retr_municipality_parcel_format
"""
import re
import json
from typing import List

import requests
from bs4 import BeautifulSoup, Tag


def count_leading_zeros(value: str):
  return len(re.search(r"(^0*)", value).group())


def fetch_parcel_prefix_format_html():
  # # PROD
  # response = requests.get("https://www.revenue.wi.gov/Pages/UST/parcels.aspx")
  # return response.text
  # DEV
  with open("sandbox_parcel_prefix_format.html") as html:
    return html.read()


def get_panel_tags(soup: BeautifulSoup):
  return soup.find_all("div", class_="panel")


def get_county_name(panel: Tag):
  panel_title = panel.find("h3", class_="panel-title")
  if not panel_title:
    return ""
  text = panel_title.text
  # Remove non-word characters (like \u200b – ZERO WIDTH SPACE)
  text = re.sub(r"\W", " ", text)
  text = re.sub(r"\s{2,}", "", text)
  text = text.upper().strip()
  return text


def get_municipality_name(tr: Tag):
  td, _, _ = tr.find_all("td")
  text = td.text.upper()
  text = re.sub(r"\t", " ", text)
  text = re.sub(r"\s{2,}", " ", text)
  return text


def count_leading_zeros(value: str):
  return len(re.search(r"(^0*)", value).group())


def get_municipality_prefix(tr: Tag):
  parts = []
  _, td, _ = tr.find_all("td")
  if td:
    for part in re.split(r"\s*or\s*|,", td.text):
      range_match = re.match(r"([\w-]+)\s+(through|thru|-)\s+([\w-]+)", part)
      if range_match:
        start_str, _, end_str = range_match.groups()
        suffix = re.search(r"[^\d]+$", start_str)
        suffix = suffix.group() if suffix else ""
        max_len = max(
          len(start_str) - count_leading_zeros(start_str),
          len(end_str) - count_leading_zeros(end_str),
        )
        try:
          start_num = int(re.sub(r"[^\d]", "", start_str))
          end_num = int(re.sub(r"[^\d]", "", end_str))
          for num in range(start_num, end_num + 1):
            value = f"{num}{suffix}" if suffix else f"{num}"
            parts.append(value.zfill(max_len))
        except Exception as exc:
          print(f"[get_municipality_prefix] {type(exc).__name__}", exc)
      else:
        parts += [x.strip() for x in part.split(" ") if len(x.strip())]
  return parts


def get_municipalities(panel: Tag):
  rv = []
  for tr in panel.select("tbody tr"):
    rv.append({
      "name": get_municipality_name(tr),
      "prefix": get_municipality_prefix(tr),
    })
  return rv


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
  with open("sandbox_parcel_format.sql", "w") as out:
    out.write(sql)


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
          "MARATHON": [
            ("BROKAW, VILLAGE OF", ["106-"])
          ],
          "OUTAGAMIE": [
            ("GREENVILLE, TOWN OF", ["110"]),
          ],
        },
        "tvc_replace": {
          "CHIPPEWA": [
            ("LAKE HOLCOMBE,TOWN OF", "LAKE HOLCOMBE, TOWN OF"),
          ],
          "DOOR": [
            ("JACKSONPOST, TOWN OF", "JACKSONPORT, TOWN OF"),
          ]
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

