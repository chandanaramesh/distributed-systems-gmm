# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:10:48 2019

@author: manda
"""
import logging
logger = logging.getLogger(__name__)

class LogEntry(object):

    def __init__(self, term, command, addr, uuid, _type = 0):
        self.term = term
        self.command = command
        self.uuid = uuid
        self.addr = addr
        self.type = _type
        logger.debug('Log Entry: Term = {}, command = {}, uuid = {}, addr = {}, type = {}'.format(term, command, uuid, addr, _type))
