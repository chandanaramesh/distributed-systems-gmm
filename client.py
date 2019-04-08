import socket
import json
import pickle
import uuid
import time

from KThread import *
#from MessageModels import *
from messages.config_messages import ConfigChange
from messages.request_redirect import Request

SHOW_STATE_TIMEOUT = 5
CHANGE_CONFIG_TIMEOUT = 20
BUY_TICKETS_TIMEOUT = 20

class ClientRequestor(object):
    cnt = 0
    def __init__(self):
        ClientRequestor.cnt = ClientRequestor.cnt + 1
        self.id = ClientRequestor.cnt
        self.num_of_reply = 0 

    def buyTickets(self, port, buy_msg, uuid):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = Request(buy_msg, uuid)
        s.sendto(pickle.dumps(msg), ("", port))
        while 1:
            try:
                reply, addr = s.recvfrom(1024)
                if reply != '':
                    self.num_of_reply += 1
                    print(reply)
                if self.num_of_reply == 2:
                    break
            except Exception as e:
                print 'Connection refused'
 
        s.close()

    def showState(self, port):
        print 'Making request to show'
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = Request('show')
        s.sendto(pickle.dumps(msg),("",port))
        while 1:
            try:
                reply, addr = s.recvfrom(1024)
                if reply != '':
                    print 'Pool Size', reply
                    break
            except Exception as e:
                print 'Connection refused'

    def configChange(self, port, new_config, uuid):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = ConfigChange(new_config, uuid, 1)
        s.sendto(pickle.dumps(msg),("",port))
        # we need to get committed twice
        while 1:
            try:
                reply, addr = s.recvfrom(1024)
                if reply != '':
                    self.num_of_reply != 1
                    print reply
                    break
            except Exception as e:
                print 'Connection refused'
        msg = ConfigChange(new_config, uuid, 2)
        s.sendto(pickle.dumps(msg), ("",port))
        while 1:
            try:
                reply, addr = s.recvfrom(1024)
                if reply != '':
                    print reply
                    break
            except Exception as e:
                print 'Connection refused'
        s.close()


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


def showHandler(clientRequest, ports, serverId):
    requestThread = KThread(target=clientRequest.showState, args=(ports[serverId - 1],))
    timeout = SHOW_STATE_TIMEOUT
    return timeout, requestThread


def changeHandler(request, clientRequestor, ports, serverId):
    uuid_ = uuid.uuid1()
    msg_split = request.split()
    new_config_msg = msg_split[1:]
    new_config = [int(item) for item in new_config_msg]
    print new_config
    requestThread = KThread(target=clientRequestor.configChange, args=(ports[serverId - 1], new_config, uuid_))
    timeout = CHANGE_CONFIG_TIMEOUT

def main():
    ports, num_ports = readConfig()
    while True:
        clientRequestor = ClientRequestor()
        serverId = input('Which node do you want to connect to? [1-%d]: ' % num_ports )
        print 'Accepted commands are [show | change | exit]'
        request = raw_input('How can we help you? -- ')
        if request == 'show':
            print 'Delegating to show handler'
            timeout, requestThread = showHandler(clientRequestor, ports, serverId)
        elif request.split()[0] == 'change':
            timeout, requestThread = changeHandler(request, clientRequestor, ports, serverId)
        elif request == 'exit':
            print 'Thanks for using the Group Management Client! See you next time'
            exit(0)
        else:
            uuid_ = uuid.uuid1()
            requestThread = KThread(target = clientRequestor.buyTickets, args =  (ports[serverId - 1], request, uuid_))
            timeout = BUY_TICKETS_TIMEOUT
        start_time = time.time()
        requestThread.start()
        while time.time() - start_time < timeout:
            if not requestThread.is_alive():
                break
        if requestThread.is_alive():
            print 'Timeout! Try again'
            requestThread.kill()

if __name__ == '__main__':
    main()