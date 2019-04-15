def getJson(nodeInformation):
    jsonDict = {}
    jsonDict['nodeId'] = nodeInformation.nid
    jsonDict['nodeName'] = nodeInformation.nn
    jsonDict['nodeAge'] = nodeInformation.na
    return jsonDict