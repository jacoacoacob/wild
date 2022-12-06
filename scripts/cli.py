from . import queries, retr
from .lib import Cli


def ping(*args, **kwargs):
  print(queries.ping(*args, **kwargs))


cli = Cli("FMC-bot")

cli.add_command(
  "ping",
  help_text="Select the current time from the database",
  execute=ping,
)

cli.add_command(
  "sync_retr",
  execute=retr.sync_retr,
  arguments=[
    (["--verbose"], {
      "default": 0,
      "type": int,
      "choices": [1,2],
      "help": """By default, all messages level WARNING and above will be 
                logged stdout. Choose 1 to log messages level INFO and above 
                to stdout. Choose 2 to log all messages to stdout.""",
    })
  ]
)
