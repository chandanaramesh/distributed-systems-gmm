"""     
    Class to parse CLI arguments
"""

import logging
import argparse
# from Commons.Utils import Utils

logger = logging.getLogger(__name__)


class ArgsParser:
    def __init__(self):
        logger.debug('Init ArgsParser')

    def parseArguments(self):
        logger.debug('Parsing the arguments')
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--serverId", "-sid", help="The Server ID", required=True, type=int)
        args = parser.parse_args()

        if self._validateArgs(args):
            return args
        else:
            return None

    def _validateArgs(self, args):
        return True
