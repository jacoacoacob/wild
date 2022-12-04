

import os
import sys

import dotenv
import requests
import psycopg2

import argparse

from . import retr, queries

dotenv.load_dotenv()

# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")

# parser = argparse.ArgumentParser(
#   prog="FMCdb Bot",
#   description="A robut",
# )

# subparsers = parser.add_subparsers(help="Helllllp")

# parser_1 = subparsers.add_parser("say_hi", help="This command says hello")
# parser_1.add_argument("name")
# parser_1.set_defaults(func=lambda args: print(f"Hello {args.name.capitalize()}!"))

# # parser.add_argument("filename")
# # parser.add_argument("-c", "--count")
# # parser.add_argument("-v", "--verbose", action="store_true")


def run():
  result = queries.select_conveyance_codes()
  print(result)