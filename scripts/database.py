import os
import functools
from typing import Literal

import psycopg2


def unpack_sql_and_params(*args):
  if type(args[0]) is tuple:
    args, = args
  # print(args)
  # if type(args) is tuple:
  #   args, = args
  if len(args) == 1:
    return args[0], []
  if len(args) == 2:
    return args
  raise ValueError("Expected list of 1 or 2 elements")


def execute(fetch: Literal["one", "all", None] = None):
  """
  This decorator will execute SQL text and params returned as a tuple from
  the function it wraps.
  """
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      DATABASE_URL = os.getenv("DATABASE_URL")
      if not DATABASE_URL:
        raise Exception("DATABASE_URL envionment variable not found.")
      conn = psycopg2.connect(DATABASE_URL)
      result = None
      try:
        with conn:
          with conn.cursor() as cursor:
            sql, params = unpack_sql_and_params(func(*args, **kwargs))
            cursor.execute(sql, params)
            if fetch == "one":
              result = cursor.fetchone()
            if fetch == "all":
              result = cursor.fetchall()
      except Exception as exc:
        print(f"[database::transaction] {type(exc).__name__}:", exc)
      finally:
        conn.close()
        return result
    return wrapper
  return decorator
