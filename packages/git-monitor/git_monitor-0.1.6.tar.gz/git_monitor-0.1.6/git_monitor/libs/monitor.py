import logging
from git import Repo
import sys
import os
from dotenv import dotenv_values

fname_config = ".git_monitor"
logger = logging.getLogger("git_monitor")
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class Monitor:

    def __init__(self, path_proj, name):
        self.repo = Repo(path_proj)
        self.name = name

    @classmethod
    def by_env(cls, name):
        if os.path.isfile(fname_config):
            config = dotenv_values(fname_config)
            if name in config:
                try:
                    monitor = cls(config[name], name)
                    monitor.print_status()
                except Exception as e:
                    logger.info(e)
                return monitor
            else:
                logger.debug(f"package name {name} not in {fname_config}.")
        else:
            logger.debug(f"config file {fname_config} not found.")

    def print_status(self):

        logger.info(f"Project {self.name} status:\n")

        if self.repo.head.is_detached:
            logger.info("On Detached head.")
        else:
            logger.info(f"On branch {self.repo.active_branch}.")

        logger.info(f"Current commit- {self.repo.head.object.hexsha}")
        logger.info(f"Message-\n{self.repo.head.commit.message}")

        if len(self.repo.untracked_files) > 0:
            logger.info("\nuntracked-")
            for file in self.repo.untracked_files:
                logger.info(file)

        diffs = self.repo.index.diff(None)
        if len(diffs) > 0:
            logger.info("\nmodified-")
            for d in diffs:
                logger.info(d.a_path)

        logger.info("\n")
