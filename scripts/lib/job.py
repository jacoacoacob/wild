import os
import logging
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

JOB_ARTIFACTS_ROOT = os.getenv("JOB_ARTIFACTS_ROOT", "jobs")

JOB_VERBOSITY_TO_LOG_LEVEL = [logging.WARNING, logging.INFO, logging.DEBUG]


class Job:
  def __init__(self, verbose=0) -> None:
    self.job_id = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    self.artifacts_path = os.path.abspath(
      os.path.join(JOB_ARTIFACTS_ROOT, self.job_id)
    )
    os.makedirs(self.artifacts_path)
    self.logger = logging.getLogger(self.job_id)
    self.logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
      "%(levelname)s %(asctime)s [%(module)s::%(funcName)s] %(message)s",
      datefmt="%Y-%m-%d %H:%M:%S"
    )
    ch = logging.StreamHandler()
    ch.setLevel(JOB_VERBOSITY_TO_LOG_LEVEL[verbose])
    ch.setFormatter(formatter)
    fh = logging.FileHandler(os.path.join(self.artifacts_path, "debug.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    self.logger.addHandler(ch)
    self.logger.addHandler(fh)
