import json
import subprocess
from subprocess import Popen
import time 
import csv
#本算法中的时间计算系统按照美国西部时区进行计算
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

class users():
    #strptime是把字符串转化为struct
    #strftime是把strcut转化为字符串
    #ctime是把时间戳转化为字符串
    #asctime是接受时间元组并返回一个可读的字符串形式
    #mktime是接受时间元组返回时间戳----这个时间戳是将时间元组按照本地时间方式来计算
    #time.time()返回当前的时间戳
    #localtime是接受时间戳，返回元组，没有参数就返回当前的时间元组

    def __init__(self, email, port, password):
        self.email = email
        self.port = port 
        self.password = password
        self.start_date = time.localtime() 
        


def read_csv(filepath):
    f = csv.reader(open(filepath))
    records = [i for i in f]
    records = records[1:]
    return records

def search_users(l, email): #根据邮箱来寻找用户，如果没有则返回None
    for user in l:
        if user.email == email:
            return user
        else:
            return None



if __name__ =="__main__":
    record_nums = 0 #记录的总数目，在比对之后考虑是否加入新的交易记录
    users_list = [] #记录用户类的列表，搜索用户的工作在此进行
    while(True):
        #这里应该git pull一下
        records = read_csv("Records.csv")
        if len(records) > record_nums:
            new_records = records[record_nums:]
        
        #检查出有新的交易记录，首先审核用户是否存在，存在则更新，不存在则新建用户
        if new_records:
            for record in new_records:
                email = record[1]
                month = record[2]
                trs_time = record[3]
                port = record[4]
                password = record[5]

                user = search_users(users_list, email)
                if user:
                    #更新交易信息
                    pass 
                else:
                    user = users(email, port, password)                
                    #更新交易信息
                    users_list.append(user)
        break
        #交易数据更新结束之后，检查各个用户流量限制，时间限制，是否应该清零流量
        for user in users_list:
                current_time_stamp = time.time()
                end_time = user.end_time
                port = user.port 
                #到期则删除该port
                if current_time_stamp > end_time:
                    del_port(port)
                    user.active = False
                else: #未到期则检查是否应该重置端口
                    user.check_reset_usage()





















