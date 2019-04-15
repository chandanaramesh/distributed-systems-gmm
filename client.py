import os
import time
import uuid
import json
import socket
import pickle
import logging
import argparse

from KThread import *
#from messages.config_messages import ConfigChange
from messages.request_redirect import Request

SHOW_STATE_TIMEOUT = 5
CHANGE_CONFIG_TIMEOUT = 20
CRUD_TIMEOUT = 20

INTERACTIVE_MODE = True
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

SERVER_IDS_AVAILABLE = "ID of the server [1-%d]"

logger = logging.getLogger(__name__)


class ClientRequestor(object):
    cnt = 0

    def __init__(self):
        ClientRequestor.cnt = ClientRequestor.cnt + 1
        self.id = ClientRequestor.cnt
        self.num_of_reply = 0

    def showState(self, port):
        logger.info('Making request to show')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = Request('show')
        s.sendto(pickle.dumps(msg), ("", port))
        while 1:
            try:
                reply, addr = s.recvfrom(1024)
                if reply != '':
                    print reply
                    break
                else:
                    print 'Did not receive reply from server within the timeout time of ' + str(SHOW_STATE_TIMEOUT)
            except Exception as e:
                print 'Connection refused'

    def addProcess(self, port, command, uuid):
        logger.info('Making request to add Process')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = Request(command, uuid)
        s.sendto(pickle.dumps(msg), ("", port))
        while 1:
            try:
                reply, addr = s.recvfrom(1024)
                if reply != '':
                    print reply
                    break
                else:
                    print 'Did not receive reply from server within the timeout time of ' + str(CRUD_TIMEOUT)
            except Exception as e:
                print 'Connection refused'

def init():
    setupLogging()
    logger.info('Client Setup started')
    ports, num_ports = readConfig()
    logger.info('Number of nodes = {}'.format(str(num_ports)))
    args = setupClient(num_ports)
    return args, ports, num_ports


def readConfig():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        ports = config['AddressBook']
        num_ports = len(ports)
        return ports, num_ports
    except Exception as e:
        raise e
        print 'Could not read the configuration file to get info about the nodes. Existing application'
        exit()


def setupLogging():
    global logger
    if not os.path.exists('./logs'):
        os.makedirs('./logs')
    logging.basicConfig(filename='./logs/clientLogs.log', level=LOG_LEVEL,
                        format=LOG_FORMAT)
    logger = logging.getLogger(__name__)


def setupClient(num_ports):
    global SERVER_IDS_AVAILABLE
    global INTERACTIVE_MODE
    SERVER_IDS_AVAILABLE = SERVER_IDS_AVAILABLE % num_ports
    args = parseArguments()
    logger.debug('Non Interactive Args = {}'.format(args))
    INTERACTIVE_MODE = args.no_interactive
    return args


def parseArguments():
    logger.debug('Parsing the arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-interactive", "-ni", help="Disable Interative Mode", required=False, default=False, action='store_true')
    parser.add_argument(
        "--debug", "-d", help="Enable Debug Mode", required=False, action='store_true')
    parser.add_argument(
        "--server", "-s", help=SERVER_IDS_AVAILABLE, required=False, type=int)
    parser.add_argument(
        "--command", "-c", help="Any of the allowed command [show | addProcess <groupId> <processId> "
                                "| deleteProcess <groupId> <processId> | deleteGroup <GroupId>]", required=False, nargs='+')
    args = parser.parse_args()
    return args


def showHandler(clientRequest, ports, serverId):
    requestThread = KThread(target=clientRequest.showState, args=(ports[serverId - 1],))
    timeout = SHOW_STATE_TIMEOUT
    return timeout, requestThread

def addProcessHandler(clientRequest, ports, serverId, command, uuid):
    requestThread = KThread(target=clientRequest.addProcess, args=(ports[serverId - 1],command, uuid))
    timeout = CRUD_TIMEOUT
    return timeout, requestThread

def main():
    args, ports, num_ports = init()
    if not INTERACTIVE_MODE:
        while True:
            clientRequestor = ClientRequestor()
            serverId = input('Which node do you want to connect to? [1-%d]: ' % num_ports)
            print 'Accepted commands are [show | exit]'
            request = raw_input('How can we help you? -- ')
            if request == 'show':
                print 'Delegating to show handler'
                timeout, requestThread = showHandler(clientRequestor, ports, serverId)
            elif request == 'exit':
                print 'Thanks for using the Group Management Client! See you next time'
                exit(0)
            else:
                print 'Default Condition Encountered. Exiting'
                exit(0)
            start_time = time.time()
            requestThread.start()
            while time.time() - start_time < timeout:
                if not requestThread.is_alive():
                    break
            if requestThread.is_alive():
                print 'Timeout! Try again'
                requestThread.kill()
    else:
        command = ' '.join(args.command)
        logger.info('Server = {}, command = {}'.format(str(args.server), command))
        clientRequestor = ClientRequestor()
        serverId = args.server
        request = ' '.join(args.command)
        if 'show' in request:
            logger.info('Delegating to show handler')
            timeout, requestThread = showHandler(clientRequestor, ports, serverId)
        elif 'addProcess' in request:
            uuid_ = uuid.uuid1()
            logger.info('Adding a process based on the command {}'.format(command))
            timeout, requestThread = addProcessHandler(clientRequestor, ports, serverId, command, uuid_)
        elif request == 'exit':
            print 'Thanks for using the Group Management Client! See you next time'
            exit(0)
        else:
            print 'Default Condition Encountered. Exiting'
            exit(0)
        start_time = time.time()
        requestThread.start()
        while time.time() - start_time < timeout:
            if not requestThread.is_alive():
                break
        if requestThread.is_alive():
            requestThread.kill()
            exit(0)
        else:
            print 'Timeout! Try again'
            exit(0)


if __name__ == '__main__':
    main()
