import json
import subprocess
from subprocess import Popen
import time 
import os 
import sys
import csv
#本算法中的时间计算系统按照美国西部时区进行计算
ssadmin_path = "~/documents/.ssmgr/ss-bash/ssadmin.sh"

def run_cmd(cmd):
    c = Popen(cmd, shell=True, stdout=subprocess.PIPE)
    results = c.stdout.readlines()
    return results 

def add_port(port, password, limit):
    cmd_head = ssadmin_path +" add " + str(port) + " " + password + " " + limit
    results = run_cmd(cmd_head)
    return results 

def del_port(port):
    cmd_head = ssadmin_path + " del " + str(port) 
    results = run_cmd(cmd_head)
    return results

#重置用量
def reset_used(port):
    cmd_head = ssadmin_path + " rused " + str(port) 
    results = run_cmd(cmd_head)
    return results

#显示各端口总用量，可以指定某一端口
def show_port(port=None):
    cmd_head = ssadmin_path +" show" 
    if port:
        cmd_head += (" " +str(port))
    results = run_cmd(cmd_head)
    return results[1:]

def ss_start():
    cmd_head = ssadmin_path + " start"
    return run_cmd(cmd_head)

def ss_restart():
    cmd_head = ssadmin_path + " restart"
    return run_cmd(cmd_head)

def ss_stop():
    cmd_head = ssadmin_path + " stop"
    return run_cmd(cmd_head)
