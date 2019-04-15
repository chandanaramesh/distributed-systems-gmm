import unittest
import subprocess32 as subprocess
import sys
import time


PATH = r'/distribute/distributed-systems-gmm/GroupManagement.py'
log_file_path = r'/distribute/distributed-systems-gmm/logs/GroupManagement-1.log'


class GroupManagementTests(unittest.TestCase):
    def setUp(self):
        pass

    def testfollower(self):

        cmd= "{0} PATH -sid {1} ".format
        p=subprocess.Popen(['/usr/bin/python',PATH, '-sid' , '1'],stdout=subprocess.PIPE)

        with open(log_file_path, 'r') as file:
            for line in file:
                match = line.split(" ")[8:15]
                #print match[0]
                value = ' '.join(match)
                #print value
                assert "Group Management Node Server with ID 1",value




    def testfollower1(self):

        with open(log_file_path, 'r') as file:
            for line in file:
                match = line.split(" ")[8:15]
                #print match[0]
                value = ' '.join(match)
                #print value
                assert "startElection Method server ID - 1",value
    
    
    def testfollower_running(self):
        with open(log_file_path, 'r') as file:
            for line in file:
                match = line.split(" ")[5:15]
                #print match[0]
                value = ' '.join(match)
                #print value
                assert "Running as a follower",value
    
    
    
    def test_leader_running(self):
        with open(log_file_path, 'r') as file:
            for line in file:
                match = line.split(" ")[5:15]
                #print match[0]
                value = ' '.join(match)
                #print value
                assert "Running as a leader",value






if __name__=='__main__':
    #Get path to client.py and set CLIENT_PATH

    unittest.main()


