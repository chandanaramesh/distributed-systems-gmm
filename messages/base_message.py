# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 13:16:23 2019

@author: manda
"""

import logging

logger = logging.getLogger(__name__)


class BaseMessage(object):
    AppendEntriesMessage = 0
    RequestVoteMessage = 1
    RequestVoteResponse = 2
    AppendEntriesResponse = 3
    ChangeMessage = 4
    RedirectMessage = 5
    ClientMessage = 6

    def __init__(self, sender, receiver, term):
        self.sender = sender
        self.receiver = receiver
        self.term = term
        logger.debug('Base Message Init. Sender = {}, Receiver = {}, term = {}'.format(sender, receiver, term))
