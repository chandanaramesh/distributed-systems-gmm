# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:09:31 2019

@author: manda
"""
import logging

logger = logging.getLogger(__name__)
messageType = {'redirect':5, 'client':6}

class Request(object):
    def __init__(self, request_msg, uuid = 0):
        self.request_msg = request_msg
        self.type = messageType['client']
        self.uuid = uuid
        logger.debug('Request: request_msg = {}, uuid = {}'.format(request_msg, uuid))

class RequestRedirect(Request):
    def __init__(self, request_msg, uuid, addr):
        self.request_msg = request_msg
        self.uuid = uuid
        self.addr = addr
        self.type = messageType['redirect']
        logger.debug('RequestRedirect: request_msg = {}, uuid = {}, addr = {}'.format(request_msg, uuid, addr))