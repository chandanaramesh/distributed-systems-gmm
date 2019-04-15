import unittest
import subprocess32 as subprocess
import sys
import time

PATH = r'/distribute/distributed-systems-gmm/GroupManagement.py'
log_file_path = r'/distribute/distributed-systems-gmm/logs/GroupManagement-2.log'

class GroupManagementTests(unittest.TestCase):

   def setUp(self):
       pass

   def test_node(self):
       cmd= "{0} PATH -sid {1} &".format
       p=subprocess.Popen(['/usr/bin/python',PATH, '-sid' , '1'],stdout=subprocess.PIPE)
       time.sleep(5)
       cmd= "{0} PATH -sid {2} &".format
       p=subprocess.Popen(['/usr/bin/python',PATH, '-sid' , '2'],stdout=subprocess.PIPE)

       with open(log_file_path, 'r') as file:
           for line in file:
               match = line.split(" ")[7:15]
               #print match[0]
               value = ' '.join(match)
                #print value
               assert "Started listening on port 50002",value

   def testfollower(self):

        with open(log_file_path, 'r') as file:
            for line in file:
                match = line.split(" ")[7:15]
                #print match[0]
                value = ' '.join(match)
                #print value
                assert "Starting Group Management Node Server with ID 2",value




   def testfollower1(self):
        #cmd= "{0} PATH -sid {1} ".format
        #p=subprocess.Popen(['/usr/bin/python',PATH, '-sid' , '1'],stdout=subprocess.PIPE)

        with open(log_file_path, 'r') as file:
            for line in file:
                match = line.split(" ")[8:15]
                #print match[0]
                value = ' '.join(match)
                #print value
                assert "startElection Method server ID - 2",value

   def testfollower2(self):
        #cmd= "{0} PATH -sid {1} ".format
        #p=subprocess.Popen(['/usr/bin/python',PATH, '-sid' , '1'],stdout=subprocess.PIPE)

        with open(log_file_path, 'r') as file:
            for line in file:
                match = line.split(" ")[8:15]
                #print match[0]
                value = ' '.join(match)
                #print value
                assert "Server leader method",value


   def testfollower_running(self):
        #cmd= "{0} PATH -sid {1} ".format
        #p=subprocess.Popen(['/usr/bin/python',PATH, '-sid' , '1'],stdout=subprocess.PIPE)

        with open(log_file_path, 'r') as file:
            for line in file:
                match = line.split(" ")[5:15]
                #print match[0]
                value = ' '.join(match)
                #print value
                assert "Running as a follower",value




if __name__=='__main__':
    #Get path to client.py and set CLIENT_PATH

    unittest.main()


