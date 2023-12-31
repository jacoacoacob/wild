
import os
import functools
from typing import Literal

import psycopg2
from psycopg2.extras import RealDictRow, RealDictCursor


def unpack_sql_and_params(*args):
  if type(args[0]) is tuple:
    args, = args
  if len(args) == 1:
    return args[0], []
  if len(args) == 2:
    return args
  raise ValueError("Expected list of 1 or 2 elements")


def get_database_url():
  DATABASE_URL = os.getenv("DATABASE_URL")
  if not DATABASE_URL:
    raise Exception("DATABASE_URL envionment variable not found.")
  return DATABASE_URL


def query(fetch: Literal["one", "all", None] = None, use_dict_cursor = True):
  """
  This decorator will execute SQL text and params returned as a tuple from
  the function it wraps.
  """
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      try:
        conn = psycopg2.connect(get_database_url())
        result = None
        with conn:
          with conn.cursor(cursor_factory=RealDictCursor if use_dict_cursor else None) as cursor:
            sql, params = unpack_sql_and_params(func(*args, **kwargs))
            cursor.execute(sql, params)
            if fetch == "one":
              result = cursor.fetchone()
            if fetch == "all":
              result = cursor.fetchall()
      except Exception as exc:
        print(f"[db::execute] {type(exc).__name__}:", exc)
      finally:
        conn.close()
        if use_dict_cursor:
          if type(result) is RealDictRow:
            return dict(result)
          if type(result) is list:
            return [dict(record) for record in result]
        else:
          return result
    return wrapper
  return decorator


def copy_csv_to_table(file, table):
  try:
    with psycopg2.connect(get_database_url()) as conn:
      with conn.cursor() as cursor:
        cursor.copy_expert(f"COPY {table} FROM STDIN WITH (FORMAT CSV, HEADER)", file)
    conn.close()
    return True
  except Exception as exc:
    conn.close()
    raise exc