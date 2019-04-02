kill -9 $(ps aux | grep 'GroupManagement.py' | grep -v grep | awk '{print $2}')
