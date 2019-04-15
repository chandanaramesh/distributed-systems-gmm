import logging
from messages.base_message import BaseMessage
logger = logging.getLogger(__name__)

class NodeInformation:
    def __init__(self, nid, nn, na=1):
        self.nid = nid
        self.nn = nn
        self.na = na