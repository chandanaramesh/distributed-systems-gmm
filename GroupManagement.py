import os
import sys
import time
import logging

from node import *
from commons.ArgParser import ArgsParser
from commons.Constants import (LOG_FILENAME, LOG_FORMAT, DEBUG_LEVEL)


logger = logging.getLogger(__name__)
ARGS = None


def init(logFileSuffix='generic'):
    global logger
    try:
        if not os.path.exists('./logs'):
            os.makedirs('./logs')
        logging.basicConfig(filename=LOG_FILENAME+'-'+logFileSuffix+'.log', level=DEBUG_LEVEL,
                            format=LOG_FORMAT)
        logger = logging.getLogger(__name__)
    except Exception as e:
        logger.error("Error in the init. Error = {}".format(e))
        exit(1)

def parseArgs():
    global ARGS
    try:
        logger.debug('Parsing arguments')
        argParser = ArgsParser()
        ARGS = argParser.parseArguments()
        if not ARGS:
            logger.error('Error in parsing Arguments')
            exit(1)
        logger.debug(ARGS)
    except Exception as e:
        logger.error("Error in the parse logic. Error = {}".format(e))
        exit(1)


def setup():
	parseArgs()
	init(logFileSuffix=str(ARGS.serverId))


def main():
	setup()
	logger.info('Setup Completed.')
	logger.info('Starting Group Management Node Server with ID {}'.format(ARGS.serverId))
	serverId = int(ARGS.serverId)
	server = Server(serverId)
	server.run()


if __name__ == "__main__":
    main()
