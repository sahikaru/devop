#!/usr/bin/env python

import pexpect
import getpass
import sh
import os
import paramiko

username = 'root'
hostname = 'szwg-tdw-ftp06.szwg01'
remote_path = '~/.ssh/believeme'
localfile = 'id_dsa.pub'
passwd = '123456'

def get_public_key():
    '''get pub-key file id_dsa.pub with shell command:
        ssh-keygen -t dsa
        file will generate in dirctory ~/.ssh
    '''
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
    '''copy pub key file id_dsa.pub to current dirctory
    '''
    key_file = os.environ["HOME"] + "/.ssh/id_dsa.pub"
    current_path = os.environ["PWD"] + "/"
    sh.cp(key_file,current_path)

def scp_file(username,hostname,remote_path,localfile,passwd):
    '''a scp function to copy a pub key file to remote machine
    as file believe_me
    '''
    local_file = os.environ["PWD"]+'/id_dsa.pub'
    remote_file = "/root/.ssh/believeme"

    t = paramiko.Transport((hostname,22))
    t.connect(username=username,password=passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(local_file,remote_file)
    t.close() 

    
def run_cmd():
    '''to build up trust relationship: backup old destination .ssh file 
    and write new .ssh file
    '''
    cmd_mkssh = "mv /root/.ssh /root/.ssh_bak;mkdir -m 700 .ssh"
    cmd_mvfile = "cat /root/.ssh/believeme > /root/.ssh/authorized_keys"

    remote_client = paramiko.SSHClient()
    remote_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_client.connect(hostname,22,username,passwd)
    stin,stdout,stderr = remote_client.exec_command(cmd_mkssh)
    scp_file(username,hostname,remote_path,localfile,passwd)
    stin,stdout,stderr = remote_client.exec_command(cmd_mvfile)
    
    print stdout.read()
    remote_client.close()

if __name__ == '__main__':
    get_public_key()
    copy_key_file()
    run_cmd()
