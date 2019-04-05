# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 13:24:10 2019

@author: manda
"""
import logging
from .base_message import BaseMessage

logger = logging.getLogger(__name__)

class AppendEntriesMessage(BaseMessage):

    def __init__(self, sender, receiver, term, entries, commitIndex, prevLogIndex, prevLogTerm):
        BaseMessage.__init__(self, sender, receiver, term)
        self.type = BaseMessage.AppendEntries
        self.entries = entries
        self.commitIndex = commitIndex
        self.prevLogTerm = prevLogTerm
        self.prevLogIndex = prevLogIndex
        # logger.debug('Append Entries Request Message. Message Type = {}, entries = {}, commit index = {}, previous Log Term = {}, previous Log Index = {}'.format(self.type, self.entries, self.commitIndex, self.prevLogTerm, self.prevLogIndex))

class AppendEntriesResponseMessage(BaseMessage):

    def __init__(self, sender, receiver, term, success, matchIndex):
        BaseMessage.__init__(self, sender, receiver, term)
        self.success = success
        self.type = BaseMessage.AppendEntriesResponse
        self.matchIndex = matchIndex
        # logger.debug('Append Entries Response Message. Message Type = {}, success = {}, match index = {}'.format(self.type, self.success, self.matchIndex))
