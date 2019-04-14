# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 16:24:03 2019

@author: manda
"""

import json
import time
import uuid
import socket
import pickle
import random
import logging

from KThread import *
from messages.base_message import BaseMessage
from messages.log_messages import LogEntry
from messages.config_messages import ConfigChange
from messages.request_redirect import RequestRedirect
from messages.vote_messages import VoteResponseMessage
from messages.append_entries_messages import AppendEntriesResponseMessage

from commons.Constants import DEBUG, ACCEPTOR, SERVER_NODE_GROUP_NAME

logger = logging.getLogger(__name__)

def acceptor(server, data, addr):
    Msg = pickle.loads(data)
    _type = Msg.type

    switch = {
        0: appendEntriesMessage,
        1: requestVote,
        2: responseVote,
        3: appendEntriesResponse,
        4: changeConfig,
        5: clientRequests,
        6: clientRequests
    }

    switch[_type](server, Msg, addr)


def appendEntriesMessage(server, Msg, addr):
    _sender = Msg.sender
    _term = Msg.term
    entries = Msg.entries
    leaderCommit = Msg.commitIndex
    prevLogTerm = Msg.prevLogTerm
    prevLogIndex = Msg.prevLogIndex

    matchIndex = server.commitIndex

    # This is a valid new leader
    if _term >= server.currentTerm:
        server.currentTerm = _term
        server.save()
        server.stepDown()
        if server.role == 'follower':
            server.last_update = time.time()
        if prevLogIndex != 0:
            if len(server.log) >= prevLogIndex:
                if server.log[prevLogIndex - 1].term == prevLogTerm:
                    success = 'True'
                    server.leaderID = _sender
                    if len(entries) != 0:
                        server.log = server.log[:prevLogIndex] + entries
                        matchIndex = len(server.log)
                else:
                    success = 'False'
            else:
                success = 'False'
        else:
            success = 'True'
            if len(entries) != 0:
                server.log = server.log[:prevLogIndex] + entries
                server.save()
                matchIndex = len(server.log)
            server.leaderID = _sender
    else:
        success = 'False'

    # TODO - Update here for fast update
    if leaderCommit > server.commitIndex:
        lastApplied = server.commitIndex
        server.commitIndex = min(leaderCommit, len(server.log))
        if server.commitIndex > lastApplied:
            server.groupInfo = server.initialState
            for idx in range(1, server.commitIndex + 1):
                if server.log[idx - 1].type == BaseMessage.AppendEntriesMessage:
                    server.groupInfo = server.log[idx - 1].command
                elif server.log[idx - 1].type == BaseMessage.RequestVoteResponse:
                    server.during_change = 0

    reply_msg = AppendEntriesResponseMessage(server.id, _sender, server.currentTerm, success, matchIndex)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(pickle.dumps(reply_msg), ("", server.addressbook[_sender]))


def responseVote(server, Msg, addr):
    _sender = Msg.sender
    _term = Msg.term
    _msg = Msg.data
    if DEBUG or ACCEPTOR:
        print '---------Get vote response message---------'
    voteGranted = int(_msg)
    if voteGranted:
        if server.during_change == 0:
            if server.role == 'candidate':
                if _sender in server.request_votes:
                    server.request_votes.remove(_sender)
                server.numVotes += 1
                if server.numVotes == server.majority:
                    print 'Got majority votes, become leader at Term %d' % server.currentTerm
                    if server.election.is_alive():
                        server.election.kill()
                    # becomes a leader
                    server.role = 'leader'
                    server.follower_state.kill()
                    print 'new leader ', server.id, ' during change 0'
                    server.leader_state = KThread(target=server.leader, args=())
                    server.leader_state.start()
        else:
            server.request_votes.remove(_sender)
            if _sender in server.peers:
                server.newVotes += 1
            majority = len(server.new) / 2 + 1
            if server.newVotes >= majority:
                print 'Got majority from new, become leader at Term %d' % server.currentTerm
                if server.election.is_alive():
                    server.election.kill()
                server.role = 'leader'
                print 'new leader ', server.id
                server.follower_state.kill()
                server.leader_state = KThread(target=server.leader, args=())
                server.leader_state.start()
    else:
        if _term > server.currentTerm:  # discover higher term
            server.currentTerm = _term
            server.save()
            if DEBUG or ACCEPTOR:
                print 'Server '
            if server.role == 'candidate':
                server.stepDown()

        print 'vote rejected by ', _sender, ' to ', server.id


def requestVote(server, Msg, addr):
    _sender = Msg.sender
    _term = Msg.term
    if _sender not in server.peers:
        return
    _msg = Msg.data
    if DEBUG or ACCEPTOR:
        # TODO: Make the message better
        print '---------Get requestvote message--------- votes needed from  ', server.id, " ", server.currentTerm, " for ", _sender, " term ", _term

    _msg = _msg.split()
    log_info = (int(_msg[0]), int(_msg[1]))
    if _term < server.currentTerm:
        if DEBUG or ACCEPTOR:
            print 'rejected due to old term by ', server.id
        voteGranted = 0
    elif _term == server.currentTerm:
        if log_info >= (server.lastLogTerm, server.lastLogIndex) and (
                server.votedFor == -1 or server.votedFor == _sender):
            voteGranted = 1
            server.votedFor = _sender
            server.save()
        else:
            voteGranted = 0
    else:
        # find higher term in RequestForVoteMessage
        server.currentTerm = _term
        server.save()
        server.stepDown()

        if log_info >= (server.lastLogTerm, server.lastLogIndex):
            voteGranted = 1
            server.votedFor = _sender
            if DEBUG or ACCEPTOR:
                print 'found higher term.. log matched.. stepped down..given vote to ', _sender, ' by ', server.id
            server.save()
        else:
            voteGranted = 0
            if DEBUG or ACCEPTOR:
                print 'found higher term.. log mismatched.. stepped down..rejected vote to ', _sender, ' by ', server.id
    reply = str(voteGranted)
    reply_msg = VoteResponseMessage(server.id, _sender, server.currentTerm, reply)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(pickle.dumps(reply_msg), ("", server.addressbook[_sender]))


def appendEntriesResponse(server, message, addr):
    print ''
    print ''
    print 'Received message from server' + str(message.sender)
    _sender = message.sender
    _term = message.term
    success = message.success
    matchIndex = message.matchIndex

    print('*** Server %d *****' % server.id)
    print(server.groupInfo)

    if success == 'False':
        if _term > server.currentTerm:
            server.currentTerm = _term
            server.save()
            server.stepDown()
        else:
            server.nextIndex[_sender] -= 1
    else:
        if server.nextIndex[_sender] <= len(server.log) and matchIndex > server.matchIndex[_sender]:
            print 'Server logs length = %d' % len(server.log)
            print 'Follower Match Index = %d' % matchIndex
            print 'Server view of sender {} match Index = {}'.format(_sender, server.matchIndex[_sender])
            print 'Server view of sender {} next index = {}'.format(_sender, server.nextIndex[_sender])
            print 'Server Commit Index {}'.format(server.commitIndex)
            server.matchIndex[_sender] = matchIndex
            server.nextIndex[_sender] += 1

        if server.commitIndex < max(server.matchIndex.values()):
            start = server.commitIndex + 1
            print 'Server Commit index = %d' % start
            print 'Server Match Index Max = %d' % max(server.matchIndex.values())
            for N in range(start, max(server.matchIndex.values()) + 1):
                if server.during_change == 0:
                    # not in config change
                    compare = 1
                    for key, item in server.matchIndex.items():
                        if key in server.peers and item >= N:
                            compare += 1
                    majority = (len(server.peers) + 1) / 2 + 1
                    if compare == server.majority and server.log[N - 1].term == server.currentTerm:
                        for idx in range(server.commitIndex + 1, N + 1):
                            # TODO: THis is where server config is overwritten from the log
                            print '************* Hit the Error State of Resetting Group Info ************'
                            server.groupInfo = server.log[idx - 1].command
                            server.save()
                            _uuid = uuid.uuid1()
                            if message.sender in server.groupInfo[SERVER_NODE_GROUP_NAME]:
                                server.groupInfo[SERVER_NODE_GROUP_NAME][message.sender].nodeAge += 1
                            if server.id in server.groupInfo[SERVER_NODE_GROUP_NAME]:
                                server.groupInfo[SERVER_NODE_GROUP_NAME][server.id].nodeAge += 1
                            logEntry = LogEntry(server.currentTerm, server.groupInfo, BaseMessage.LocalMessageAddress,
                                                _uuid)
                            server.log.append(logEntry)
                            print 'Age Updated for self ' + str(server.id) + ' and peer server ' + str(message.sender)
                            if server.log[idx - 1].addr is not None:  # To Handle Local Messages
                                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                s.sendto('Your request is fullfilled', server.log[idx - 1].addr)
                                s.close()
                            logger.debug('Replied to the client')
                        server.commitIndex = N
     # print 'send new once'


def changeConfig(server, Msg, addr):
    print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& msg.phase, server,role &&&&&&&&&&&&&&&&&&&& ', Msg.phase, server.role
    if Msg.phase == 1:
        print 'Config change phase 1 ', server.id, " ", server.currentTerm
        server.during_change = 1
        server.new = Msg.new_config
        server.old = server.peers[:]
        server.old.append(server.id)
        if Msg.addr != None:
            addr = Msg.addr
        newEntry = LogEntry(server.currentTerm, Msg, addr, Msg.uuid, 1)
        server.log.append(newEntry)
        server.peers = list(set(server.old + server.new))
        server.peers.remove(server.id)
        server.save()
        print 'Config change phase 1 applied'
    # return
    else:
        print 'Config change phase 2 ', server.id, " ", server.currentTerm
        server.during_change = 2
        server.new = Msg.new_config
        if Msg.addr != None:
            addr = Msg.addr
        newEntry = LogEntry(server.currentTerm, Msg, addr, Msg.uuid, 2)
        server.log.append(newEntry)
        server.peers = server.new[:]
        if server.id in server.peers:
            server.peers.remove(server.id)
        server.save()
        print 'Config change phase 2 applied, running peers'

    if server.role != 'leader':
        print 'redirect config change to the leader from  ', server.id, " ", server.currentTerm
        if server.leaderID != 0:
            redirect_target = server.leaderID
        else:
            redirect_target = random.choice(server.peers)
        if Msg.addr != None:
            addr = Msg.addr
        redirect_msg = ConfigChange(Msg.new_config, Msg.uuid, Msg.phase, addr)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(pickle.dumps(redirect_msg), ("", server.addressbook[redirect_target]))
        s.close()

    return


def clientRequests(server, Msg, addr):
    # addr = Msg.addr
    msg_string = Msg.request_msg
    if msg_string == 'show':
        groupMap = {}
        for group in server.groupInfo:
            nodeMap = {}
            for node in server.groupInfo[group]:
                nodeMap[node] = server.groupInfo[group][node].getJson()
            groupMap[group] = nodeMap
        state = json.dumps(groupMap)
        show_msg = str(state)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(show_msg, addr)
        s.close()

    else:
        ticket_num = int(msg_string.split()[1])
        if server.role == 'leader':
            print "I am the leader, customer wants to buy %d tickets" % ticket_num
            if ticket_num > server.poolsize:
                print 'Tickets not enough'
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto('We do not have enough tickets', addr)
                s.close()
                return

            # check whether this command has already been
            for idx, entry in enumerate(server.log):
                if entry.uuid == Msg.uuid:
                    if server.commitIndex >= idx + 1:
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.sendto('Your request has been fullfilled', addr)
                        s.close()
                    else:  # ignore
                        pass
                    return  # ignore this new command

            newEntry = LogEntry(server.currentTerm, ticket_num, addr, Msg.uuid)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto('The Leader gets your request', addr)
            s.close()
            server.log.append(newEntry)
            print "server log"
            for logEntry in server.log:
                print logEntry.command
                print logEntry.addr
            server.save()
        # we need to redirect the request to leader
        else:
            print 'redirect the request to leader from ', server.id, " ", server.currentTerm
            if server.leaderID != 0:
                redirect_target = server.leaderID
            else:
                redirect_target = random.choice(server.peers)
            redirect_msg = RequestRedirect(msg_string, Msg.uuid, addr)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(pickle.dumps(redirect_msg), ("", server.addressbook[redirect_target]))
            s.close()
    return
