#!/usr/bin/env python

import pexpect
import getpass
import sh
import os
username = 'root'
hostname = 'szwg-tdw-ftp06.szwg01'
remote_path = '~/.ssh/'
localfile = 'test.dat'
passwd = '123456'

def get_keys():
    child = pexpect.spawn("ssh-keygen -t dsa")
    if not child.expect("Generating public/private dsa key pair."):
        print "first"
        child.sendline("\n")
        if not child.expect("Enter passphrase"):
            print "second"
            child.send("\n")
            if not child.expect("Enter same passphrase again"):
                print "thrid"
                child.send("\n")
                if not child.expect("The key fingerprint is:"):
                    print "ok"
def copy_key_file():
    home_path = os.path.expanduser("~")
    key_file = home_path + "/.ssh/id_dsa.pub"
    current_path = str(sh.pwd().strip("\n")) + "/"
    print current_path
    sh.cp(key_file,current_path)

def scp_file(username,hostname,remote_path,localfile,passwd):
    '''a scp function to copy a file to remote machine
    '''
    cmd = 'scp %s %s@%s:%s' %(localfile,username,hostname,remote_path)
    scp_child=pexpect.spawn(cmd)

    if scp_child.expect('password:'):
        scp_child.sendline(passwd)
        print scp_child.read()

if __name__ == '__main__':
