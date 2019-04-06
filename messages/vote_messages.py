# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 13:17:46 2019

@author: manda
"""
import logging
from .base_message import BaseMessage

logger = logging.getLogger(__name__)

class RequestForVoteMessage(BaseMessage):

    def __init__(self, sender, receiver, term, data):
        BaseMessage.__init__(self, sender, receiver, term)
        self.data = data
        self.type = BaseMessage.RequestVote
        logger.debug('Request Vote Message. Message Type = {}, data = {}'.format(self.type, self.data))


class VoteResponseMessage(BaseMessage):

    def __init__(self, sender, receiver, term, data):
        BaseMessage.__init__(self, sender, receiver, term)
        self.type = BaseMessage.RequestVoteResponse
        self.data = data
        logger.debug('Vote Response Message. Message Type = {}, data = {}'.format(self.type, self.data))
