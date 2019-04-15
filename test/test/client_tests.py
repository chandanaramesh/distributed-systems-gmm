import sys
import subprocess
import unittest

#This should not be hardcoded.
CLIENT_PATH = r'distribute/distributed-systems-gmm/client.py'

class ClientTests(unittest.TestCase):
    def setUp(self):
        pass

    def testShow(self):
        cmd = "{0} -ni -s {1} -c show".format
        #output = subprocess.call(['/usr/bin/python',CLIENT_PATH,'-ni','-s','1','-c','show'])
        p = subprocess.Popen(['/usr/bin/python',CLIENT_PATH,'-ni','-s','1','-c','show'], stdout=subprocess.PIPE)
        output, err = p.communicate()
        print 'output- ' +output
        assert 'GmmServersGroup' in output 

if __name__=='__main__':
    #Get path to client.py and set CLIENT_PATH

    unittest.main()
