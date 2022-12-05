from . import queries, lib
from .lib import Cli


cli = Cli("FMC-bot")

selet_now = cli.add_command(
  "select_now",
  help_text="Select the current time from the database",
  execute=queries.select_now,
)

cli.add_command(
  "select_conveyance_codes",
  help_text="Select all conveyance code rows",
  execute=queries.select_conveyance_codes
)
