
import os
import functools
from argparse import ArgumentParser
from typing import Literal

import dotenv
import psycopg2
from psycopg2.extras import RealDictRow, RealDictCursor

dotenv.load_dotenv()


def unpack_sql_and_params(*args):
  if type(args[0]) is tuple:
    args, = args
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
      try:
        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
          raise Exception("DATABASE_URL envionment variable not found.")
        conn = psycopg2.connect(DATABASE_URL)
        result = None
        with conn:
          with conn.cursor(cursor_factory=RealDictCursor) as cursor:
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
        if type(result) is RealDictRow:
          return dict(result)
        if type(result) is list:
          return [dict(record) for record in result]
    return wrapper
  return decorator


class Cli:
  def __init__(self, name="", commands_description=""):
    self.parser = ArgumentParser(name)
    self.subparsers = self.parser.add_subparsers(
      title="Commands",
      description=commands_description
    )

  def add_command(self, name, help_text="", execute=None, arguments=[]):
    parser = self.subparsers.add_parser(
      name,
      description=help_text,
      help=help_text
    )
    for args in arguments:
      args, kwargs = args
      parser.add_argument(*args, **kwargs)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.set_defaults(func=execute)
    return parser

  def run(self):
    command = self.parser.parse_args().__dict__
    execute = command.pop("func", None)
    if execute:
      result = execute(**command)
      if command.get("verbose"):
        print(result)
    else:
      self.parser.print_help()
  
