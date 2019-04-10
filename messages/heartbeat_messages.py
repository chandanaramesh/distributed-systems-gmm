import logging
from .base_message import BaseMessage

logger = logging.getLogger(__name__)

class HeartBeatMessage(BaseMessage):

    def __init__(self, sender, receiver, term):
        BaseMessage.__init__(self, sender, receiver, term)
        self.type = BaseMessage.HeartBeat
        # logger.debug('Append Entries Request Message. Message Type = {}, entries = {}, commit index = {}, previous Log Term = {}, previous Log Index = {}'.format(self.type, self.entries, self.commitIndex, self.prevLogTerm, self.prevLogIndex))

class HeartBeatResponseMessage(BaseMessage):

    def __init__(self, sender, receiver, term, success):
        BaseMessage.__init__(self, sender, receiver, term)
        self.success = success
        self.type = BaseMessage.HeartBeatResponse

