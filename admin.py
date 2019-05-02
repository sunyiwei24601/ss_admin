import json
import subprocess
from subprocess import Popen
import time 
ssadmin_path = "~/documents/.ssmgr/ss-bash/ssadmin.sh"

def run_cmd(cmd):
    c = Popen(cmd, shell=True, stdout=subprocess.PIPE, stedrr=subprocess.STDOUT)
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

def reset_used(port):
    cmd_head = ssadmin_path + " rused " + str(port) 
    results = run_cmd(cmd_head)
    return results

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

class users():
    #strptime是把字符串转化为struct
    #strftime是把strcut转化为字符串
    #ctime是把时间戳转化为字符串
    #asctime是接受时间元组并返回一个可读的字符串形式
    #mktime是接受时间元组返回时间戳
    #time.time()返回当前的时间戳
    #localtime是接受时间戳，返回元组，没有参数就返回当前的时间元组

    def __init__(self, email, port, password):
        self.email = email
        self.port = port 
        self.password = password
        self.start_date = time.localtime() 




if __name__ =="__main__":

