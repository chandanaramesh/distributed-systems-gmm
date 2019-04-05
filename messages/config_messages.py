# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 13:27:50 2019

@author: manda
"""
import logging

logger = logging.getLogger(__name__)
messageType = {'change':4}

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
        self.type = messageType['change']
        logger.debug('Config Change: new_config = {}, uuid = {}, phase = {}, addr = {}'.format(new_config, uuid, phase, addr))
