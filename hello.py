from flask import Flask
from flask import request,render_template, redirect, url_for
import sys
import subprocess
import json

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def tree():
    """
    Show the Group and Processes in a tree structure
    Returns values to test.html
    """
    print('Standard', file=sys.stderr)
    if request.method == "GET":
        print('Success')
        #Check if it's python or python2
        arg = ['python', 'client.py', '-ni', '-s', '1', '-c', 'show']
        proc1 = subprocess.Popen(arg, stdout=subprocess.PIPE)
        output = json.loads(proc1.communicate()[0])
        return render_template('test.html', data=output)


@app.route('/deletegroup', methods=["GET", "POST"])
def deletegroup():    
    """
    Input group name from HTML element and delete the group
    Redirected to tree function

    """
    if request.method == "POST":
        print('Inside deletegroup')
        del_group = request.form['groupDelete']
        arg = ['python', 'client.py', '-ni', '-s', '1', '-c', 'deleteGroup', del_group]
        groupdel = subprocess.Popen(arg, stdout=subprocess.PIPE)
        return redirect(url_for('tree'))


@app.route('/deleteprocess', methods=["POST"])
def deleteprocess():
    """
    Input group name and process name from HTML element and delete from the group
    Redirected to tree function

    """
    if request.method == "POST":
        print("Inside deleteprocess")
        group_proc_del = request.form['groupProcessDelete']
        del_proc = request.form['deleteProcess']
        print("GROUPNAME: {}\nPROCESSNAME: {}".format(group_proc_del, del_proc))
        arg = ['python', 'client.py', '-ni', '-s', '1', '-c', 'deleteProcess', group_proc_del, del_proc]
        processdel = subprocess.Popen(arg, stdout=subprocess.PIPE)
        return redirect(url_for('tree'))


@app.route('/addprocess', methods=["POST"])
def addprocess():
    """
    Input group name and process name from HTML element and add to the group
    Redirected to tree function

    """
    if request.method == "POST":
        print("Inside addprocess")
        group_proc_add = request.form['groupProcessAdd']
        add_proc = request.form['addProcess']
        print("GROUPNAME: {}\nPROCESSNAME: {}".format(group_proc_add, add_proc))
        arg = ['-ni', '-s', '1', '-c', 'addProcess']
        arg.append(group_proc_add)
        arg.append(add_proc)
        command = ' '.join(arg)
        command += str(group_proc_add) + ' '+str(add_proc)
        cmd = ['/usr/bin/python', '/Users/arun/git/distributed-systems-gmm/client.py', '-ni', '-s', '1', '-c', 'addProcess', group_proc_add, add_proc]
        print(cmd)
        processadd = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        return redirect(url_for('tree'))


if __name__ == '__main__':
    app.run(debug = True)
