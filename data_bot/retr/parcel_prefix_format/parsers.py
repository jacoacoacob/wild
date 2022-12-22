import re

from bs4 import BeautifulSoup, Tag


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
