import logging
from messages.base_message import BaseMessage
logger = logging.getLogger(__name__)

class NodeInformation:
    def __init__(self, nodeId, nodeName, nodeAge=1):
        logger.debug('Node information object init')
        self.nodeId = nodeId
        self.nodeName = nodeName
        self.nodeAge = nodeAge
        logger.debug('Node Id = {}, Node Name = {}, Node Age = {}'.format(self.nodeId, self.nodeName, self.nodeAge))

    def getJson(self):
        jsonDict = {}
        jsonDict['nodeId'] = self.nodeId
        jsonDict['nodeName'] = self.nodeName
        jsonDict['nodeAge'] = self.nodeAge
        return jsonDict