from argparse import ArgumentParser


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
    parser.set_defaults(func=execute)

  def run(self):
    command = self.parser.parse_args().__dict__
    execute = command.pop("func", None)
    if execute:
      execute(**command)
    else:
      self.parser.print_help()
  