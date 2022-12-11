import os
import logging
import json
import functools
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

JOB_ARTIFACTS_ROOT = os.getenv("JOB_ARTIFACTS_ROOT", "jobs")

JOB_VERBOSITY_TO_LOG_LEVEL = [logging.WARNING, logging.INFO, logging.DEBUG]


auto_log_formatter = logging.Formatter(
  "%(levelname)s %(asctime)s %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S"
)

job_log_formatter = logging.Formatter(
  "%(levelname)s %(asctime)s [%(module)s::%(funcName)s] %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S"
)

def set_formatter(logger, formatter):
  for handler in logger.handlers:
    handler.setFormatter(formatter)


def auto_log(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    if isinstance(args[0], Job):
      job = args[0]
      set_formatter(job.logger, auto_log_formatter)
      job.logger.info(f"[auto_log] Starting {func.__name__}")
      job.logger.debug(f"[auto_log] {dict(func_name=func.__name__, args=args, kwargs=kwargs)}")
      set_formatter(job.logger, job_log_formatter)
      result = func(*args, **kwargs)
      set_formatter(job.logger, auto_log_formatter)
      job.logger.info(f"[auto_log] Finished {func.__name__}")
      job.logger.debug(f"[auto_log] {dict(func_name=func.__name__, result=result)}")
      set_formatter(job.logger, job_log_formatter)
      return result
  return wrapper
    

class Job:
  def __init__(self, verbose=0) -> None:
    self.job_id = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    self.artifacts_path = os.path.abspath(
      os.path.join(JOB_ARTIFACTS_ROOT, self.job_id)
    )
    os.makedirs(self.artifacts_path)
    self.logger = logging.getLogger(self.job_id)
    self.logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(JOB_VERBOSITY_TO_LOG_LEVEL[verbose])
    ch.setFormatter(job_log_formatter)
    fh = logging.FileHandler(os.path.join(self.artifacts_path, "debug.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(job_log_formatter)
    self.logger.addHandler(ch)
    self.logger.addHandler(fh)

  def execute(self, *args, **kwargs):
    raise NotImplemented