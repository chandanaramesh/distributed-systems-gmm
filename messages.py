import time
import socket
import logging

logger = logging.getLogger(__name__)


class BaseMessage(object):
    AppendEntries = 0
    RequestVote = 1
    RequestVoteResponse = 2
    AppendEntriesResponse = 3

    def __init__(self, sender, receiver, term):
        self.sender = sender
        self.receiver = receiver
        self.term = term
        logger.debug('Base Message Init. Sender = {}, Receiver = {}, term = {}'.format(sender, receiver, term))


class RequestVoteMsg(BaseMessage):

    def __init__(self, sender, receiver, term, data):
        BaseMessage.__init__(self, sender, receiver, term)
        self.data = data
        self.type = BaseMessage.RequestVote
        logger.debug('Request Vote Message. Message Type = {}, data = {}'.format(self.type, self.data))


class VoteResponseMsg(BaseMessage):

    def __init__(self, sender, receiver, term, data):
        BaseMessage.__init__(self, sender, receiver, term)
        self.type = BaseMessage.RequestVoteResponse
        self.data = data
        logger.debug('Vote Response Message. Message Type = {}, data = {}'.format(self.type, self.data))

class AppendEntriesMsg(BaseMessage):

    def __init__(self, sender, receiver, term, entries, commitIndex, prevLogIndex, prevLogTerm):
        BaseMessage.__init__(self, sender, receiver, term)
        self.type = BaseMessage.AppendEntries
        self.entries = entries
        self.commitIndex = commitIndex
        self.prevLogTerm = prevLogTerm
        self.prevLogIndex = prevLogIndex
        # logger.debug('Append Entries Request Message. Message Type = {}, entries = {}, commit index = {}, previous Log Term = {}, previous Log Index = {}'.format(self.type, self.entries, self.commitIndex, self.prevLogTerm, self.prevLogIndex))

class AppendEntriesResponseMsg(BaseMessage):

    def __init__(self, sender, receiver, term, success, matchIndex):
        BaseMessage.__init__(self, sender, receiver, term)
        self.success = success
        self.type = BaseMessage.AppendEntriesResponse
        self.matchIndex = matchIndex
        # logger.debug('Append Entries Response Message. Message Type = {}, success = {}, match index = {}'.format(self.type, self.success, self.matchIndex))

class LogEntry(object):

    def __init__(self, term, command, addr, uuid, _type = 0):
        self.term = term
        self.command = command
        self.uuid = uuid
        self.addr = addr
        self.type = _type
        logger.debug('Log Entry: Term = {}, command = {}, uuid = {}, addr = {}, type = {}'.format(term, command, uuid, addr, _type))

class Request(object):
    """docstring for Request"""
    def __init__(self, request_msg, uuid = 0):
        self.request_msg = request_msg
        self.type = 'client'
        self.uuid = uuid
        logger.debug('Request: request_msg = {}, uuid = {}'.format(request_msg, uuid))

class RequestRedirect(Request):
    def __init__(self, request_msg, uuid, addr):
        self.request_msg = request_msg
        self.uuid = uuid
        self.addr = addr
        self.type = 'redirect'
        logger.debug('RequestRedirect: request_msg = {}, uuid = {}, addr = {}'.format(request_msg, uuid, addr))

class ServerConfig(object):
    def __init__(self, poolsize, currentTerm, votedFor, log, peers):
        self.poolsize = poolsize
        self.currentTerm = currentTerm
        self.votedFor = votedFor
        self.log = log
        self.peers = peers
        logger.debug('Server Configuration: poolsize = {}, currentTerm = {}, votedFor = {}. log = {}, peers = {}'.format(poolsize, currentTerm, votedFor, log, peers))
        # self.new_quorom = new_quorom

class ConfigChange(object):
    def __init__(self, new_config, uuid, phase, addr=None):
        self.new_config = new_config
        self.uuid = uuid
        self.addr = addr
        self.phase = phase
        self.type = 'change'
        logger.debug('Config Change: new_config = {}, uuid = {}, phase = {}, addr = {}'.format(new_config, uuid, phase, addr))
